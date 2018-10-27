from aws_backup import *
from main_window import *

if __name__ == '__main__':
	if !(os.path.isfile('user')):
		app = QApplication(sys.argv)
		ex = Backup()
		sys.exit(app.exec_())
		var_list = ex.pass1
		assert 1<0
		add_update_new_device()
	while(True):
		update_device()
		time.sleep(60)
