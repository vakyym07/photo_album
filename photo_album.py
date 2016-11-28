from PyQt5.QtWidgets import \
    QWidget, QMainWindow, \
    QAction, QFormLayout, \
    QScrollArea, QDesktopWidget, \
    QGroupBox, QPushButton, \
    QVBoxLayout, QLabel, \
    QGridLayout, QHBoxLayout, \
    QLineEdit, QApplication, \
    qApp, QInputDialog, \
    QWidgetItem, QFileDialog
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import sys
import os
import os.path
import functools


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_widget = Photo()
        self.init_ui()

    def init_ui(self):
        self.resize(1024, 768)
        self.center()
        self.setWindowTitle('Photo Album')
        self.setCentralWidget(self.main_widget)
        self.create_menu()
        self.show()

    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        open_file = file_menu.addMenu('&Open')
        open_file_action = QAction('&Open', self)
        open_file_action.triggered.connect(lambda: self.main_widget.init_ui())
        open_file.addAction(open_file_action)

    # def createToolbar(self):
    #     nextAction = QAction(QIcon('right.png'), 'Next', self)
    #     nextAction.triggered.connect(self.getNextPhoto)
    #     prevAction = QAction(QIcon('left.png'), 'Prev', self)
    #     prevAction.triggered.connect(self.getPrevPhoto)
    #     searchAction = QAction(QIcon('lupa.gif'), 'Search', self)
    #     searchAction.triggered.connect(self.createSearchBox)
    #     toolbar = self.addToolBar('Toolbar')
    #     toolbar.addAction(prevAction)
    #     toolbar.addAction(nextAction)
    #     toolbar.addAction(searchAction)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def createSearchBox(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Search photo')
        if ok:
            self.searchPhoto(text)

    def getNextPhoto(self):
        if len(self.arrPhoto) != 0:
            if self.currentIndexPhoto != len(self.arrPhoto) - 1:
                self.currentIndexPhoto += 1
                self.show_photo(self.arrPhoto[self.currentIndexPhoto])

    def getPrevPhoto(self):
        if len(self.arrPhoto) != 0:
            if self.currentIndexPhoto > 0:
                self.currentIndexPhoto -= 1
                self.show_photo(self.arrPhoto[self.currentIndexPhoto])

    def searchPhoto(self, fname):
        if fname in self.arrPhoto:
            self.show_photo(self.arrPhoto[self.arrPhoto.index(fname)])
        else:
            self.showMessageBox('This photo has been found. Incorrect name.')

    def showMessageBox(self, message):
        reply = QMessageBox.question(self, 'Message', message, QMessageBox.Ok)


class Photo(QWidget):
    def __init__(self):
        self.arrPhoto = []
        self.currentIndexPhoto = 0
        self.grid = QGridLayout()
        super().__init__()

    def init_ui(self):
        self.open_path()
        self.setLayout(self.grid)

    def open_path(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        head_path, tail_path = os.path.split(fname)
        self.arrPhoto = [os.path.join(head_path, e)
                         for e in os.listdir(head_path)
                         if os.path.isfile(os.path.join(head_path, e))]
        self.currentIndexPhoto = self.arrPhoto.index(
            os.path.join(head_path, tail_path))
        self.show_photo(self.arrPhoto[self.currentIndexPhoto])
        self.show_all_photo()

    def show_all_photo(self):
        mygroupbox = QGroupBox("Images")
        myform = QFormLayout()
        scroll = QScrollArea()
        area_images = QVBoxLayout()
        if len(self.arrPhoto) != 0:
            for photo in self.arrPhoto:
                try:
                    pixmap = QPixmap(photo)
                    new_pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio,
                                               Qt.SmoothTransformation)
                    label = QLabel()
                    label.setPixmap(new_pixmap)
                    label.mousePressEvent = functools.partial(
                        self.clicked_image, source_obj=pixmap)
                    myform.addRow(label)
                except Exception:
                    pass
            mygroupbox.setLayout(myform)
            scroll.setWidget(mygroupbox)
            scroll.setWidgetResizable(True)
            scroll.setFixedHeight(768)
            area_images.addWidget(scroll)
            self.grid.addLayout(area_images, 0, 2)

    def clicked_image(self, event, source_obj=None):
        new_pixmap = source_obj.scaled(600, 600, Qt.KeepAspectRatio,
                                       Qt.SmoothTransformation)
        label = QLabel()
        label.setPixmap(new_pixmap)

        self.grid.addWidget(label, 0, 1)

    def show_photo(self, name_photo):
        pixmap = QPixmap(name_photo)
        new_pixmap = pixmap.scaled(600, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        label = QLabel()
        label.setPixmap(new_pixmap)
        self.grid.addWidget(label, 0, 1)

    def clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            if isinstance(item, QWidgetItem):
                item.widget().close()
            else:
                self.clear_layout(item.layout())
            layout.removeItem(item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())



