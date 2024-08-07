import math
import sys

from shortcut import Ui_Dialog
from design import Ui_MainWindow
from PyQt5.QtCore import QRegExp, Qt, QEvent, QSettings
from PyQt5.QtGui import QIcon, QPixmap, QRegExpValidator
from PyQt5.QtWidgets import QApplication, QLineEdit, QMainWindow, QMessageBox, QDialog


class Persenolize(QMainWindow, Ui_MainWindow):
    def __init__(self):
        # super().__init__()
        super(Persenolize, self).__init__()
        self.initUI()

    def initUI(self):
        self.setupUi(self)
        self.setWindowIcon(QIcon("icon.ico"))

        self.setFixedSize(1537, 774)
        validator = QRegExpValidator(QRegExp("[0-9.]+"))
        self.f_y.setValidator(validator)
        self.f_c.setValidator(validator)
        self.L_col1.setValidator(validator)
        self.L_col2.setValidator(validator)
        self.x.setValidator(validator)
        self.b_column1.setValidator(validator)
        self.h_column1.setValidator(validator)
        self.b_beam1.setValidator(validator)
        self.h_beam1.setValidator(validator)
        self.d_beam1.setValidator(validator)
        self.b_beam2.setValidator(validator)
        self.h_beam2.setValidator(validator)
        self.d_beam2.setValidator(validator)
        self.A_s1Top.setValidator(validator)
        self.A_s1Btm.setValidator(validator)
        self.A_s2Top.setValidator(validator)
        self.A_s2Btm.setValidator(validator)

        self.column_is.currentTextChanged.connect(
            self.disable_enable_column_is)
        self.beam1_2.currentTextChanged.connect(self.disable_enable_beam1_2)

        self.start.clicked.connect(self.calculate)
        self.show()

        ShortcutWindow()

    # when user press Enter cursor move to next line edit
    def event(self, event):
        if event.type() == QEvent.KeyPress and event.key() in (
            Qt.Key_Enter,
            Qt.Key_Return,
        ):
            self.focusNextPrevChild(True)
        return super().event(event)

    def disable_enable_beam1_2(self):
        if self.beam1_2.currentText().lower() == 'other':
            self.b_beam2.setEnabled(False)
            self.h_beam2.setEnabled(False)
            self.d_beam2.setEnabled(False)
            self.A_s2Top.setEnabled(False)
            self.A_s2Btm.setEnabled(False)

            self.b_beam2.setText('0')
            self.h_beam2.setText('0')
            self.d_beam2.setText('0')
            self.A_s2Top.setText('0')
            self.A_s2Btm.setText('0')
            self.mpr_2_top.setText('0')
            self.mpr_2_btm.setText('0')
        else:
            self.b_beam2.setEnabled(True)
            self.h_beam2.setEnabled(True)
            self.d_beam2.setEnabled(True)
            self.A_s2Top.setEnabled(True)
            self.A_s2Btm.setEnabled(True)
            self.mpr_2_top.setText('')
            self.mpr_2_btm.setText('')

    def disable_enable_column_is(self):
        if self.column_is.currentText().lower() == 'other':
            self.L_col2.setEnabled(False)
            self.L_col2.setText('0')
        else:
            self.L_col2.setEnabled(True)

    def calculate(self):
        frame_type, column_is, beam1_2, joint = self.frame_type.currentText(
        ).lower(), self.column_is.currentText().lower(
        ), self.beam1_2.currentText().lower(), self.joint.currentText().lower(
        )

        A_s1Top, A_s1Btm, d_beam1, b_beam1, f_y, f_c, h_beam1 = self.A_s1Top.text(
        ), self.A_s1Btm.text(), self.d_beam1.text(), self.b_beam1.text(
        ), self.f_y.text(), self.f_c.text(), self.h_beam1.text()

        A_s2Top, A_s2Btm, d_beam2, b_beam2, h_beam2 = self.A_s2Top.text(
        ), self.A_s2Btm.text(), self.d_beam2.text(), self.b_beam2.text(
        ), self.h_beam2.text()

        L_col1, L_col2, h_column1, x, b_column1 = self.L_col1.text(
        ), self.L_col2.text(), self.h_column1.text(), self.x.text(
        ), self.b_column1.text()

        # * ToDo: Resize picture and mpr labels in output tab

        def next_tab():
            cur_index = self.tabWidget.currentIndex()
            if cur_index < len(self.tabWidget) - 1:
                self.tabWidget.setCurrentIndex(cur_index + 1)

        def base_formula(coefficient):
            nonlocal b_beam2
            nonlocal b_beam1

            if b_beam1 > b_column1 and b_beam2 > b_column1:
                b_beam2 = b_beam1 = float(self.b_column1.text())
            elif b_beam1 > b_column1:
                b_beam1 = float(self.b_column1.text())
            elif b_beam2 > b_column1:
                b_beam2 = float(self.b_column1.text())
            else:
                pass

            if b_beam2 > 0:
                av_beam1_2 = (b_beam2 + b_beam1) / 2

            elif b_beam1 == 0:
                av_beam1_2 = (b_beam2 + b_beam2) / 2

            elif b_beam2 == 0:
                av_beam1_2 = (b_beam1 + b_beam1) / 2

            else:
                pass

            if beam1_2 == 'continuous':
                if b_beam1 == b_column1 and b_beam2 == b_column1 or b_beam1 > b_column1 and b_beam2 > b_column1:
                    result1 = av_beam1_2 + h_column1
                    result2 = min(result1, b_column1)
                    Aj = result2 * h_column1

                elif b_beam1 < b_column1 and b_beam2 < b_column1:
                    result1 = (b_beam1 + (2 * x)) + (b_beam2 + (2 * x))
                    Aj = (result1 / 2) * h_column1

                elif b_beam1 > b_column1 and b_beam2 < b_column1:
                    result1 = (b_beam2 + b_column1) / 2
                    Aj = result1 * h_column1

                elif b_beam1 < b_column1 and b_beam2 > b_column1:
                    result1 = (b_beam1 + b_column1) / 2
                    Aj = result1 * h_column1

                elif b_beam1 < b_column1 and b_beam2 == b_column1 and x >= 0:
                    result1 = (b_beam1 + (2 * x) + b_beam2)
                    Aj = (result1 / 2) * h_column1

                elif b_beam2 < b_column1 and b_beam1 == b_column1 and x >= 0:
                    result1 = (b_beam2 + (2 * x) + b_beam1)
                    Aj = (result1 / 2) * h_column1

                else:
                    a_j1 = av_beam1_2 + h_column1
                    a_j2 = av_beam1_2 + (2 * x)
                    Aj = min(a_j1, a_j2) * h_column1

            else:
                a_j1 = av_beam1_2 + h_column1
                a_j2 = av_beam1_2 + (2 * x)
                Aj = min(a_j1, a_j2) * h_column1

            self.A_joint.setNum(Aj)
            formula = coefficient * math.sqrt(f_c) * Aj
            phi_Vn = round((formula * phi) * 1e-3)
            self.label_42.setNum(int(formula) * 1e-3)
            self.phi_v_n.setNum(phi_Vn)
            return float(round(formula * 1e-3, 2))

        def calculate_mpr_1Top():
            result1 = A_s1Top * d_beam1 * alpha * f_y
            result2 = (0.59 * f_y * alpha * A_s1Top) / \
                (b_beam1 * d_beam1 * f_c)
            mpr1_top = round((result1 * (1 - result2)) * 1e-3, 3)
            return mpr1_top

        def calculate_mpr_2Top():
            result1 = A_s2Top * d_beam2 * alpha * f_y
            result2 = (0.59 * f_y * alpha * A_s2Top) / \
                (b_beam2 * d_beam2 * f_c)
            mpr2_top = round((result1 * (1 - result2)) * 1e-3, 3)
            return mpr2_top

        def calculate_mpr_1Btm():
            result1 = A_s1Btm * d_beam1 * alpha * f_y
            result2 = (0.59 * f_y * alpha * A_s1Btm) / \
                (b_beam1 * d_beam1 * f_c)
            mpr1_btm = round((result1 * (1 - result2)) * 1e-3, 3)
            return mpr1_btm

        def calculate_mpr_2Btm():
            result1 = A_s2Btm * d_beam2 * alpha * f_y
            result2 = (0.59 * f_y * alpha * A_s2Btm) / \
                (b_beam2 * d_beam2 * f_c)
            mpr2_btm = round((result1 * (1 - result2)) * 1e-3, 3)
            return mpr2_btm

        def calculate_V1():
            result1 = max(A_s1Btm + A_s2Top, A_s1Top + A_s2Btm)
            result2 = result1 * alpha * f_y
            V1 = result2 * 1e-3
            return V1

        def calculate_Vc():
            result1 = mpr1_top + mpr2_btm
            result2 = mpr2_top + mpr1_btm
            result3 = max(result1, result2) * 2
            difinitive_result = result3 / (L_col2 + L_col1)
            return round(difinitive_result, 2)

        def calculate_Vu():
            Vc = float(self.v_c.text())
            return V1 - Vc

        def calculate_Ratio():
            phi_Vn, Vu = float(self.phi_v_n.text()), calculate_Vu()
            ratio = round(Vu / phi_Vn, 2)
            if ratio > 1:
                self.ratio.setText(f'{ratio} N.G.')
                self.ratio.setStyleSheet('QLabel {color: #FF0000;}')
                pixmap = QPixmap('ng.jpg')
                emoji = QPixmap('notOK.png')
                self.label_37.setPixmap(pixmap)
                self.label_39.setPixmap(emoji)
                self.label_39.adjustSize()
                self.label_37.adjustSize()

            else:
                self.ratio.setText(f'{ratio} OK')
                self.ratio.setStyleSheet('QLabel {color: #228B22;}')
                pixmap = QPixmap('ok.jpg')
                emoji = QPixmap('Ok.png')
                self.label_37.setPixmap(pixmap)
                self.label_39.setPixmap(emoji)
                self.label_39.adjustSize()
                self.label_37.adjustSize()
        try:
            A_s1Top, A_s1Btm, d_beam1, b_beam1, f_y, f_c, h_beam1 = float(
                A_s1Top), float(A_s1Btm), float(d_beam1), float(b_beam1), float(
                    f_y), float(f_c), float(h_beam1)

            A_s2Top, A_s2Btm, d_beam2, b_beam2, h_beam2 = float(A_s2Top), float(
                A_s2Btm), float(d_beam2), float(b_beam2), float(h_beam2)

            L_col1, L_col2, h_column1, x, b_column1 = float(L_col1), float(
                L_col2), float(h_column1), float(x), float(b_column1)

            next_tab()

        except ValueError:
            lineEdit_list = [
                'b_beam2', 'h_beam2', 'A_s2Top', 'A_s2Btm', 'A_s1Top', 'A_s1Btm', 'h_beam1', 'b_beam1', 'x', 'b_column1', 'h_column1', 'd_beam1', 'd_beam2', 'L_col1', 'L_col2', 'f_y', 'f_c'
            ]

            showLineEdit_list = [
                'b Beam2', 'h Beam2', 'As2 Top', 'As2 Bottom', 'As1 Top', 'As1 Bottom', 'h Beam1', 'b Beam1', 'x', 'b', 'h', 'd Beam1', 'd Beam2', 'L Column1', 'L Column2', 'Fy', "F'c"
            ]
            for child in self.frame.findChildren(QLineEdit):
                if len(child.text()) == 0:
                    for index, value in enumerate(lineEdit_list):
                        if child.objectName() == value:
                            Name = showLineEdit_list[index]
                            break

                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText(f'Row ( {Name} ) is empty!')
                    msg.setInformativeText(
                        "All rows must have a value.\nYou must correct your mistake."
                    )
                    msg.setWindowTitle("Error")
                    msg.setStandardButtons(QMessageBox.Retry)
                    btn = msg.exec_()
                    if btn == QMessageBox.Retry:
                        return
            return

        if frame_type == 'special':
            self.alpha.setNum(1.25)
            self.phi.setNum(0.85)

        elif frame_type == 'intermediate':
            self.alpha.setNum(1)
            self.phi.setNum(0.75)

        alpha, phi = float(self.alpha.text()), float(self.phi.text())

        if beam1_2 == 'other':
            mpr2_top = float(self.mpr_2_top.text())
            mpr2_btm = float(self.mpr_2_btm.text())
        else:
            mpr2_top = calculate_mpr_2Top()
            mpr2_btm = calculate_mpr_2Btm()
            self.mpr_2_top.setNum(mpr2_top)
            self.mpr_2_btm.setNum(mpr2_btm)

        if column_is == 'continuous' and beam1_2 == 'continuous' and joint == 'confined':
            self.formula.setText("5.3 √F'c * Aj")
            base_formula(5.3)

        elif column_is == 'continuous' and beam1_2 == 'continuous' and joint == 'not confined' or column_is == 'continuous' and beam1_2 == 'other' and joint == 'confined' or column_is == 'other' and beam1_2 == 'continuous' and joint == 'confined':
            self.formula.setText("4.0 √F'c * Aj")
            base_formula(4.0)

        elif column_is == 'continuous' and beam1_2 == 'other' and joint == 'not confined' or column_is == 'other' and beam1_2 == 'continuous' and joint == 'not confined' or column_is == 'other' and beam1_2 == 'other' and joint == 'confined':
            self.formula.setText("3.2 √F'c * Aj")
            base_formula(3.2)

        elif column_is == 'other' and beam1_2 == 'other' and joint == 'not confined':
            self.formula.setText("2.12 √F'c * Aj")
            base_formula(2.12)

        mpr1_top = calculate_mpr_1Top()
        self.mpr_1_top.setNum(mpr1_top)

        mpr1_btm = calculate_mpr_1Btm()
        self.mpr_1_btm.setNum(mpr1_btm)

        V1 = calculate_V1()
        self.v1.setNum(V1)

        if L_col2 == 0:
            self.v_c.setNum(0)
        else:
            Vc = calculate_Vc()
            self.v_c.setNum(Vc)

        Vu = calculate_Vu()
        self.v_u.setNum(Vu)

        calculate_Ratio()


class ShortcutWindow(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # ==> REMOVE TITLE BAR
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.ui.ok.clicked.connect(lambda: self.close())

        self.settings = QSettings('JointShear', 'shortcut')
        val = self.settings.value('checkBox')
        try:
            if val == 'false' or val == None:
                self.show()
        except:
            pass

    def closeEvent(self, event):
        self.settings.setValue('checkBox', self.ui.checkBox.isChecked())


app = QApplication(sys.argv)
main = Persenolize()
sys.exit(app.exec())
