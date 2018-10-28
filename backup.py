from aws_backup import *
from main_window import *

if __name__ == '__main__':
    if not (os.path.isfile('user')):
        while(True):
            app = QApplication(sys.argv)
            ex = Backup()
            app.exec_()
            #sys.exit(app.exec_())
            var_list = ex.getpass()
            print(var_list)
            
            print("yes")
            #sys.exit(app.exec_())
            if(len(var_list)==4): 
                add_update_new_device(var_list)
                while(True):
                    update_device()
                    time.sleep(60)
