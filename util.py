#from test import MainWindow, TableWidgetDemo_2, TableWidgetDemo


import numpy as np
import pandas as pd

#먼저 UI에서 교량의 총 길이, 하중, 교량의 높이, 부재의 종류를 받을 거임. 이게 인풋정보
# 인사이드 정보는 내부에서 계산하기 위해 사용할 정보
#Bridge_Length = int(input('교량 총 길이(m) :')) # UI가 없기때문에 일단 대충 만듬
#Bridge_Height = int(input('교량 높이(m) :'))
#Load = float(input('교량이 받는 하중(kN/m) :'))
#I_Cell = input('I빔의 H*B 값 :')
#H_Cell = input('H빔의 H*B 값 :')

#Bridge_Length = int(input('교량 총 길이(m) :')) # UI가 없기때문에 일단 대충 만듬
#Bridge_Height = int(input('교량 높이(m) :'))
#Load = float(input('교량이 받는 하중(kN/m) :'))
#I_Cell = input('I빔의 H*B 값 :')
#H_Cell = input('H빔의 H*B 값 :')


class inside_information() :
    def __init__(self):
        self.nodes_coordinates = np.empty((0, 2), dtype=float) # 절점 좌표 2차원 초기화 안하고 그냥 배열만 한다 np.empty(), 배열할 때마다 초기화하고 싶으면 np.zeros(), np.ones()m, np.full() 사용
        self.nodes_dof = np.empty((0, 2), dtype=float) # 절점 자유도 2차원
        self.elements = np.empty((0, 4), dtype=float) # 요소정보 2차원
        self.materials = np.empty((0, 5)) # 재료정보 2차원
        self.loads = np.array([], dtype=float) # 하중 행렬 1차원
        self.bottom_member_length = 10 # 하단 부재 한 개 길이 10m로 고정, 상단 부재도 동일
        self.upper_member_length = 10
        self.middle_member_length = None  # 중간 비스듬히 있는 부재
        self.num_of_bottom_members = int(Bridge_Length / self.bottom_member_length)
        self.elastic_modulus = 210000 # 단위는 MPa
        self.material_strength = 500
        self.I_total_self_weight = None
        self.H_total_self_weight = None
        self.I_beam_area = None
        self.H_beam_area = None
        self.nodes_iDOF = np.empty((0, 2), dtype=float)
        self.beam_choice = globals(beam_choice)


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
        if self.num_of_bottom_members >= 2 :
            if len(self.nodes_coordinates) >= 5 :
                point1 = np.array(self.nodes_coordinates[0])
                point2 = np.array(self.nodes_coordinates[1])
                self.middle_member_length = np.linalg.norm(point2 - point1)

            else :
                print('중간 부재의 길이를 계산하기에 절점 개수가 충분하지 않습니다.')
        else :
            print('중간 부재와 상단 부재가 존재하지 않습니다.')

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
                new_dof_pair.append(idof)
            self.nodes_iDOF = np.vstack([self.nodes_iDOF, new_dof_pair])

        return self.nodes_iDOF


    def material_properties(self):
        # 이 함수 호출하기 전에 중간부재 길이도 알아야하고 중간 부재 길이를 알려면 절점이 2개
        I_beam_path = r"C:\Users\chjw5\PycharmProjects\가상\I_beam_new.csv"
        H_beam_path = r"C:\Users\chjw5\PycharmProjects\가상\H_beam_new.csv"

        I_beam_data = pd.read_csv(I_beam_path, encoding='cp949')
        H_beam_data = pd.read_csv(H_beam_path, encoding='cp949')

        filtered_I = I_beam_data[I_beam_data['H*B(mm)'] == I_Cell]
        filtered_H = H_beam_data[H_beam_data['H*B(mm)'] == H_Cell]

        if self.middle_member_length is None:
            self.calculate_middle_member_length()

        if self.middle_member_length is not None:
            if filtered_I.empty :
                print('I-beam 데이터의 H*B(mm)가 비어있다')
                return
            if filtered_H.empty :
                print('H-beam 데이터의 H*B(mm)가 비어있다')
                return

            I_HB_data = filtered_I.iloc[0]
            self.I_beam_area = float(I_HB_data['단면적(cm^2)']) * 0.0001 # 단위변환 m^2으로
            I_unit_weight = float(I_HB_data['단위중량(kg/m)'])
            I_middle_beam_weight = float(I_unit_weight * self.middle_member_length)
            I_bottom_beam_weight = float(I_unit_weight * self.bottom_member_length)
            I_upper_beam_weight = I_bottom_beam_weight

            H_HB_data = H_beam_data[H_beam_data['H*B(mm)'] == H_Cell].iloc[0]
            self.H_beam_area = float(H_HB_data['단면적(cm^2)'] * 0.0001)
            H_unit_weight = float(H_HB_data['단위무게(kg/m)'])
            H_middle_beam_weight = float(H_HB_data['단위무게(kg/m)'] * self.middle_member_length)
            H_bottom_beam_weight = float(H_unit_weight * self.bottom_member_length)
            H_upper_beam_weight = H_bottom_beam_weight

            if self.num_of_bottom_members == 1 :
                self.I_total_self_weight = I_unit_weight * self.bottom_member_length
                self.H_total_self_weight = H_unit_weight * self.bottom_member_length

            else :
                self.I_total_self_weight = I_middle_beam_weight * (self.num_of_bottom_members * 2) + I_bottom_beam_weight * self.num_of_bottom_members + I_upper_beam_weight * (self.num_of_bottom_members - 1)
                self.H_total_self_weight = H_middle_beam_weight * (self.num_of_bottom_members * 2) + H_bottom_beam_weight * self.num_of_bottom_members + H_upper_beam_weight * (self.num_of_bottom_members - 1)

            if self.beam_choice == 'I_beam' : # self.beam_choice는 정우형 UI class를 부모 객체로 받으면 UI class __init__에 self.beam_choice가 있기 때문에 딱히 내 클래스에서 언급할 필요 없음.
                self.materials = np.array([self.elastic_modulus, self.material_strength, self.I_total_self_weight, self.I_beam_area])

            elif self.beam_choice == 'H_beam' :
                self.materials = np.array([self.elastic_modulus, self.material_strength, self.H_total_self_weight, self.H_beam_area])


    def define_elements(self):
        if self.middle_member_length is None :
            self.calculate_middle_member_length()

        if self.middle_member_length is not None :
            if self.nodes_iDOF.size == 0 :
                self.add_nodes_dof()

            if self.nodes_iDOF.size > 0 :
                if self.bottom_member_length < self.middle_member_length :
                    max_length = self.middle_member_length

                if self.bottom_member_length > self.middle_member_length :
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






