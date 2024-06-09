import sys
import pandas as pd
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget, QLabel, QAbstractItemView, QStyledItemDelegate
from PySide6.QtCore import Qt, QPoint, QRect
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QPen,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from yoni import Ui_MainWindow  # 생성된 파이썬 파일의 이름에 따라 import 구문이 달라질 수 있습니다.
from PySide6.QtUiTools import QUiLoader
from secondwindow import Ui_Form
from third import Ui_Form_2
from simple_truss_test import inside_information
import string

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.H_beam.clicked.connect(self.groupboxRadFunction)
        self.ui.I_beam.clicked.connect(self.groupboxRadFunction)
        self.ui.Bridge_Length.returnPressed.connect(self.print_Bridge_Length)
        self.ui.Load.returnPressed.connect(self.printLoad)
        self.ui.Bridge_Height.returnPressed.connect(self.print_Bridge_Height())
        self.window_2 = None
        self.window_3 = None
        self.beam_choice = None

        # 'label'이라는 객체 이름을 가진 Label 위젯을 찾습니다.
        self.label = self.ui.pixmap
        if self.label:
            # QPixmap 객체를 생성하고 이미지 파일을 로드합니다.
            pixmap = QPixmap(r"C:\Users\chjw5\PycharmProjects\가상\H_I_beam.png")
            # Label 위젯에 QPixmap 객체를 설정합니다.
            self.label.setPixmap(pixmap)

        self.label = self.ui.warren_truss
        if self.label:
            # QPixmap 객체를 생성하고 이미지 파일을 로드합니다.
            warren_truss = QPixmap(r"C:\Users\chjw5\PycharmProjects\가상\triangle.jpg")
            # Label 위젯에 QPixmap 객체를 설정합니다.
            self.label.setPixmap(warren_truss)

    def groupboxRadFunction(self):
        if self.ui.H_beam.isChecked():
            self.beam_choice = 'H_beam'
            print(self.beam_choice)

            self.window_2 = TableWidgetDemo("your_excel_file.csv", "tableWidget")
            self.window_2.show()

        elif self.ui.I_beam.isChecked():
            self.beam_choice = 'I_beam'
            print(self.beam_choice)

            self.window_3 = TableWidgetDemo_2("I_beam.csv", "tableWidget_2")
            self.window_3.show()

    def print_Bridge_Length(self):
        # Lineedit에 있는 글자를 가져오는 메서드
        Bridge_Length = (self.ui.Bridge_Length.text())

        #print(Bridge_Length)

    def printLoad(self):
        Load = (self.ui.Load.text())
        #print(Load)

    def print_Bridge_Height(self):
        Bridge_Height = (self.ui.Bridge_Height.text())

class TableWidgetDemo(QWidget):
    def __init__(self, file_path, table_name):
        super(TableWidgetDemo, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.table_name = table_name
        self.ui.tableWidget.cellDoubleClicked.connect(self.cell_double_clicked)
        self.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # CSV 파일 읽기
        self.load_csv_data(file_path)

    def cell_double_clicked(self, row, column):
        item = self.ui.tableWidget.item(row, column)
        if item:
            H_Cell = item.text()  # 더블클릭한 셀의 값을 H_Cell 변수에 저장
            #print(H_Cell)  # H_Cell 변수의 값을 출력

    def load_csv_data(self, file_path):
        try:
            # pandas를 사용하여 CSV 파일 읽기
            df = pd.read_csv(file_path)

            # 테이블 위젯 선택
            table_widget = getattr(self.ui, self.table_name)

            # 행과 열의 수 설정
            table_widget.setRowCount(len(df))
            table_widget.setColumnCount(len(df.columns))

            # CSV 파일의 헤더를 테이블 헤더로 설정
            table_widget.setHorizontalHeaderLabels(df.columns)

            # 데이터를 테이블 위젯에 삽입
            for row_index, row_data in enumerate(df.values):
                for col_index, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(str(cell_data))
                    # 숫자를 오른쪽 정렬하여 삽입
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                    # 테이블 위젯에 항목을 설정
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

        # CSV 파일 읽기
        self.load_csv_data_2(file_path)

    def cell_double_clicked(self, row, column):
        item = self.ui.tableWidget_2.item(row, column)
        if item:
            I_Cell = item.text()  # 더블클릭한 셀의 값을 I_Cell 변수에 저장
            #print(I_Cell)  # I_Cell 변수의 값을 출력

    def load_csv_data_2(self, file_path):
        try:
            # pandas를 사용하여 CSV 파일 읽기
            df = pd.read_csv(file_path)

            # 테이블 위젯 선택
            table_widget_2 = getattr(self.ui, self.table_name)

            # 행과 열의 수 설정
            table_widget_2.setRowCount(len(df))
            table_widget_2.setColumnCount(len(df.columns))

            # CSV 파일의 헤더를 테이블 헤더로 설정
            table_widget_2.setHorizontalHeaderLabels(df.columns)

            # 데이터를 테이블 위젯에 삽입
            for row_index, row_data in enumerate(df.values):
                for col_index, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(str(cell_data))
                    # 숫자를 오른쪽 정렬하여 삽입
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                    # 테이블 위젯에 항목을 설정
                    table_widget_2.setItem(row_index, col_index, item)

        except Exception as e:
            print(f"Error loading CSV file: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
