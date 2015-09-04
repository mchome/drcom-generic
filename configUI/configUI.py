#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui
import config

class Window(QtGui.QMainWindow):
	def __init__(self):
		super(Window, self).__init__()
		self.initUI()

	def initUI(self):
		self.textEdit = QtGui.QTextEdit()
		self.setCentralWidget(self.textEdit)
		self.statusBar()

		openFile1 = QtGui.QAction(QtGui.QIcon('open.png'), u'打开d版抓包', self)
		openFile1.setShortcut('Ctrl+1')
		openFile1.setStatusTip(u'打开d版抓包')
		openFile1.triggered.connect(lambda: self.showDialog('d'))

		openFile2 = QtGui.QAction(QtGui.QIcon('open2.png'), u'打开p版抓包', self)
		openFile2.setShortcut('Ctrl+2')
		openFile2.setStatusTip(u'打开p版抓包')
		openFile2.triggered.connect(lambda: self.showDialog('p'))

		exit = QtGui.QAction(QtGui.QIcon('exit.png'), u'退出', self)
		exit.setShortcut('Ctrl+Q')
		exit.setStatusTip(u'退出')
		exit.triggered.connect(self.close)


		menubar = self.menuBar()
		fileMenu = menubar.addMenu(u'文件')
		fileMenu.addAction(openFile1)
		fileMenu.addAction(openFile2)
		fileMenu.addAction(exit)

		self.setGeometry(300, 300, 350, 300)
		self.setWindowTitle(u'drcom 配置器')
		self.setWindowIcon(QtGui.QIcon('favicon.ico'))
		self.show()

	def showDialog(self, method):
		fpath = QtGui.QFileDialog.getOpenFileName(self, u'打开文件', 
				'')
		if method == 'd':
			r = config.config_d(fpath)
			with open('drcom.conf', 'rb') as f:
				text = f.read()
				self.textEdit.setText(text)
			self.setStatusTip(r)
		elif method == 'p':
			r = config.config_p(fpath)
			with open('drcom.conf', 'rb') as f:
				text = f.read()
				self.textEdit.setText(text)
			self.setStatusTip(r)
		else:
			self.textEdit.setText('Error')

def main():
	app = QtGui.QApplication(sys.argv)
	ex = Window()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()