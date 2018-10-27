import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, 
    QTextEdit, QGridLayout, QApplication, QPushButton)


class Backup(QWidget):
    
    def _init_(self):
        super()._init_()
        
        self.initUI()
        
        
    def initUI(self):
        
        self.ID_key = QLabel('ID Key')
        self.access_key = QLabel('Acess Key')
        self.Bucket = QLabel('Bucket Name')
        self.Passcode = QLabel('Passcode')

        self.ID_keyEdit = QLineEdit()
        self.access_keyEdit = QLineEdit()
        self.BucketEdit = QLineEdit()
        self.PasscodeEdit = QLineEdit()

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
        print(pass1)
        if self.ID_keyEdit.text()!="" and self.access_keyEdit.text()!="" and self.BucketEdit.text()!="" and self.PasscodeEdit.text()!="" and len(self.PasscodeEdit.text())==8:
            self.close()

    

if _name_ == '_main_':
    
    app = QApplication(sys.argv)
    ex = Backup()
    sys.exit(app.exec_())