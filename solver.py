# InputData 클래스 : 사용자 입력 관리
class InputData:
    def __init__(self, Bridge_Length, Load, material_type):
        self.Load = Load  # kN/m
        self.Bridge_Length =Bridge_Length   # meters
        self.material_type = material_type  # 'I-beam' or 'H-beam'


import pandas as pd

# MaterialProperties 클래스 : 부재 재료의 속성 관리

# 파일 경로
class MaterialProperties:
    def __init__(self, h_beam_path, i_beam_path):
        # H빔 데이터 로드
        self.h_beam_data = pd.read_csv(h_beam_path, encoding='cp949')
        # I빔 데이터 로드
        self.i_beam_data = pd.read_csv(i_beam_path, encoding='utf-8-sig')

        # 데이터를 호칭치수 기준으로 인덱스 설정 후 딕셔너리로 변환
        self.h_beam_properties = self.h_beam_data.set_index('H*B(mm)').to_dict('index')
        self.i_beam_properties = self.i_beam_data.set_index('H*B(mm)').to_dict('index')

    def get_properties(self, beam_type, nominal_size):
        # 빔 유형과 호칭치수에 따라 속성 반환
        if beam_type == 'H-beam':
            return self.h_beam_properties[nominal_size]
        elif beam_type == 'I-beam':
            return self.i_beam_properties[nominal_size]


# 파일 경로
h_beam_path = r'C:\Users\chjw5\PycharmProjects\가상\H_beam_new.csv'
i_beam_path = r'C:\Users\chjw5\PycharmProjects\가상\I_beam_new.csv'

# MaterialProperties 인스턴스 생성
material_properties = MaterialProperties(h_beam_path, i_beam_path)

# NodeElementData 클래스: 절점, 자유도, 요소 정보 관리
class NodeElementData:
    def __init__(self):
        self.nodes = {}  # 예: {1: (x1, y1), 2: (x2, y2), ...}
        self.elements = {}  # 예: {1: (node1, node2, material_type), ...}
        self.degrees_of_freedom = {}  # 예: {1: 'free', 2: 'constrained', ...}

    def add_node(self, node_id, coordinates):
        self.nodes[node_id] = coordinates

    def add_element(self, element_id, node1, node2, material_type):
        self.elements[element_id] = (node1, node2, material_type)

    def set_freedom(self, node_id, status):
        self.degrees_of_freedom[node_id] = status

# ResultData 클래스: 계산 결과 저장
class ResultData:
    def __init__(self):
        self.forces = {}
        self.stresses = {}
        self.displacements = {}

    def store_result(self, element_id, force, stress, displacement):
        self.forces[element_id] = force
        self.stresses[element_id] = stress
        self.displacements[element_id] = displacement

# 데이터 클래스
class StructuralModel:
    def __init__(self):
        self.nodes = {}  # 노드 ID와 좌표: {node_id: (x, y)}
        self.elements = {}  # 요소 ID와 연결된 노드, 재료: {element_id: (node1, node2, material_type)}
        self.loads = {}  # 노드에 적용된 하중: {node_id: (Fx, Fy)}
        self.constraints = {}  # 노드의 경계조건: {node_id: (x_constraint, y_constraint)}

    def add_node(self, node_id, x, y):
        self.nodes[node_id] = (x, y)

    def add_element(self, element_id, node1, node2, material_type):
        self.elements[element_id] = (node1, node2, material_type)

    def add_load(self, node_id, Fx, Fy):
        self.loads[node_id] = (Fx, Fy)

    def add_constraint(self, node_id, x_constraint, y_constraint):
        self.constraints[node_id] = (x_constraint, y_constraint)


model = StructuralModel()

# 하중 및 경계조건 설정
def apply_distributed_load(model, load_per_meter, length, num_nodes):
    delta_x = length / (num_nodes - 1)
    for i in range(num_nodes):
        node_id = i + 1
        if i == 0 or i == num_nodes - 1:  # 끝점의 하중은 절반만 적용
            model.add_load(node_id, load_per_meter * delta_x / 2, 0)
        else:
            model.add_load(node_id, load_per_meter * delta_x, 0)

# 부재 강성 계산
import numpy as np


def calculate_element_stiffness(E, A, L, theta):
    theta_rad = np.radians(theta)
    c = np.cos(theta_rad)
    s = np.sin(theta_rad)

    # 요소의 로컬 강성 행렬
    k_local = (E * A / L) * np.array([[1, -1], [-1, 1]])

    # 변환 행렬
    T = np.array([
        [c, s, 0, 0],
        [-s, c, 0, 0],
        [0, 0, c, s],
        [0, 0, -s, c]
    ])

    # 전체 좌표계로의 강성 행렬 변환
    k_global = T.T @ k_local @ T
    return k_global

# 변위 계산
from scipy.linalg import solve

def calculate_displacements(K_global, forces):
    displacements = solve(K_global, forces)
    return displacements

# 변형률 및 응력 계산
def calculate_strain_and_stress(displacements, L, E):
    strain = displacements / L
    stress = E * strain
    return stress

#부재력 계산 및 안정성 평가
def calculate_force_and_evaluate(stress, A, allowable_stress):
    force = stress * A
    if force > allowable_stress:
        print("교량이 무너질 위험이 있습니다.")
    else:
        print("교량이 안전합니다.")


