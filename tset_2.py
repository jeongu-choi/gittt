import numpy as np
import pandas as pd

#먼저 UI에서 교량의 총 길이, 하중, 교량의 높이, 부재의 종류를 받을 거임. 이게 인풋정보
# 인사이드 정보는 내부에서 계산하기 위해 사용할 정보

class inside_information :
    def __init__(self):
        self.nodes_coordinates = np.empty((0, 2), dtype=float) # 절점 좌표 2차원 초기화 안하고 그냥 배열만 한다 np.empty(), 배열할 때마다 초기화하고 싶으면 np.zeros(), np.ones()m, np.full() 사용
        self.nodes_dof = np.empty((0, 2), dtype=float) # 절점 자유도 2차원
        self.elements = np.array([], dtype=int) # 요소정보 2차원
        self.materials = np.empty((0, 5), dtype=float) # 재료정보 2차원
        self.loads = np.array([], dtype=float) # 하중 행렬 1차원
        self.bottom_member_length = 10 # 하단 부재 한 개 길이 10m로 고정, 상단 부재도 동일
        self.upper_member_length = 10
        self.middle_member_length = None  # 중간 비스듬히 있는 부재
        self.num_of_bottom_members = int(Bridge_Length / self.bottom_member_length)
        self.elastic_modulus = 210000 # 단위는 MPa
        self.material_strength = 500
        self.I_total_self_weight = None
        self.H_total_self_weight = None


    def add_nodes_coordinates(self): #문제 없음
        if self.num_of_bottom_members == 1 :
            total_num_nodes = 2
        elif self.num_of_bottom_members >= 2 :
            total_num_nodes = 5 + ((self.num_of_bottom_members - 2) * 2)

        for i in range(total_num_nodes) :
            if i == 0 :
                nodes_x_coordinates = 0
                nodes_y_coordinates = 0
            if i >= 1 :
                nodes_x_coordinates = 0.5 * i * self.bottom_member_length
                if i % 2 == 0 :
                    nodes_y_coordinates = 0
                else :
                    nodes_y_coordinates = Bridge_Height
            self.nodes_coordinates = np.vstack([self.nodes_coordinates, [nodes_x_coordinates, nodes_y_coordinates]])

    def calculate_middle_member_length(self): #문제 없음
        if len(self.nodes_coordinates) > 1 :
            point1 = np.array(self.nodes_coordinates[0])
            point2 = np.array(self.nodes_coordinates[1])
            self.middle_member_length = np.linalg.norm(point2 - point1)

        else :
            return print('부재의 길이를 계산하기 위해서는 상단 절점이 있어야 합니다.')

    def add_nodes_dof(self): #문제 없음
        if self.num_of_bottom_members == 1 :
            total_num_nodes = 2
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


    def material_properties(self): #문제 없음
        I_beam_path = 'C:\\Users\\sooha\\PycharmProjects\\가상환경\\I-beam.csv'
        H_beam_path = 'C:\\Users\\sooha\\PycharmProjects\\가상환경\\H-beam.csv'

        I_beam_data = pd.read_csv(I_beam_path, encoding='cp949')
        H_beam_data = pd.read_csv(H_beam_path, encoding='cp949')

        I_HB_data = I_beam_data[I_beam_data['H*B(mm)'] == I_Cell].iloc[0]
        I_beam_area = I_HB_data['단면적(cm^2)'] * 0.0001 # 단위변환 m^2으로
        I_middle_beam_weight = I_HB_data['단위중량(kg/m)'] * self.middle_member_length

        H_HB_data = H_beam_data[H_beam_data['H*B(mm)'] == H_Cell].iloc[0]
        H_beam_area = H_HB_data['단면적(cm^2)'] * 0.0001
        H_middle_beam_weight = H_HB_data['단위무게(kg/m)'] * self.middle_member_length

        self.I_total_self_weight = I_middle_beam_weight * (self.num_of_bottom_members * 2)

