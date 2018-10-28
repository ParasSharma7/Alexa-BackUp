import sys
import threading
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, 
    QTextEdit, QGridLayout, QApplication, QPushButton)


class Backup(QWidget):
    
    def __init__(self):
        super(Backup,self).__init__()
        self.pass1=""
        self.initUI()

        
    def initUI(self):
        self.ID_key = QLabel('Access Key')
        self.access_key = QLabel('Secret Key')
        self.Bucket = QLabel('Bucket Name')
        self.Passcode = QLabel('Passcode')

        self.ID_keyEdit = QLineEdit()
        self.access_keyEdit = QLineEdit()
        self.BucketEdit = QLineEdit()
        self.PasscodeEdit = QLineEdit()
        self.ID_keyEdit.setEchoMode(QLineEdit.Password)
        self.access_keyEdit.setEchoMode(QLineEdit.Password)
        self.BucketEdit.setEchoMode(QLineEdit.Password)
        self.PasscodeEdit.setEchoMode(QLineEdit.Password)
        Submit = QPushButton("Submit")
        

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.ID_key, 1, 0)
        grid.addWidget(self.ID_keyEdit, 1, 1)

        grid.addWidget(self.access_key, 2, 0)
        grid.addWidget(self.access_keyEdit, 2, 1)

        grid.addWidget(self.Bucket, 3, 0)
        grid.addWidget(self.BucketEdit, 3, 1)
        
        grid.addWidget(self.Passcode, 4, 0)
        grid.addWidget(self.PasscodeEdit, 4, 1)
        
        grid.addWidget(Submit, 5, 1)
        
        self.setLayout(grid) 
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Back Up')    
        Submit.clicked.connect(self.on_click)
        self.show()

        
    def on_click(self, btn):
        self.pass1=[self.ID_keyEdit.text(), self.access_keyEdit.text(), self.BucketEdit.text(), self.PasscodeEdit.text()]
        if self.ID_keyEdit.text()!="" and self.access_keyEdit.text()!="" and self.BucketEdit.text()!="" and self.PasscodeEdit.text()!="" and len(self.PasscodeEdit.text())==8:
            self.close()

    def getpass(self):
        return self.pass1
    
