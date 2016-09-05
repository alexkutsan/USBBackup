from PyQt5 import QtCore
from PyQt5.QtWidgets import  QApplication
import sys

def main():
	app = QApplication(sys.argv)
	fs_watcher = QtCore.QFileSystemWatcher()
	fs_watcher.addPath("/etc/mtab")
	fs_watcher.fileChanged.connect(lambda : print("foo"))
	sys.exit(app.exec_())

main()