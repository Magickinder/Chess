from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt

import ChessEngine

class ChoiceWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._initMainWindow()
        self.Layout()
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.show()
        self.chosen = 'Q'
        print(self.chosen)

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent == Qt.Key_Escape:
            pass

    def _initMainWindow(self):
        self.setWindowTitle('Promotion')
        self.setFixedSize(250, 150)
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

    def chooseBishop(self):
        self.chosen = 'B'
        self.close()

    def chooseKnight(self):
        self.chosen = 'N'
        self.close()

    def chooseRook(self):
        self.chosen = 'R'
        self.close()

    def chooseQueen(self):
        self.chosen = 'Q'
        self.close()

    def Layout(self):
        layout = QVBoxLayout()
        layoutgorny = QHBoxLayout()
        layoutdolny = QHBoxLayout()
        checkBoxes = QGroupBox()
        checkBoxes.setTitle("Wybierz figure")
        BishopButton = QPushButton("Bishop")
        KnightButton = QPushButton("Knight")
        RookButton = QPushButton("Rook")
        QueenButton = QPushButton("Queen")
        layoutdolny.addWidget(BishopButton)
        layoutdolny.addWidget(KnightButton)
        layoutdolny.addWidget(RookButton)
        layoutdolny.addWidget(QueenButton)

        text = QLabel('Wybierz figurę')
        text.setAlignment(Qt.AlignCenter)
        layout.addWidget(text)

        Bishop = QLabel()
        Bishop.setScaledContents(True)
        BishopMapa = QPixmap("Images/wB.png")
        Bishop.setPixmap(BishopMapa)
        layoutgorny.addWidget(Bishop)

        Knight = QLabel()
        Knight.setScaledContents(True)
        KnightMapa = QPixmap("Images/wN.png")
        Knight.setPixmap(KnightMapa)
        layoutgorny.addWidget(Knight)

        Rook = QLabel()
        Rook.setScaledContents(True)
        RookMapa = QPixmap("Images/wR.png")
        Rook.setPixmap(RookMapa)
        layoutgorny.addWidget(Rook)

        Queen = QLabel()
        Queen.setScaledContents(True)
        QueenMapa = QPixmap("Images/wQ.png")
        Queen.setPixmap(QueenMapa)
        layoutgorny.addWidget(Queen)

        layout.addLayout(layoutgorny)
        layout.addLayout(layoutdolny)
        BishopButton.clicked.connect(self.chooseBishop)
        KnightButton.clicked.connect(self.chooseKnight)
        RookButton.clicked.connect(self.chooseRook)
        QueenButton.clicked.connect(self.chooseQueen)

        self.generalLayout.addLayout(layout)
