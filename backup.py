import time
from aws_backup import *
from main_window import *

if __name__ == '__main__':
    if not (os.path.exists('user')):
        while(True):
            app = QApplication(sys.argv)
            ex = Backup()
            app.exec_()
            var_list = ex.getpass()
            if(len(var_list)==4): 
                add_update_new_device(var_list)
    while(True):
        update_device()
        time.sleep(20)
