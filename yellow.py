import numpy as np
import pandas as pd
import math

class inside_information:
    def __init__(self, Bridge_Length, Bridge_Height, Load, I_Cell, H_Cell, beam_choice):
        self.Bridge_Length = Bridge_Length
        self.Bridge_Height = Bridge_Height
        self.Load = Load
        self.I_Cell = I_Cell
        self.H_Cell = H_Cell
        self.beam_choice = beam_choice

        self.nodes_coordinates = np.empty((0, 2), dtype=float)
        self.nodes_dof = np.empty((0, 2), dtype=float)
        self.elements = np.empty((0, 4), dtype=float)
        self.materials = np.empty((0, 5))
        self.loads = np.array([], dtype=float)
        self.bottom_member_length = 10
        self.upper_member_length = 10
        self.middle_member_length = None
        self.num_of_bottom_members = int(self.Bridge_Length / self.bottom_member_length)
        self.elastic_modulus = 210000
        self.material_strength = 500
        self.I_total_self_weight = None
        self.H_total_self_weight = None
        self.I_beam_area = None
        self.H_beam_area = None
        self.nodes_iDOF = np.empty((0, 2), dtype=float)
        self.iFree = np.array([], dtype=float)
        self.iDOF_load = np.array([], dtype=float)
        self.stiffness_materix = np.empty(())
        self.angle = np.arctan(self.Bridge_Height / (self.bottom_member_length * 0.5))

    def add_nodes_coordinates(self):
        if self.num_of_bottom_members == 1:
            total_num_nodes = 2
        elif self.num_of_bottom_members >= 2:
            total_num_nodes = 5 + ((self.num_of_bottom_members - 2) * 2)

        for i in range(total_num_nodes):
            if i == 0:
                nodes_x_coordinates = 0
                nodes_y_coordinates = 0
            else:
                nodes_x_coordinates = 0.5 * i * self.bottom_member_length
                if i % 2 == 0:
                    nodes_y_coordinates = 0
                else:
                    nodes_y_coordinates = self.Bridge_Height
            self.nodes_coordinates = np.vstack([self.nodes_coordinates, [nodes_x_coordinates, nodes_y_coordinates]])

    def calculate_middle_member_length(self):
        if self.num_of_bottom_members >= 2:
            if self.nodes_coordinates.size == 0:
                self.add_nodes_coordinates()
            if self.nodes_coordinates.size > 0:
                if len(self.nodes_coordinates) >= 5:
                    point1 = np.array(self.nodes_coordinates[0])
                    point2 = np.array(self.nodes_coordinates[1])
                    self.middle_member_length = np.linalg.norm(point2 - point1)
                else:
                    print('중간 부재의 길이를 계산하기에 절점 개수가 충분하지 않습니다.')
        else:
            print('중간 부재와 상단 부재가 존재하지 않습니다.')

    def add_nodes_dof(self):
        if self.num_of_bottom_members == 1:
            total_num_nodes = 2
        elif self.num_of_bottom_members >= 2:
            total_num_nodes = 5 + ((self.num_of_bottom_members - 2) * 2)
        for i in range(total_num_nodes):
            if i == 0:
                dof = [1, 1]
            elif i == total_num_nodes - 1:
                dof = [0, 1]
            else:
                dof = [0, 0]
            self.nodes_dof = np.vstack([self.nodes_dof, dof])
        iFree = 0
        iR = 0
        for dof_pair in self.nodes_dof:
            new_dof_pair = []
            for dof in dof_pair:
                if dof == 1:
                    iR += 1
                    idof = -iR
                else:
                    iFree += 1
                    idof = iFree
                    self.iFree = np.append(self.iFree, [iFree])
                new_dof_pair.append(idof)
            self.nodes_iDOF = np.vstack([self.nodes_iDOF, new_dof_pair])

    def material_properties(self):
        I_beam_path = r"C:\Users\chjw5\PycharmProjects\가상\I_beam_new.csv"
        H_beam_path = r"C:\Users\chjw5\PycharmProjects\가상\H_beam_new.csv"

        I_beam_data = pd.read_csv(I_beam_path, encoding='UTF-8')
        H_beam_data = pd.read_csv(H_beam_path, encoding='UTF-8')

        filtered_I = I_beam_data[I_beam_data['H*B(mm)'] == self.I_Cell]
        filtered_H = H_beam_data[H_beam_data['H*B(mm)'] == self.H_Cell]

        # 필터된 데이터 출력 (디버깅용)
        print("Filtered I-beam data:", filtered_I)
        print("Filtered H-beam data:", filtered_H)

        if self.middle_member_length is None:
            self.calculate_middle_member_length()

        if self.middle_member_length is not None:
            if filtered_I.empty:
                print('I-beam 데이터의 H*B(mm)가 비어있다')
                return
            if filtered_H.empty:
                print('H-beam 데이터의 H*B(mm)가 비어있다')
                return

            I_HB_data = filtered_I.iloc[0]
            self.I_beam_area = float(I_HB_data['단면적(cm^2)']) * 0.0001
            I_unit_weight = float(I_HB_data['단위중량(kg/m)'])
            I_middle_beam_weight = float(I_unit_weight * self.middle_member_length)
            I_bottom_beam_weight = float(I_unit_weight * self.bottom_member_length)
            I_upper_beam_weight = I_bottom_beam_weight

            H_HB_data = filtered_H.iloc[0]
            self.H_beam_area = float(H_HB_data['단면적(cm^2)'] * 0.0001)
            H_unit_weight = float(H_HB_data['단위무게(kg/m)'])
            H_middle_beam_weight = float(H_HB_data['단위무게(kg/m)'] * self.middle_member_length)
            H_bottom_beam_weight = float(H_unit_weight * self.bottom_member_length)
            H_upper_beam_weight = H_bottom_beam_weight

            if self.num_of_bottom_members == 1:
                self.I_total_self_weight = I_unit_weight * self.bottom_member_length
                self.H_total_self_weight = H_unit_weight * self.bottom_member_length
            else:
                self.I_total_self_weight = I_middle_beam_weight * (
                            self.num_of_bottom_members * 2) + I_bottom_beam_weight * self.num_of_bottom_members + I_upper_beam_weight * (
                                                       self.num_of_bottom_members - 1)
                self.H_total_self_weight = H_middle_beam_weight * (
                            self.num_of_bottom_members * 2) + H_bottom_beam_weight * self.num_of_bottom_members + H_upper_beam_weight * (
                                                       self.num_of_bottom_members - 1)

            if self.beam_choice == 'I_beam':
                self.materials = np.array(
                    [self.elastic_modulus, self.material_strength, self.I_total_self_weight, self.I_beam_area])
            elif self.beam_choice == 'H_beam':
                self.materials = np.array(
                    [self.elastic_modulus, self.material_strength, self.H_total_self_weight, self.H_beam_area])

    def define_elements(self):
        if self.middle_member_length is None:
            self.calculate_middle_member_length()

        if self.middle_member_length is not None:
            if self.nodes_iDOF.size == 0:
                self.add_nodes_dof()

            if self.nodes_iDOF.size > 0:
                max_length = max(self.bottom_member_length, self.middle_member_length)
                if self.num_of_bottom_members == 1:
                    total_num_elements = 1
                elif self.num_of_bottom_members >= 2:
                    total_num_elements = 7 + ((self.num_of_bottom_members - 2) * 4)

                for i in range(len(self.nodes_coordinates)):
                    for j in range(i + 1, len(self.nodes_coordinates)):
                        distance = np.linalg.norm(self.nodes_coordinates[i] - self.nodes_coordinates[j])
                        if distance <= max_length:
                            element_iDOF = list(self.nodes_iDOF[i]) + list(self.nodes_iDOF[j])
                            self.elements = np.vstack([self.elements, element_iDOF])
        return self.elements

    def add_load(self):
        if self.nodes_coordinates.size == 0:
            self.add_nodes_coordinates()

        if self.nodes_coordinates.size > 0:
            total_num_nodes = 2 if self.num_of_bottom_members == 1 else 5 + ((self.num_of_bottom_members - 2) * 2)

        if self.nodes_dof.size == 0:
            self.add_nodes_dof()

        if self.nodes_dof.size > 0:
            mid_concentrated_load = int(self.Load) * int(self.Bridge_Length)
            node_load_before = mid_concentrated_load / total_num_nodes
            node_load = node_load_before * (-1)
            for _ in range(total_num_nodes):
                self.loads = np.append(self.loads, [node_load])
            for _ in range(len(self.iFree)):
                self.iDOF_load = np.append(self.iDOF_load, [node_load])

    def construct_stiffness_matrix(self):
        E = None  # E 변수 초기화
        if self.middle_member_length is None:
            self.calculate_middle_member_length()

        if self.middle_member_length is not None:
            if self.materials.size == 0:
                self.material_properties()

            if self.materials.size > 0:
                A = float(self.materials[3])
                E = self.elastic_modulus
                top_and_bottom_Length = self.bottom_member_length
                mid_Length = self.middle_member_length

                top_bottom_Stiff = (E * A) / top_and_bottom_Length
                mid_Stiff = (E * A) / mid_Length
                T = np.array([[math.cos(self.angle), math.sin(self.angle), 0, 0],
                              [(-math.sin(self.angle)), math.cos(self.angle), 0, 0],
                              [0, 0, math.cos(self.angle), math.sin(self.angle)],
                              [0, 0, -math.sin(self.angle), math.cos(self.angle)]])

                top_bottom_k = top_bottom_Stiff * np.array([[1, 0, -1, 0],
                                                            [0, 0, 0, 0],
                                                            [-1, 0, 1, 0],
                                                            [0, 0, 0, 0]])
        return E

    def transformation_matrix(self):
        cos_theta = np.cos(self.angle)
        sin_theta = np.sin(self.angle)
        T = np.array([
            [cos_theta, sin_theta],
            [-sin_theta, cos_theta]
        ])
        return T

    def global_transformation_matrix(self):
        T = self.transformation_matrix()
        T_global = np.zeros((4, 4))
        T_global[0:2, 0:2] = T
        T_global[2:4, 2:4] = T
        return T_global

    def inverse_global_transformation_matrix(self):
        T_global = self.global_transformation_matrix()
        T_global_inv = np.linalg.inv(T_global)
        return T_global_inv

# 삭제하거나 필요시 테스트 코드로 사용하세요.
# if __name__ == "__main__":
#     Bridge_Length = float(input('교량 총 길이(m) :'))
#     Bridge_Height = float(input('교량 높이(m) :'))
#     Load = float(input('교량이 받는 하중(kN/m) :'))
#     I_Cell = input('I빔의 H*B 값 :')
#     H_Cell = input('H빔의 H*B 값 :')
#     beam_choice = 'H_beam'  # 예시로 설정, 필요에 따라 변경하세요
#     inside_info = inside_information(Bridge_Length, Bridge_Height, Load, I_Cell, H_Cell, beam_choice)
#     inside_info.add_nodes_coordinates()
#     inside_info.calculate_middle_member_length()
#     inside_info.add_nodes_dof()
#     inside_info.material_properties()
#     inside_info.define_elements()
#     inside_info.add_load()
#     stiffness_matrix = inside_info.construct_stiffness_matrix()
#     print(stiffness_matrix)
