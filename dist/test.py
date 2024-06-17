import sys
import numpy as np
import pandas as pd
import math
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget, QLabel, QAbstractItemView
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from yoni import Ui_MainWindow  # 생성된 파이썬 파일의 이름에 따라 import 구문이 달라질 수 있습니다.
from secondwindow import Ui_Form
from third import Ui_Form_2
from yellow import inside_information  # yellow.py에서 inside_information 클래스를 임포트


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.H_beam.clicked.connect(self.groupboxRadFunction)
        self.ui.I_beam.clicked.connect(self.groupboxRadFunction)

        # self.ui.Bridge_Length.returnPressed.connect(self.print_Bridge_Length)
        # self.ui.Load.returnPressed.connect(self.printLoad)
        # self.ui.Bridge_Height.returnPressed.connect(self.print_Bridge_Height)
        self.ui.calculate_button.clicked.connect(self.run_calculations)  # 계산 버튼 클릭 시 실행

        self.window_2 = None
        self.window_3 = None
        self.beam_choice = None
        self.symbol = 0

        self.Bridge_Length = 0
        self.Bridge_Height = 0
        self.Load = 0
        self.I_Cell = ""
        self.H_Cell = ""

        self.label = self.ui.pixmap
        if self.label:
            pixmap = QPixmap(r"C:\Users\chjw5\PycharmProjects\가상\H_I_beam.png")
            self.label.setPixmap(pixmap)

        self.label = self.ui.warren_truss
        if self.label:
            warren_truss = QPixmap(r"C:\Users\chjw5\PycharmProjects\가상\triangle.jpg")
            self.label.setPixmap(warren_truss)

        self.ui.symbol_dialog.currentIndexChanged.connect(self.update_symbol)

    def groupboxRadFunction(self):
        if self.ui.H_beam.isChecked():
            self.beam_choice = 'H_beam'
            self.window_2 = TableWidgetDemo("your_excel_file.csv", "tableWidget")
            self.window_2.show()
        elif self.ui.I_beam.isChecked():
            self.beam_choice = 'I_beam'
            self.window_3 = TableWidgetDemo_2("I_beam.csv", "tableWidget_2")
            self.window_3.show()

    # def print_Bridge_Length(self):
    # self.Bridge_Length = int(self.ui.Bridge_Length.text())

    # def printLoad(self):
    # self.Load = int(self.ui.Load.text())

    # def print_Bridge_Height(self):
    # self.Bridge_Height = int(self.ui.Bridge_Height.text())

    def run_calculations(self):
        self.Bridge_Length = int(self.ui.Bridge_Length.text())
        self.Load = int(self.ui.Load.text())
        self.Bridge_Height = int(self.ui.Bridge_Height.text())
        self.I_Cell = self.window_3.I_Cell if self.window_3 else ""
        self.H_Cell = self.window_2.H_Cell if self.window_2 else ""
        self.symbol = int(self.symbol)


        inside_info = inside_information(
            self.Bridge_Length, self.Bridge_Height, self.Load, self.I_Cell, self.H_Cell, self.beam_choice, self.symbol
        )

        inside_info.add_nodes_coordinates()
        inside_info.calculate_middle_member_length()
        inside_info.add_nodes_dof()
        inside_info.material_properties()
        inside_info.define_elements()
        inside_info.add_load()
        inside_info.transformation_matrix()
        stiffness_matrix = inside_info.construct_stiffness_matrix()
        inside_info.down_transformation_matrix()
        inside_info.global_transformation_matrix()
        inside_info.down_global_transformation_matrix()
        inside_info.inverse_global_transformation_matrix()
        inside_info.down_inverse_global_transformation_matrix()
        inside_info.construct_stiffness_matrix()
        inside_info.calculate_max_elements()
        inside_info.construct_total_stiffness_matrix()
        inside_info.construct_displacement_matrix()
        nodes_dof = inside_info.construct_displacement_matrix()
        print(nodes_dof)



    def update_symbol(self):
        symbol_map = {
            "SS235": 235,
            "SS275": 275,
            "SS315": 315,
            "SS410": 410,
            "SS450": 450,
            "SS550": 550
        }
        selected_text = self.ui.symbol_dialog.currentText()
        self.symbol = symbol_map.get(selected_text, 0)
        #print(f"Selected symbol value: {self.symbol}")


class TableWidgetDemo(QWidget):
    def __init__(self, file_path, table_name):
        super(TableWidgetDemo, self).__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.table_name = table_name
        self.ui.tableWidget.cellDoubleClicked.connect(self.cell_double_clicked)
        self.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.H_Cell = ""

        self.load_csv_data(file_path)

    def cell_double_clicked(self, row, column):
        item = self.ui.tableWidget.item(row, column)
        if item:
            self.H_Cell = item.text()

    def load_csv_data(self, file_path):
        try:
            df = pd.read_csv(file_path)
            table_widget = getattr(self.ui, self.table_name)
            table_widget.setRowCount(len(df))
            table_widget.setColumnCount(len(df.columns))
            table_widget.setHorizontalHeaderLabels(df.columns)
            for row_index, row_data in enumerate(df.values):
                for col_index, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(str(cell_data))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                    table_widget.setItem(row_index, col_index, item)
        except Exception as e:
            print(f"Error loading CSV file: {e}")


class TableWidgetDemo_2(QWidget):
    def __init__(self, file_path, table_name):
        super(TableWidgetDemo_2, self).__init__()

        self.ui = Ui_Form_2()
        self.ui.setupUi(self)
        self.table_name = table_name
        self.ui.tableWidget_2.cellDoubleClicked.connect(self.cell_double_clicked)
        self.ui.tableWidget_2.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.I_Cell = ""

        self.load_csv_data_2(file_path)

    def cell_double_clicked(self, row, column):
        item = self.ui.tableWidget_2.item(row, column)
        if item:
            self.I_Cell = item.text()

    def load_csv_data_2(self, file_path):
        try:
            df = pd.read_csv(file_path)
            table_widget_2 = getattr(self.ui, self.table_name)
            table_widget_2.setRowCount(len(df))
            table_widget_2.setColumnCount(len(df.columns))
            table_widget_2.setHorizontalHeaderLabels(df.columns)
            for row_index, row_data in enumerate(df.values):
                for col_index, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(str(cell_data))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                    table_widget_2.setItem(row_index, col_index, item)
        except Exception as e:
            print(f"Error loading CSV file: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
