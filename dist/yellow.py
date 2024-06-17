import numpy as np
import pandas as pd
import math
import scipy.linalg
from scipy import linalg

class inside_information:
    def __init__(self, Bridge_Length, Bridge_Height, Load, I_Cell, H_Cell, beam_choice, symbol):
        self.Bridge_Length = Bridge_Length
        self.Bridge_Height = Bridge_Height
        self.Load = Load
        self.I_Cell = I_Cell
        self.H_Cell = H_Cell
        self.beam_choice = beam_choice
        self.symbol = symbol

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
        self.top_bottom_k = np.empty((0, 4), dtype=float)
        self.top_bottom_T = np.empty((0, 4), dtype=float)
        self.top_bottom_T_inv = np.empty((0, 4), dtype=float)
        self.top_bottom_K = np.empty((0, 4), dtype=float)
        self.mid_k = np.empty((0, 4), dtype=float)
        self.mid_T = np.empty((0, 4), dtype=float)
        self.down_mid_T = np.empty((0, 4), dtype=float)
        self.mid_T_inv = np.empty((0, 4), dtype=float)
        self.down_mid_T_inv = np.empty((0, 4), dtype=float)
        self.mid_K = np.empty((0, 4), dtype=float)
        self.down_mid_K = np.empty((0, 4), dtype=float)
        self.max_elements = None
        # self.total_stiffness_matrix = total_stiffness_matrix

    def add_nodes_coordinates(self):  # 문제 없음
        if self.num_of_bottom_members == 1:
            total_num_nodes = 2
        elif self.num_of_bottom_members >= 2:
            total_num_nodes = 5 + ((self.num_of_bottom_members - 2) * 2)

        for i in range(total_num_nodes):
            if i == 0:
                nodes_x_coordinates = 0
                nodes_y_coordinates = 0
            if i >= 1:
                nodes_x_coordinates = 0.5 * i * self.bottom_member_length
                if i % 2 == 0:
                    nodes_y_coordinates = 0
                else:
                    nodes_y_coordinates = self.Bridge_Height
            self.nodes_coordinates = np.vstack([self.nodes_coordinates, [nodes_x_coordinates, nodes_y_coordinates]])

        return self.nodes_coordinates

    def calculate_middle_member_length(self):  # 문제 없음
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
            self.middle_member_length = 0
            print('중간 부재와 상단 부재가 존재하지 않습니다.')

        return self.middle_member_length

    def add_nodes_dof(self):  # 문제 없음
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
        return self.iFree  #달라짐

    def material_properties(self):
        # 이 함수 호출하기 전에 중간부재 길이도 알아야하고 중간 부재 길이를 알려면 절점이 2개
        I_beam_path = r"C:\Users\chjw5\PycharmProjects\가상\I_beam_new.csv"
        H_beam_path = r"C:\Users\chjw5\PycharmProjects\가상\H_beam_new.csv"

        I_beam_data = pd.read_csv(I_beam_path, encoding='UTF-8')
        H_beam_data = pd.read_csv(H_beam_path, encoding='UTF-8')

        filtered_I = I_beam_data[I_beam_data['H*B(mm)'] == self.I_Cell]
        filtered_H = H_beam_data[H_beam_data['H*B(mm)'] == self.H_Cell]

        if self.middle_member_length is None:
            self.calculate_middle_member_length()

        if self.middle_member_length is not None:
            if filtered_I.empty:
                #print('I-beam 데이터의 H*B(mm)가 비어있다')
                pass
            elif filtered_H.empty:
                #print('H-beam 데이터의 H*B(mm)가 비어있다')
                pass

            if self.beam_choice == 'I_beam' :
                I_HB_data = filtered_I.iloc[0]
                self.I_beam_area = float(I_HB_data['단면적(cm^2)']) * 0.0001  # 단위변환 m^2으로
                I_unit_weight = float(I_HB_data['단위중량(kg/m)'])
                I_middle_beam_weight = float(I_unit_weight * self.middle_member_length)
                I_bottom_beam_weight = float(I_unit_weight * self.bottom_member_length)
                I_upper_beam_weight = I_bottom_beam_weight

                if self.num_of_bottom_members == 1:
                    self.I_total_self_weight = I_unit_weight * self.bottom_member_length
                else:
                    self.I_total_self_weight = (I_middle_beam_weight * (self.num_of_bottom_members * 2) + I_bottom_beam_weight * self.num_of_bottom_members + I_upper_beam_weight * (self.num_of_bottom_members - 1))
                self.materials = np.array([self.elastic_modulus, self.material_strength, self.I_total_self_weight, self.I_beam_area])

            if self.beam_choice == 'H_beam' :
                H_HB_data = H_beam_data[H_beam_data['H*B(mm)'] == self.H_Cell].iloc[0]
                self.H_beam_area = float(H_HB_data['단면적(cm^2)'] * 0.0001)
                H_unit_weight = float(H_HB_data['단위무게(kg/m)'])
                H_middle_beam_weight = float(H_HB_data['단위무게(kg/m)'] * self.middle_member_length)
                H_bottom_beam_weight = float(H_unit_weight * self.bottom_member_length)
                H_upper_beam_weight = H_bottom_beam_weight

                if self.num_of_bottom_members == 1:
                    self.H_total_self_weight = H_unit_weight * self.bottom_member_length

                else:
                    self.H_total_self_weight = (H_middle_beam_weight * (self.num_of_bottom_members * 2) + H_bottom_beam_weight * self.num_of_bottom_members + H_upper_beam_weight * (self.num_of_bottom_members - 1))

                self.materials = np.array([self.elastic_modulus, self.material_strength, self.H_total_self_weight, self.H_beam_area])

        return self.materials

    def define_elements(self):
        if self.middle_member_length is None:
            self.calculate_middle_member_length()

        if self.middle_member_length is not None:
            if self.nodes_iDOF.size == 0:
                self.add_nodes_dof()

            if self.nodes_iDOF.size > 0:
                if self.bottom_member_length < self.middle_member_length:
                    max_length = self.middle_member_length

                if self.bottom_member_length > self.middle_member_length:
                    max_length = self.bottom_member_length

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

                if len(self.elements) != total_num_elements:
                    print('뭔가 단단히 잘못되었습니다.')
        return self.elements

    def add_load(self):
        if self.nodes_coordinates.size == 0:
            self.add_nodes_coordinates()

        if self.nodes_coordinates.size > 0:
            if self.num_of_bottom_members == 1:
                total_num_nodes = 2
            elif self.num_of_bottom_members >= 2:
                total_num_nodes = 5 + ((self.num_of_bottom_members - 2) * 2)

        if self.nodes_dof.size == 0:
            self.add_nodes_dof()

        if self.nodes_dof.size > 0:
            if self.materials.size == 0:
                self.material_properties()
            if self.materials.size > 0:
                mid_concentrated_load = int(self.Load) * int(self.Bridge_Length)
                node_load_before = mid_concentrated_load / total_num_nodes
                node_load = node_load_before * (-1)
                if self.beam_choice == 'I_beam' :
                    I_total_self_load = -(self.I_total_self_weight * 9.81 * 0.001) / self.Bridge_Length
                if self.beam_choice == 'H_beam' :
                    H_total_self_load = -(self.H_total_self_weight * 9.81 * 0.001) / self.Bridge_Length

                self.loads = np.zeros(total_num_nodes) + node_load  # 모든 노드에 동일한 하중 적용

                before_load = np.zeros(len(self.iFree), dtype=float)
                I_self_load = np.zeros(len(self.iFree), dtype=float)
                H_self_load = np.zeros(len(self.iFree), dtype=float)

                for i in range(len(self.iFree)):
                    if i % 2 != 0:
                        before_load[i] = node_load
                        if self.beam_choice == 'I_beam':
                            I_self_load[i] = I_total_self_load
                        elif self.beam_choice == 'H_beam':
                            H_self_load[i] = H_total_self_load

                if self.beam_choice == 'I_beam':
                    self.iDOF_load = before_load + I_self_load
                elif self.beam_choice == 'H_beam':
                    self.iDOF_load = before_load + H_self_load

                self.iDOF_load = np.round(self.iDOF_load, 3)

            return self.iDOF_load

    def transformation_matrix(self):
        cos_theta = np.cos(self.angle)
        sin_theta = np.sin(self.angle)
        return np.array([
            [cos_theta, sin_theta, 0, 0],
            [-sin_theta, cos_theta, 0, 0],
            [0, 0, cos_theta, sin_theta],
            [0, 0, -sin_theta, cos_theta]
        ])

    def down_transformation_matrix(self):
        cos_theta = np.cos(self.angle)
        sin_theta = np.sin(self.angle)
        return np.array([
            [-cos_theta, sin_theta, 0, 0],
            [-sin_theta, -cos_theta, 0, 0],
            [0, 0, -cos_theta, sin_theta],
            [0, 0, -sin_theta, -cos_theta]
        ])

    def global_transformation_matrix(self):  # 4 x 4 회전변환행렬
        T = self.transformation_matrix()
        T_global = np.zeros((4, 4))
        T_global[:2, :2] = T[:2, :2]
        T_global[2:4, 2:4] = T[2:4, 2:4]
        return np.round(T_global, 3)

    def down_global_transformation_matrix(self):  # 4 x 4 회전변환행렬 (Down버전)
        T = self.down_transformation_matrix()
        down_T_global = np.zeros((4, 4))
        down_T_global[:2, :2] = T[:2, :2]
        down_T_global[2:4, 2:4] = T[2:4, 2:4]
        return np.round(down_T_global, 3)

    def inverse_global_transformation_matrix(self):  # T 역행렬
        T_global = self.global_transformation_matrix()
        if T_global.size > 0:
            T_global_inv = linalg.inv(T_global)
            return np.round(T_global_inv, 3)
        else:
            return np.eye(4)

    def down_inverse_global_transformation_matrix(self):  # D_T 역행렬
        down_T_global = self.down_global_transformation_matrix()
        if down_T_global.size > 0:
            down_T_global_inv = linalg.inv(down_T_global)
            return np.round(down_T_global_inv, 3)
        else:
            return np.eye(4)

    def construct_stiffness_matrix(self):
        # 강성 행렬에 필요한 것들. material_properties 에서 탄성계수 E, 단면적 A, 교량의 총 길이 L,  K = EA/L

        if self.middle_member_length is None:
            self.calculate_middle_member_length()

        T = np.eye(4)

        if self.middle_member_length is not None:
            if self.materials.size == 0:
                self.material_properties()
                # print('실행됐음')

            if self.materials.size > 0:
                Area = float(self.materials[3])
                Elastic = self.elastic_modulus
                top_and_bottom_Length = self.bottom_member_length
                mid_Length = self.middle_member_length
                top_bottom_Stiff = (Elastic * Area) / top_and_bottom_Length
                mid_Stiff = (Elastic * Area) / mid_Length

                self.top_bottom_T = np.array([[1, 0, 0, 0],
                                              [0, 1, 0, 0],
                                              [0, 0, 1, 0],
                                              [0, 0, 0, 1]])

                self.top_bottom_T_inv = np.linalg.inv(self.top_bottom_T)

                self.top_bottom_k = top_bottom_Stiff * np.array([[1, 0, -1, 0],
                                                                 [0, 0, 0, 0],
                                                                 [-1, 0, 1, 0],
                                                                 [0, 0, 0, 0]])

                self.top_bottom_K = self.top_bottom_T_inv @ self.top_bottom_k @ self.top_bottom_T  # @는 행렬 곱셈

                self.mid_T = self.global_transformation_matrix()
                self.mid_T_inv = self.inverse_global_transformation_matrix()
                self.down_mid_T = self.down_global_transformation_matrix()
                self.down_mid_T_inv = self.down_inverse_global_transformation_matrix()

                self.mid_k = mid_Stiff * np.array([[1, 0, -1, 0],
                                                   [0, 0, 0, 0],
                                                   [-1, 0, 1, 0],
                                                   [0, 0, 0, 0]])

                self.mid_K = self.mid_T_inv @ self.mid_k @ self.mid_T

                self.down_mid_K = self.down_mid_T_inv @ self.mid_k @ self.down_mid_T

        return self.down_mid_K

    def calculate_max_elements(self):
        if self.elements.size == 0:
            self.define_elements()
        if self.elements.size > 0:
            self.max_elements = np.max(np.array(self.elements))

    def construct_total_stiffness_matrix(self):

        if self.top_bottom_K.size == 0 and self.mid_K.size == 0:
            self.construct_stiffness_matrix()
        if self.top_bottom_K.size > 0 and self.mid_K.size > 0:
            if self.elements.size == 0 and self.max_elements is None:
                self.define_elements()
                self.calculate_max_elements()
            if self.elements.size > 0 and self.max_elements is not None:
                total_stiffness_matrix = np.zeros([int(self.max_elements), int(self.max_elements)])

                for i in range(1, len(self.elements) + 1):
                    if i % 2 != 0:
                        even_columns = [int(x) for x in self.elements[i - 1]]
                        if i % 4 != 3:
                            mid_members_df = pd.DataFrame(self.mid_K, columns=even_columns, index=even_columns)
                            even_columns1 = mid_members_df.columns.tolist()
                            for j in even_columns1:
                                for k in even_columns1:
                                    if j > 0 and k > 0:
                                        total_stiffness_matrix[j - 1, k - 1] += mid_members_df.loc[j, k]
                        if i % 4 == 3:
                            mid_members_df = pd.DataFrame(self.down_mid_K, columns=even_columns, index=even_columns)
                            even_columns1 = mid_members_df.columns.tolist()
                            for j in even_columns1:
                                for k in even_columns1:
                                    if j > 0 and k > 0:
                                        total_stiffness_matrix[j - 1, k - 1] += mid_members_df.loc[j, k]

                    if i % 2 == 0:
                        odd_columns = [int(x) for x in self.elements[i - 1]]
                        top_bottom_members_df = pd.DataFrame(self.top_bottom_K, columns=odd_columns, index=odd_columns)
                        odd_columns1 = top_bottom_members_df.columns.tolist()
                        for j in odd_columns1:
                            for k in odd_columns1:
                                if j > 0 and k > 0:
                                    total_stiffness_matrix[j - 1, k - 1] += top_bottom_members_df.loc[j, k]

        return total_stiffness_matrix
        # return np.zeros((1, 1)) # 조건을 만족하지 않는 경우 기본행렬 반환

    def construct_displacement_matrix(self):
        total_stiffness_matrix = self.construct_total_stiffness_matrix()
        if total_stiffness_matrix.size == 0 or total_stiffness_matrix.ndim != 2:
            raise ValueError('비어있거나 2차원이 아니거나')
        # print('전체강성행렬 크기 : ', total_stiffness_matrix.shape)

        if self.iDOF_load.size == 0:
            self.add_load()
        if self.iDOF_load.ndim == 1:  # 1차원 배열이면 2차원으로 변환
            self.iDOF_load = self.iDOF_load.reshape(-1, 1)
        total_stiffness_matrix_inv = linalg.inv(total_stiffness_matrix)
        displacement_matrix = total_stiffness_matrix_inv @ self.iDOF_load
        return displacement_matrix


#A = inside_information()
#print(self.construct_displacement_matrix())

