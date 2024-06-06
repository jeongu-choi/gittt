import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from yoni import Ui_MainWindow  # 생성된 파이썬 파일의 이름에 따라 import 구문이 달라질 수 있습니다.
#from secondwindow import Ui_Form
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.H_beam.clicked.connect(self.groupboxRadFunction)
        self.ui.I_beam.clicked.connect(self.groupboxRadFunction)

        self.ui.Bridge_Length.returnPressed.connect(self.print_Bridge_Length)

    def groupboxRadFunction(self):
        if self.ui.H_beam.isChecked():
            #self.second_window = SecondWindow()
            self.second_window.show()
        elif self.ui.I_beam.isChecked():
            print("I_beam Checked")

    def print_Bridge_Length(self):
        # self.lineedit이름.text()
        # Lineedit에 있는 글자를 가져오는 메서드
        print(self.ui.Bridge_Length.text())

#class SecondWindow(QWidget):
    #def __init__(self):
        #super().__init__()
        #self.ui = Ui_Form()
        #self.ui.setupUi(self)
        #self.setWindowTitle("Second Window")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())



