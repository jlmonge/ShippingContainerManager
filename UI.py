from cgitb import text
from sqlite3 import Time
from os.path import exists
import sys
from util import *
import time
from grid import Grid
from anim import *
import load
from main import balance_ship
import recovery
import Ship

from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 

from PyQt5.QtWidgets import (
   QApplication,
   QLabel,
   QMainWindow,
   QStatusBar,
   QPushButton,
   QVBoxLayout,
   QWidget,
   QGridLayout,
   QFormLayout,
   QLineEdit,
   QStackedWidget,
   QHBoxLayout,
   QRadioButton,
   QMessageBox,
   QScrollArea,
   QButtonGroup,
   QMessageBox,
   QSizePolicy,
   QInputDialog,
   QPlainTextEdit,
   QListWidget,
   QListWidgetItem,
   QListView,
   QFileDialog,
   QProgressBar,
)

from PyQt5.QtCore import Qt

from PyQt5.QtGui import QIcon
 
'''
PyQt5 install instructions
 
(optional) 1. python3 -m venv pyqtenv
(optional) 2. source pyqtenv/bin/activate
3. pip3 install pyqt5
'''
 
'''
window.setGeometry(100, 100, 1600, 900)
window.move(60, 15)
helloMsg = QLabel('Login', parent=window)
'''

class UI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
 
        # window config
        self.title = "Keogh's Yard Portage"
        self.width = 1440
        self.height = 880
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
        self.onloadListNames = []
        self.onloadListWts = []
        self.moves = []
        self.animOp = 0
        
        self.loadRScrollBox = QListWidget()
       
        # determine if program was unexpectedly shutdown by power outage
        self.cont = False

        # pages config
        self.initUI()
    
    def initUI(self):
        # calculation page
        self.calcPage = QWidget()
        layout2 = QVBoxLayout(self.calcPage)
        progLabel = QLabel(self.calcPage)
        progLabel.setText('Calculating...')
        progLabel.setAlignment(Qt.AlignCenter)
        self.progBar = QProgressBar(self.calcPage)
        self.progBar.setMaximum(100)
        self.progBtn = QPushButton('Proceed')
        self.progBtn.clicked.connect(lambda: self.animFunc(cont=False))
        layout2.addWidget(progLabel)
        layout2.addWidget(self.progBar)
        layout2.addWidget(self.progBtn)

        # main menu
        self.menuPage = QWidget()
        layout0 = QGridLayout(self.menuPage)
        loginBtn0 = self.loginBtn()
        loadBtn = QPushButton('Onload/Offload')
        loadBtn.clicked.connect(lambda: self.uploadHelper(jobType=0))
        balanceBtn = QPushButton('Balance')
        balanceBtn.clicked.connect(lambda: self.uploadHelper(jobType=1))
        contBtn = QPushButton('Continue', enabled=True)
        contBtn.clicked.connect(lambda: self.animFunc(cont=self.cont))
        layout0.addWidget(loginBtn0)
        layout0.addWidget(loadBtn)
        layout0.addWidget(balanceBtn)
        layout0.addWidget(contBtn)

        # onloading / offloading page
        self.loadPage = QWidget()
        self.loadPage.setMinimumWidth(1300)
        layout1 = QHBoxLayout(self.loadPage)
        theLeft = QVBoxLayout() #login, back, compute buttons
        theLeft.addWidget(QWidget(), 4)
        loginBtn1 = self.loginBtn()
        theLeft.addWidget(loginBtn1, 1)
        backBtn = QPushButton('Back to Menu')
        backBtn.clicked.connect(self.menuConfirmPopup)
        theLeft.addWidget(backBtn, 1)
        theLeft.addWidget(QWidget(), 3)
        computeBtn = QPushButton('Compute Solution')
        computeBtn.clicked.connect(self.computeConfirmPopup)
        theLeft.addWidget(computeBtn, 1)
        theLeft.addWidget(QWidget(), 10)
        self.theCenter = QVBoxLayout() #grid and title of page   
        unloadLabel = QLabel("Unload")
        # unloadLabel.setStyleSheet("QLabel {background-color: red;}")
        unloadLabel.setFont(QFont('Arial', 30))
        unloadLabel.setMaximumSize(800,50)
        unloadLabel.setAlignment(Qt.AlignCenter)
        self.theCenter.addWidget(unloadLabel, Qt.AlignCenter)
        theRight = QVBoxLayout() #name and containers to onload
        addOnlBtn = QPushButton('Add container to onload...')
        addOnlBtn.clicked.connect(self.addToOnloadList)
        theRight.addWidget(addOnlBtn, 4)
        theScrollArea = QScrollArea()
        theScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        theScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        theScrollLayout = QVBoxLayout(theScrollArea)
        theScrollArea.setWidget(theScrollLayout.widget())
        loadList = self.loadRScrollBox
        loadList.itemClicked.connect(self.removeFromOnloadList)
        theScrollLayout.addWidget(loadList)
        loadList.update()
        theRight.addWidget(theScrollArea, 12)
        theRight.addWidget(QWidget(), 2)
        layout1.addLayout(theLeft, 1)
        layout1.addLayout(self.theCenter, 5)
        layout1.addLayout(theRight, 2)
        layout1.setSpacing(10)
 
        # animation page
        self.animPage = QWidget()
        self.animLayout = QGridLayout(self.animPage)
        loginBtn3 = self.loginBtn()
        self.animDesc = QLabel(self.animPage)
        opBtn = QPushButton('Complete operation')
        opBtn.clicked.connect(self.completeFunc) # change completeFunc to progress anim when this is clicked
        self.animLayout.addWidget(loginBtn3, 0, 0)
        self.animLayout.addWidget(self.animDesc, 2, 0)
        self.animLayout.addWidget(opBtn, 3, 0)

        # job completion page
        self.completePage = QWidget()
        layout4 = QGridLayout(self.completePage)
        progLabel = QLabel(self.completePage)
        progLabel.setText('All operations have been completed')
        progLabel.setAlignment(Qt.AlignCenter)
        okBtn = QPushButton('OK')
        okBtn.clicked.connect(self.menuFunc)
        layout4.addWidget(progLabel)
        layout4.addWidget(okBtn)

        # configuring the widget stack
        self.widgetStack = QStackedWidget(self)
        self.widgetStack.setFixedSize(self.width, self.height)
        self.widgetStack.addWidget(self.menuPage)       #0
        self.widgetStack.addWidget(self.loadPage)       #1
        self.widgetStack.addWidget(self.calcPage)       #2
        self.widgetStack.addWidget(self.animPage)  #3
        self.widgetStack.addWidget(self.completePage)   #4

        # go to the login page
        self.loginFunc()

    def loginBtn(self):
        btn = QPushButton('Login')
        btn.clicked.connect(self.loginFunc)
        return btn

    def menuConfirmPopup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Confirmation")
        msg.setText("Are you sure you want to go back to the main menu?")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        msg.setEscapeButton(QMessageBox.Cancel)
        if (msg.exec_() == 1024): #1024 = QMessageBox.OK
            self.menuFunc()
        


    def computeConfirmPopup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Confirmation")
        msg.setText("Are you sure you want to begin computing the sequence of moves? You will be unable to make any changes when you do.")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        msg.setEscapeButton(QMessageBox.Cancel)
        if (msg.exec_() == 1024):
            print("BEGINNING COMPUTATION", flush = True)
            offload = self.grid.getSelectedContainers()
            onload = list(zip(self.onloadListWts, self.onloadListNames))
            print("OFFLOADED:", offload)
            print("ONLOADED: ", onload)
            self.calcFunc(0, offload, onload)

    def addToOnloadList(self):
        cNm = ''
        while cNm.strip() == '':
            cNm, ok1Pressed = QInputDialog.getText(self, "Onload Container", "Enter container contents:")
            if cNm.strip() != '' and ok1Pressed: 
                cWt, ok2Pressed = QInputDialog.getInt(self, "Onload Container", "Enter container weight:", 0, 0, 99999, 1)
            else:
                err = self.errBox("Description must contain at least 1 non-whitespace character.")
                err.exec_()
        if ok2Pressed:
            self.onloadListNames.append(str(cNm))
            self.onloadListWts.append(cWt)
            item = QListWidgetItem()
            item.setText(str(self.onloadListNames.index(cNm) + 1) + ". " + cNm + "   Wt = " + str(cWt))
            self.loadRScrollBox.addItem(item)

    def removeFromOnloadList(self):
            currItem = self.loadRScrollBox.currentItem()
            msg2 = QMessageBox()
            msg2.setWindowTitle("Confirmation")
            msg2.setText("Are you sure you want to remove the following container from the onload list?\n" + currItem.text())
            msg2.setIcon(QMessageBox.Information)
            msg2.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg2.setDefaultButton(QMessageBox.Cancel)
            msg2.setEscapeButton(QMessageBox.Cancel)
            if (msg2.exec_() == 1024):
                ind = int(currItem.text()[0]) - 1
                self.onloadListNames.remove(self.onloadListNames[ind])
                self.onloadListWts.remove(self.onloadListWts[ind])
                gbye = self.loadRScrollBox.takeItem(ind)
                del gbye
                #print("Removed!", flush = True)
                for i in range (0, len(self.onloadListNames)):
                    self.loadRScrollBox.setCurrentRow(i)
                    self.loadRScrollBox.currentItem().setText(str(i+1) + ". " + self.onloadListNames[i] + "   Wt = " + str(self.onloadListWts[i]))
                #print("List refreshed!", flush = True)
   
    def contFunc(self):
        pass
 
    def errBox(self, text):
        d = QMessageBox()
        d.setIcon(QMessageBox.Critical)
        d.setText(text)
        d.setWindowTitle("Error")
        d.setStandardButtons(QMessageBox.Ok)
        return d

    # jobType 0 = offload/onload, 1 = balance
    def uploadHelper(self, jobType):
        self.fileName = QFileDialog.getOpenFileName(self, "Open File", "{0}\{1}".format(os.environ['USERPROFILE'], 'Desktop'), "Text files (*.txt)")[0]
        if self.fileName:
            print(self.fileName)
            self.containers = parseManifest(self.fileName)
            self.grid = Grid(self.containers)
            if self.containers == False:
                err = self.errBox("The file is not a valid manifest.")
                err.exec_()
            else:
                if jobType == 0:
                    self.loadFunc()
                else:
                    self.calcFunc(jobType=1)

    def loginFunc(self):
        name = ''
        while name == '':
            name, okPressed = QInputDialog.getText(self, "Login", "Name:", QLineEdit.Normal, "")
            if okPressed and name != '':
                self.setWindowTitle(self.title + f" ({name})")
 
    def menuFunc(self):
        self.widgetStack.setCurrentIndex(0)
        self.animOp = 0
        print("clearing load lists")
        self.onloadListNames.clear()    # clear list
        self.onloadListWts.clear()      # clear list
        self.loadRScrollBox.clear()     # clear QListWidget

    def loadFunc(self):
        self.widgetStack.setCurrentIndex(1)
        if self.theCenter.itemAt(1):
            self.theCenter.removeWidget(self.grid)
            self.grid.deleteLater()
        self.grid.setMaximumSize(800, 400)
        self.theCenter.addWidget(self.grid)


    '''
    Input: job type (0 for unload/offload, 1 for balance)
    '''
    def calcFunc(self, jobType, offload=None, onload=None):
        self.grid.colorWhite()
        self.widgetStack.setCurrentIndex(2)
        self.progBar.reset()
        moves = []
        
        if self.moves:
            self.moves.clear()
        self.progBtn.setEnabled(False)
        complete = False
        if jobType == 0: # offload/onload (from load.py)
            moves, complete = load.solve(self.containers, offload, onload)
            print(moves)
            for move in moves:
                if move[0] == None:
                    continue
                elif type(move[0][1]) is str: # dealing with onload
                    self.moves.append(((8,1), move[2][0], move[3]))
                else: # dealing with offload
                    self.moves.append((move[0], move[2], move[3]))
        else: # balance
            ship = Ship.Ship()
            ship.from_manifest(self.fileName)
            solution = balance_ship(ship)
            self.moves = solution.get_moves()
            for move in self.moves:
                move[0][0] += 1
                move[0][1] += 1
                move[1][0] += 1

        print(self.moves)
        for i in range(100):
            time.sleep(0.01)
            if complete != True and i < 99:
                self.progBar.setValue(i+1)
            else:
                self.progBar.setValue(100)
            QApplication.processEvents()
        self.progBtn.setEnabled(True)
            

    def animFunc(self, cont):
        self.widgetStack.setCurrentIndex(3)
        self.completeFunc()
        
    def completeFunc(self):
        if self.animOp < len(self.moves):
            initPos = self.moves[self.animOp][0]
            finalPos = self.moves[self.animOp][1]
            time = self.moves[self.animOp][2]
            if self.animLayout.itemAtPosition(1, 0):
                self.animLayout.removeWidget(self.animWidget)
                self.animWidget.deleteLater()
            self.animGrid = AnimatedGrid(self.grid, initPos, finalPos) # get actual pos from algorithm
            self.animWidget = QWidget(self.animPage)
            self.animWidget.setLayout(self.animGrid)
            self.animWidget.setFixedWidth(self.width)
            self.animDesc.setText(f"Operation {self.animOp + 1}/{len(self.moves)}: {initPos} to {finalPos} [{time} min]")

            self.animLayout.addWidget(self.animWidget, 1, 0)
            self.animOp = self.animOp + 1
        else:
            self.endFunc()

    def endFunc(self):
        self.widgetStack.setCurrentIndex(4)
        filename = writeOutboundManifest(self.containers, self.fileName)
        #recovery.rfileUpdate(2, filename, [], [], [], self.moves, self.currMove)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("QLineEdit, QPushButton, QLabel { font-size: 24px; }")
    if not sys.platform.startswith('win32'):
        msgbox = QMessageBox()
        msgbox.setIcon(QMessageBox.Critical)
        msgbox.setText("Incompatible Operating System")
        msgbox.setWindowTitle("Error")
        msgbox.setStandardButtons(QMessageBox.Ok)
        msgbox.exec_()
    else:
        ui = UI()
        ui.show()
        sys.exit(app.exec_())