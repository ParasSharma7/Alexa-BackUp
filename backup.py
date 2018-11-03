import time
import os
from aws_backup import *
from main_window import *
import getpass
USER_NAME = getpass.getuser()

def add_to_startup():
    file_path = os.path.dirname(os.path.realpath(__file__))
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
    with open(bat_path + '\\' + "BackMeUpOnStartup.bat", "w+") as bat_file:
        bat_file.write('cd '+file_path+'\n')
        bat_file.write('python backup.py')

if __name__ == '__main__':
    if not (os.path.exists('user')):
        add_to_startup()
        while(True):
            app = QApplication(sys.argv)
            ex = Backup()
            app.exec_()
            var_list = ex.getpass()
            if(len(var_list)==4): 
                add_update_new_device(var_list)
                while(True):
                    try:
                        update_device()
                        time.sleep(20)
                    except:
                        print('Unable to connect to the Internet. Retrying...')
                        time.sleep(20)
    else:
        while(True):
            try:
                update_device()
                time.sleep(20)
            except:
                print('Unable to connect to the Internet. Retrying...')
                time.sleep(20)