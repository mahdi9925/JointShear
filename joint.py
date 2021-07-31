import math
import os
import sys

from design import Ui_MainWindow
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QIcon, QPixmap, QRegExpValidator
from PyQt5.QtWidgets import QApplication, QLineEdit, QMainWindow, QMessageBox


class Persenolize(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
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
        self.start.clicked.connect(self.next_tab)
        self.show()

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

    def next_tab(self):
        cur_index = self.tabWidget.currentIndex()
        if cur_index < len(self.tabWidget) - 1:
            self.tabWidget.setCurrentIndex(cur_index + 1)

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

        count = 0
        for child in self.widget.findChildren(QLineEdit):
            count += 1
            if len(child.text()) == 0:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("There is a empty row.")
                msg.setInformativeText(
                    "All rows must have a value.\nYou can look at the details to correct your mistake."
                )
                msg.setWindowTitle("Error")
                msg.setDetailedText(f'row {count+4} is empty!')
                msg.setStandardButtons(QMessageBox.Retry | QMessageBox.Cancel)
                btn = msg.exec_()
                if btn == QMessageBox.Retry:
                    os.execl(sys.executable, sys.executable, *sys.argv)
                else:
                    sys.exit()
                # os.system('clear')
            else:
                pass

        def base_formula(coefficient):
            # os.system('clear')
            nonlocal b_beam2
            nonlocal b_beam1

            if b_beam1 > b_column1 and b_beam2 > b_column1:
                b_beam2 = b_beam1 = float(self.b_column1.text())
                self.log.append('b column1 = b beam1 = b beam2\n')

            elif b_beam1 > b_column1:
                b_beam1 = float(self.b_column1.text())
                self.log.append('b column1 = b beam1\n')

            elif b_beam2 > b_column1:
                b_beam2 = float(self.b_column1.text())
                self.log.append('b column1 = b beam2\n')
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
            self.log.append(f"φVn = {str(phi_Vn)} (tonf)")
            self.log.append(f'Aj = {str(Aj)} (cm2)')
            return float(round(formula * 1e-3, 2))

        def calculate_mpr_1Top():
            reslut1 = A_s1Top * d_beam1 * alpha * f_y
            reslut2 = (0.59 * f_y * alpha * A_s1Top) / \
                (b_beam1 * d_beam1 * f_c)
            mpr1_top = round((reslut1 * (1 - reslut2)) * 1e-3, 3)
            return mpr1_top

        def calculate_mpr_2Top():
            reslut1 = A_s2Top * d_beam2 * alpha * f_y
            reslut2 = (0.59 * f_y * alpha * A_s2Top) / \
                (b_beam2 * d_beam2 * f_c)
            mpr2_top = round((reslut1 * (1 - reslut2)) * 1e-3, 3)
            return mpr2_top

        def calculate_mpr_1Btm():
            reslut1 = A_s1Btm * d_beam1 * alpha * f_y
            reslut2 = (0.59 * f_y * alpha * A_s1Btm) / \
                (b_beam1 * d_beam1 * f_c)
            mpr1_btm = round((reslut1 * (1 - reslut2)) * 1e-3, 3)
            return mpr1_btm

        def calculate_mpr_2Btm():
            reslut1 = A_s2Btm * d_beam2 * alpha * f_y
            reslut2 = (0.59 * f_y * alpha * A_s2Btm) / \
                (b_beam2 * d_beam2 * f_c)
            mpr2_btm = round((reslut1 * (1 - reslut2)) * 1e-3, 3)
            return mpr2_btm

        def calculate_V1():
            reslut1 = max(A_s1Btm + A_s2Top, A_s1Top + A_s2Btm)
            result2 = reslut1 * alpha * f_y
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
                pixmap = QPixmap('static/ng.jpg')
                emoji = QPixmap('static/notOK.png')
                self.label_37.setPixmap(pixmap)
                self.label_39.setPixmap(emoji)
                self.label_39.adjustSize()
                self.label_37.adjustSize()

            else:
                self.ratio.setText(f'{ratio} OK')
                self.ratio.setStyleSheet('QLabel {color: #228B22;}')
                pixmap = QPixmap('static/ok.jpg')
                emoji = QPixmap('static/Ok.png')
                self.label_37.setPixmap(pixmap)
                self.label_39.setPixmap(emoji)
                self.label_39.adjustSize()
                self.label_37.adjustSize()

        A_s1Top, A_s1Btm, d_beam1, b_beam1, f_y, f_c, h_beam1 = float(
            A_s1Top), float(A_s1Btm), float(d_beam1), float(b_beam1), float(
                f_y), float(f_c), float(h_beam1)

        A_s2Top, A_s2Btm, d_beam2, b_beam2, h_beam2 = float(A_s2Top), float(
            A_s2Btm), float(d_beam2), float(b_beam2), float(h_beam2)

        L_col1, L_col2, h_column1, x, b_column1 = float(L_col1), float(
            L_col2), float(h_column1), float(x), float(b_column1)

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
            self.log.append(
                f"Vn = 5.3 √F'c * Aj\nVn = {base_formula(5.3)} (tonf)")

        elif column_is == 'continuous' and beam1_2 == 'continuous' and joint == 'not confined' or column_is == 'continuous' and beam1_2 == 'other' and joint == 'confined' or column_is == 'other' and beam1_2 == 'continuous' and joint == 'confined':
            self.log.append(
                f"Vn = 4.0 √F'c * Aj\nVn = {base_formula(4.0)} (tonf)")

        elif column_is == 'continuous' and beam1_2 == 'other' and joint == 'not confined' or column_is == 'other' and beam1_2 == 'continuous' and joint == 'not confined' or column_is == 'other' and beam1_2 == 'other' and joint == 'confined':
            self.log.append(
                f"Vn = 3.2 √F'c * Aj\nVn = {base_formula(3.2)} (tonf)")

        elif column_is == 'other' and beam1_2 == 'other' and joint == 'not confined':
            self.log.append(
                f"Vn = 2.12 √F'c * Aj\nVn = {base_formula(2.12)} (tonf)")

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


app = QApplication(sys.argv)
main = Persenolize()
sys.exit(app.exec())
