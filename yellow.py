import numpy as np
import pandas as pd
import math
import scipy.linalg
from scipy import linalg
import os
import subprocess
import time
import warnings
import openpyxl
from openpyxl.drawing.image import Image
warnings.filterwarnings('ignore') # 경고 무시
import matplotlib.pyplot as plt
plt.rc('font', family='Malgun Gothic') # 한글 깨짐
import matplotlib
matplotlib.rcParams['axes.unicode_minus'] = False # 음수 표시

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
        self.elastic_modulus = 210000 * (10 ** 3) # KPa
        self.material_strength = self.symbol * (10 ** 3) # KPa
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

    def calculate_middle_member_length(self): #문제 없음
        if self.num_of_bottom_members >= 2 :
            if self.nodes_coordinates.size == 0 :
                self.add_nodes_coordinates()
            if self.nodes_coordinates.size > 0 :
                if len(self.nodes_coordinates) >= 5 :
                    point1 = np.array(self.nodes_coordinates[0])
                    point2 = np.array(self.nodes_coordinates[1])
                    self.middle_member_length = np.linalg.norm(point2 - point1)

                else :
                    print('중간 부재의 길이를 계산하기에 절점 개수가 충분하지 않습니다.')
        if self.num_of_bottom_members == 1 :
            print('트러스 구조가 아닙니다.')

        #return self.middle_member_length

    def add_nodes_dof(self): #문제 없음
        if self.num_of_bottom_members == 1 :
            print('트러스 구조가 아닙니다.')
        elif self.num_of_bottom_members >= 2 :
            total_num_nodes = 5 + ((self.num_of_bottom_members - 2) * 2)
        for i in range(total_num_nodes) :
            if i == 0 :
                dof = [1, 1]
            elif i == total_num_nodes - 1 :
                dof = [0, 1]
            else :
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
        return self.iFree

    def material_properties(self):
        # 이 함수 호출하기 전에 중간부재 길이도 알아야하고 중간 부재 길이를 알려면 절점이 2개
        I_beam_path = 'C:\\Users\\chjw5\\PycharmProjects\\가상\\I_beam_renewal.csv'
        H_beam_path = 'C:\\Users\\chjw5\\PycharmProjects\\가상\\H_beam_new.csv'

        I_beam_data = pd.read_csv(I_beam_path, encoding='utf-8')
        H_beam_data = pd.read_csv(H_beam_path, encoding='utf-8')

        filtered_I = I_beam_data[I_beam_data['H*B(mm)'] == self.I_Cell]
        filtered_H = H_beam_data[H_beam_data['H*B(mm)'] == self.H_Cell]

        if self.middle_member_length is None:
            self.calculate_middle_member_length()

        if self.middle_member_length is not None:
            if filtered_I.empty :
                #print('I-beam 데이터의 H*B(mm)가 비어있다')
                pass
            if filtered_H.empty :
                #print('H-beam 데이터의 H*B(mm)가 비어있다')
                pass

            if self.beam_choice == 'I_beam':
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

            if self.beam_choice == 'H_beam':
                H_HB_data = filtered_H.iloc[0]
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
        if self.num_of_bottom_members == 1 :
            print('트러스 구조가 아닙니다.')

        if self.middle_member_length is None :
            self.calculate_middle_member_length()

        if self.middle_member_length is not None :
            if self.nodes_iDOF.size == 0 :
                self.add_nodes_dof()

            if self.nodes_iDOF.size > 0 :

                if self.num_of_bottom_members == 1:
                    print('트러스 구조가 아닙니다.')

                elif self.num_of_bottom_members >= 2:
                    total_num_elements = 7 + ((self.num_of_bottom_members - 2) * 4)

                for i in range(len(self.nodes_coordinates)):
                    for j in range(i + 1, len(self.nodes_coordinates)):

                        distance = np.linalg.norm(self.nodes_coordinates[i] - self.nodes_coordinates[j])

                        if self.nodes_coordinates[i, 1] != self.nodes_coordinates[j, 1] :
                            max_length = self.middle_member_length

                        if self.nodes_coordinates[i, 1] == self.nodes_coordinates[j, 1] :
                            max_length = self.bottom_member_length

                        if distance <= max_length:
                            element_iDOF = list(self.nodes_iDOF[i]) + list(self.nodes_iDOF[j])
                            self.elements = np.vstack([self.elements, element_iDOF])

                if len(self.elements) != total_num_elements :
                                print('뭔가 단단히 잘못되었습니다.')
        return self.elements, len(self.elements)


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
                if self.beam_choice == 'I_beam':
                    I_total_self_load = -(self.I_total_self_weight * 9.81 * 0.001) / self.Bridge_Length
                if self.beam_choice == 'H_beam':
                    H_total_self_load = -(self.H_total_self_weight * 9.81 * 0.001) / self.Bridge_Length

                self.loads = np.zeros(total_num_nodes) + node_load  # 모든 노드에 동일한 하중 적용

                before_load = np.zeros(len(self.iFree), dtype=float)
                I_self_load = np.zeros(len(self.iFree), dtype=float)
                H_self_load = np.zeros(len(self.iFree), dtype=float)

                if self.num_of_bottom_members == 1 :
                    print('트러스 구조가 아닙니다.')

                if self.num_of_bottom_members > 1 :
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

    def global_transformation_matrix(self): # 4 x 4 회전변환행렬
        T = self.transformation_matrix()
        T_global = np.zeros((4, 4))
        T_global[:2, :2] = T[:2, :2]
        T_global[2:4, 2:4] = T[2:4, 2:4]
        return np.round(T_global, 3)

    def down_global_transformation_matrix(self): # 4 x 4 회전변환행렬 (Down버전)
        T = self.down_transformation_matrix()
        down_T_global = np.zeros((4, 4))
        down_T_global[:2, :2] = T[:2, :2]
        down_T_global[2:4, 2:4] = T[2:4, 2:4]
        return np.round(down_T_global, 3)

    def inverse_global_transformation_matrix(self): # T 역행렬
        T_global = self.global_transformation_matrix()
        if T_global.size > 0 :
            T_global_inv = linalg.inv(T_global)
            return np.round(T_global_inv, 3)
        else :
            return np.eye(4)

    def down_inverse_global_transformation_matrix(self): # D_T 역행렬
        down_T_global = self.down_global_transformation_matrix()
        if down_T_global.size > 0 :
            down_T_global_inv = linalg.inv(down_T_global)
            return np.round(down_T_global_inv, 3)
        else :
            return np.eye(4)

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
        #강성 행렬에 필요한 것들. material_properties 에서 탄성계수 E, 단면적 A, 교량의 총 길이 L,  K = EA/L

        if self.num_of_bottom_members == 1 :
            print('트러스 구조가 아닙니다.')

        if self.middle_member_length is None :
            self.calculate_middle_member_length()

        if self.middle_member_length is not None and self.middle_member_length > 0 :
            if self.materials.size == 0 :
                self.material_properties()
                #print('실행됐음')

            if self.materials.size > 0 :
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

                self.top_bottom_K = self.top_bottom_T_inv @ self.top_bottom_k @ self.top_bottom_T   # @는 행렬 곱셈

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
        if self.elements.size == 0 :
            self.define_elements()
        if self.elements.size > 0 :
            self.max_elements = np.max(np.array(self.elements))
        return self.max_elements


    def construct_total_stiffness_matrix(self):
        if self.num_of_bottom_members == 1:
            print('트러스 구조가 아닙니다.')

        if self.top_bottom_K.size == 0 and self.mid_K.size == 0 :
            self.construct_stiffness_matrix()
        if self.top_bottom_K.size > 0 and self.mid_K.size > 0 :
            if self.elements.size == 0 and self.max_elements is None :
                self.define_elements()
                self.calculate_max_elements()
            if self.elements.size > 0 and self.max_elements is not None :
                total_stiffness_matrix = np.zeros([int(self.max_elements), int(self.max_elements)])

                for i in range(1, len(self.elements) + 1) :
                    if i % 2 != 0 :
                        even_columns = [int(x) for x in self.elements[i - 1]]
                        if i % 4 != 3 :
                            mid_members_df = pd.DataFrame(self.mid_K, columns=even_columns, index=even_columns)
                            even_columns1 = mid_members_df.columns.tolist()
                            for j in even_columns1 :
                                for k in even_columns1 :
                                    if j > 0 and k > 0 :
                                        total_stiffness_matrix[j-1, k-1] += mid_members_df.loc[j, k]
                        if i % 4 == 3 :
                            mid_members_df = pd.DataFrame(self.down_mid_K, columns=even_columns, index=even_columns)
                            even_columns1 = mid_members_df.columns.tolist()
                            for j in even_columns1:
                                for k in even_columns1:
                                    if j > 0 and k > 0:
                                        total_stiffness_matrix[j - 1, k - 1] += mid_members_df.loc[j, k]

                    if i % 2 == 0 :
                        odd_columns = [int(x) for x in self.elements[i - 1]]
                        top_bottom_members_df = pd.DataFrame(self.top_bottom_K, columns=odd_columns, index=odd_columns)
                        odd_columns1 = top_bottom_members_df.columns.tolist()
                        for j in odd_columns1 :
                            for k in odd_columns1 :
                                if j > 0 and k > 0 :
                                    total_stiffness_matrix[j-1, k-1] += top_bottom_members_df.loc[j, k]

        return total_stiffness_matrix
        #return np.zeros((1, 1)) # 조건을 만족하지 않는 경우 기본행렬 반환


    def construct_displacement_matrix(self):
        if self.num_of_bottom_members == 1 :
            print('트러스 구조가 아닙니다.')

        total_stiffness_matrix = self.construct_total_stiffness_matrix()
        if total_stiffness_matrix.size == 0 or total_stiffness_matrix.ndim != 2 :
            raise ValueError('비어있거나 2차원이 아니거나')
        #print('전체강성행렬 크기 : ', total_stiffness_matrix.shape)

        if self.iDOF_load.size == 0:
            self.add_load()
        if self.iDOF_load.ndim == 1 : # 1차원 배열이면 2차원으로 변환
            self.iDOF_load = self.iDOF_load.reshape(-1, 1)
        total_stiffness_matrix_inv = linalg.inv(total_stiffness_matrix)
        displacement_matrix = total_stiffness_matrix_inv @ self.iDOF_load
        return displacement_matrix

    def calculate_members_force(self):
        displacement_matrix = self.construct_displacement_matrix()
        dof_members_force_matrix = np.empty((0, 4), dtype=float)
        total_members_force_matrix = np.array([], dtype=float)

        for i in range(1, len(self.elements) + 1) :
            element_displacement_matrix = np.zeros((1, 4))

            for j in range(4):
                if self.elements[i-1, j] < 0:
                    element_displacement_matrix[0, j] = 0
                else:
                    element_displacement_matrix[0, j] = displacement_matrix[int(self.elements[i-1, j]) - 1, 0]

            element_displacement_matrix_t = element_displacement_matrix.T # 1x4를 4x1로 변환(전치행렬)

            if i % 2 != 0 :
                if i % 4 != 3 :
                    M = self.mid_K
                if i % 4 == 3 :
                    M = self.down_mid_K
            if i % 2 == 0 :
                M = self.top_bottom_K

            member_force_matrix = M @ element_displacement_matrix_t
            f = member_force_matrix.T
            dof_members_force_matrix = np.vstack([dof_members_force_matrix, f])

        for a in range(1, len(self.elements) + 1) :

            if dof_members_force_matrix[a - 1, 1] != 0 :
                point1 = dof_members_force_matrix[a - 1, 0]
                point2 = dof_members_force_matrix[a - 1, 1]
                mid_member_force = -round(np.sqrt(point1 ** 2 + point2 ** 2), 3) # 중간부재들은 모두 압축력을 받는다.
                total_members_force_matrix = np.append(total_members_force_matrix, mid_member_force)
            if dof_members_force_matrix[a - 1, 1] == 0 :
                if dof_members_force_matrix[a - 1, 0] < 0 : # 인장강도
                    top_bottom_force = round(dof_members_force_matrix[a - 1, 0] * (-1), 3)
                    total_members_force_matrix = np.append(total_members_force_matrix, top_bottom_force)
                else : # 압축강도
                    top_bottom_force = -round(dof_members_force_matrix[a - 1, 0], 3)
                    total_members_force_matrix = np.append(total_members_force_matrix, top_bottom_force)

        return total_members_force_matrix

    def evaluate_safety_to_excel(self):
        if self.material_properties().size == 0 :
            self.material_properties()
        if self.material_properties().size > 0 :
            Area = self.materials[3]
            material_strength = self.material_strength * Area
            total_members_force_matrix = self.calculate_members_force()
            total_members_force_list = total_members_force_matrix.tolist()
            results = []
            columns = ['부재 번호', '부재력', '허용강도', '판단여부', '오차율']
            index = [str(a) for a in range(1, len(self.elements) + 1)]
            for i, member_force in enumerate(total_members_force_list) :
                if abs(member_force) >= material_strength : # 부재력이 강재의 강도보다 크거나 같은 경우 : NG 같은 경우도 NG라 판단 -> 최대한 안정적으로
                    status = 'NG'
                    recommendation = f'{(abs(member_force) - material_strength) / abs(member_force) * 100 : .2f}%'
                if abs(member_force) < material_strength : # 부재력이 강재의 강도보다 작을 경우 : OK
                    status = 'OK'
                    recommendation = '-'

                results.append([i + 1, member_force, material_strength, status, recommendation])

            result_df = pd.DataFrame(results, columns=columns, index=index)

            excel_filename = '최종 결과.xlsx'
            result_df.to_excel(excel_filename, index=False) # 인덱스를 따로 추가해서 기본적으로 오는 인덱스 제거
            print('엑셀 파일 저장 완료.')

            try :
                subprocess.call(['taskkill', '/F', '/IM', 'EXCEL.EXE'])
                time.sleep(1)
            except Exception as e :
                print('엑셀 프로세스 종료 중 오류 발생 :', e)

    def plot_truss(self):
        if self.nodes_coordinates.size == 0:
            self.add_nodes_coordinates()
            self.evaluate_safety_to_excel()

        if self.nodes_coordinates.size > 0:
            finale_df = pd.read_excel('C:\\Users\\chjw5\\PycharmProjects\\가상\\최종 결과.xlsx')

            plt.figure(figsize=(15, 5))
            total_members_force_list = self.calculate_members_force().tolist()

            for i in range(len(self.nodes_coordinates) - 2):
                point1 = self.nodes_coordinates[i]
                point2 = self.nodes_coordinates[i + 1]
                point3 = self.nodes_coordinates[i + 2]
                # 선 색상 결정
                if finale_df.loc[i, '판단여부'] == 'NG':
                    color = 'orangered'
                    label = 'NG'
                else:
                    color = 'deepskyblue'
                    label = 'OK'
                # 선 그리기
                plt.plot([point1[0], point2[0]], [point1[1], point2[1]], color=color, label=label)
                plt.plot([point1[0], point3[0]], [point1[1], point3[1]], color=color, label=label)
                plt.plot([point2[0], point3[0]], [point2[1], point3[1]], color=color, label=label)

                mid_x1 = (point1[0] + point2[0]) / 2
                mid_x2 = (point1[0] + point3[0]) / 2
                mid_x3 = (point2[1] + point3[1]) / 2
                mid_y1 = (point1[1] + point2[1]) / 2
                mid_y2 = (point1[1] + point3[1]) / 2
                mid_y3 = (point2[1] + point3[1]) / 2

                force = total_members_force_list[i]
                force_str = f'{force:.2f}'
                fontsize_base = 15
                fontsize = max(5, fontsize_base - np.exp(0.5 * len(force_str))) # force 개수에 따라 폰트는 점점 작아져야함

                # 텍스트 그리기 (배경색 추가 및 위치 조정)
                plt.text(mid_x1, mid_y1 - 0.3, f'{force:.2f}', fontsize=fontsize, ha='center', va='bottom',
                         bbox=dict(facecolor='white', alpha=1, edgecolor='none', pad=0.5))
                plt.text(mid_x2, mid_y2 - 0.3, f'{force:.2f}', fontsize=fontsize, ha='center', va='bottom',
                         bbox=dict(facecolor='white', alpha=1, edgecolor='none', pad=0.5))
                plt.text(mid_x3, mid_y3 - 0.3, f'{force:.2f}', fontsize=fontsize, ha='center', va='bottom',
                         bbox=dict(facecolor='white', alpha=1, edgecolor='none', pad=0.5))

            plt.xlim(-(self.Bridge_Length * 0.1), self.Bridge_Length * 1.1)
            plt.ylim(-(self.Bridge_Height * 0.3), self.Bridge_Height * 1.3)
            hinge = self.nodes_coordinates[0]
            roller = self.nodes_coordinates[len(self.nodes_coordinates) - 1]
            plt.title('와렌 트러스')
            plt.grid(False)
            plt.plot(hinge[0], hinge[1], '^', color='black')
            plt.plot(roller[0], roller[1], 'o', color='black')
            plt.xlabel('X (m)')
            plt.ylabel('Y (m)')
            # plt.show()

            image_path = '와렌트러스 그림.png'
            plt.savefig(image_path)
            # plt.close()
            self.insert_image_to_excel()

    def insert_image_to_excel(self):
        excel_filename = 'C:\\Users\\chjw5\\PycharmProjects\\가상\\최종 결과.xlsx'
        image_filename = 'C:\\Users\\chjw5\\PycharmProjects\\가상\\와렌트러스 그림.png'

        wb = openpyxl.load_workbook(excel_filename)
        ws = wb.active

        img = Image(image_filename)
        img.anchor = 'G1'
        ws.add_image(img)
        wb.save(excel_filename)

        print('이미지가 엑셀 파일에 삽입되었습니다.')

        os.startfile(excel_filename)
    #os.startfile(excel_filename)


#A = inside_information()
#print(self.construct_displacement_matrix())

