import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import PyQt5.QtGui


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.textfind = TextFind(parent=self)
        self.setCentralWidget(self.textfind)

        openFile = QtWidgets.QAction('openfile', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('open new file')
        openFile.triggered.connect(self.op)

        bar = self.menuBar()
        # 파일 메뉴 설정하는 것
        filemenu = bar.addMenu('File')
        close_action = QtWidgets.QAction('Close', self)
        filemenu.addAction(openFile)
        filemenu.addAction(close_action)

        close_action.triggered.connect(self.close)

    def op(self):  # 파일 불러서 그 안에 있는 내용을 함수에 보내고 그 리턴값을 표시하는 것
        name = QtWidgets.QFileDialog.getOpenFileName(self, 'openfile', './')

        if name[0]:
            highlightTextEdit(name[0], ["main()", "virus", "hello"], self)  # 수정한곳


class TextFind(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        grid = QtWidgets.QGridLayout(self)
        self.table = QTableWidget(parent)
        self.setLayout(grid)  # 배열 짜는 부분 QList view와 Qtable view 를 사용함


        self.malwareTextBox = QtWidgets.QTextEdit()

        contents = ['사과', '바나나', '멜론']
        self.malwareListBox = QtWidgets.QListView(self)
        models = QStandardItemModel()
        for c in contents:
            models.appendRow(QStandardItem(c))
            self.malwareListBox.setModel(models)

        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setColumnCount(2)
        self.table.setRowCount(3) # 세로 설정
        self.table.setItem(0, 0,QTableWidgetItem("abc")) #앞의 자리가 행 뒤의 자리가 열
        self.table.setItem(1, 0, QTableWidgetItem("abcd"))
        self.table.setItem(0, 1, QTableWidgetItem("가"))
        self.table.setItem(1, 1, QTableWidgetItem("가나"))



        grid.addWidget(self.malwareTextBox, 1 , 1, 2, 1)
        grid.addWidget(self.malwareListBox, 1, 2)
        grid.addWidget(self.table, 2, 2)



        self.setWindowTitle('악성코드 부분은 어디일까')

    def abc(self):  # 이건 사람이 ctrl + c,v 를 했을 때 내용을 함수에 보내줄 부분\
        text = self.add1.toPlainText()
        highlightTextEdit_input(text ,["main()", "virus", "hello"], self)


class highlightSyntax(QSyntaxHighlighter):
    def __init__(self, listKeywords, parent=None):
        super(highlightSyntax, self).__init__(parent)
        brush = QBrush(Qt.green, Qt.SolidPattern)
        keyword = QTextCharFormat()
        keyword.setForeground(brush)  # 이거 글자 굵게 만드는 건데 잘 안됨
        keyword.setFontWeight(QFont.Bold)

        self.highlightingRules = [highlightRule(QRegExp(key), keyword, key)
                                  for key in listKeywords]

    def highlightBlock(self, text):

        for rule in self.highlightingRules:
            expression2 = rule.pattern2
            expression = rule.pattern
            index1 = expression.indexIn(text)

            while index1 >= 0:
                length = expression.matchedLength()
                self.setFormat(index1, length, rule.format)
                index1 = expression.indexIn(text, length + index1)

        self.setCurrentBlockState(0)


class highlightRule(object):
    def __init__(self, pattern, format, pattern2):
        self.pattern = pattern
        self.format = format
        self.pattern2 = pattern2


class highlightTextEdit(QTextEdit):
    def __init__(self, fileInput, listKeywords, main, parent=None):  # 수정한곳
        super(highlightTextEdit, self).__init__(parent)
        highlightSyntax(listKeywords, main.textfind.malwareTextBox)  # 수정한곳

        with open(fileInput, "r") as fInput:
            main.textfind.malwareTextBox.setText(fInput.read())  # 수정한곳


class highlightTextEdit_input(QTextEdit):
    def __init__(self, text, listKeywords, main, parent=None):  # 수정한곳
        super(highlightTextEdit_input, self).__init__(parent)
        highlightSyntax(listKeywords, main.textfind.malwareTextBox)  # 수정한곳
        main.textfind.malwareTextBox.setText(text)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()

    sys.exit(app.exec_())