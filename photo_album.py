from PyQt5.QtWidgets import \
    QWidget, QMainWindow, \
    QAction, QFormLayout, \
    QScrollArea, QDesktopWidget, \
    QGroupBox, QPushButton, \
    QVBoxLayout, QLabel, \
    QGridLayout, QHBoxLayout, \
    QLineEdit, QApplication, \
    qApp, QInputDialog, \
    QWidgetItem, QFileDialog, \
    QMessageBox, QProgressBar
from PyQt5.QtGui import \
    QPixmap, QIcon, \
    QPalette, QBrush
from PyQt5.QtCore import Qt, QBasicTimer, QThread, pyqtSignal
import sys
import os
import os.path
import functools
import clustering_image
import time


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_widget = Photo()
        self.main_widget.init_ui()
        self.init_ui()

    def init_ui(self):
        self.resize(1024, 768)
        self.center()
        palette = QPalette()
        pixmap = QPixmap("background.jpg")
        palette.setBrush(QPalette.Background, QBrush(pixmap))
        self.setPalette(palette)
        self.setWindowTitle('Photo Album')
        self.setCentralWidget(self.main_widget)
        self.create_menu()
        self.show()

    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        open_file_action = QAction('&Open', self)
        open_file_action.triggered.connect(self.main_widget.open_path)
        do_clustering = QAction('Cluster images', self)
        do_clustering.triggered.connect(self.main_widget.do_clustering)
        file_menu.addAction(open_file_action)
        file_menu.addAction(do_clustering)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()


class Photo(QWidget):
    def __init__(self):
        super().__init__()
        self.current_path = None
        self.arr_photo = []
        self.current_index_photo = 0
        self.grid = QGridLayout()
        self.progressbar = None
        self.task = None

    def init_ui(self):
        button = QPushButton("Open directory", self)
        button.clicked.connect(self.open_path)
        button.setFixedWidth(300)
        button.setFixedHeight(200)
        self.grid.addWidget(button, 4, 4)
        self.setLayout(self.grid)

    def open_path(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        if os.path.exists(fname):
            head_path, tail_path = os.path.split(fname)
            self.current_path = head_path
            self.arr_photo = [os.path.join(head_path, e)
                              for e in os.listdir(head_path)
                              if os.path.isfile(os.path.join(head_path, e))]
            self.current_index_photo = self.arr_photo.index(
                os.path.join(head_path, tail_path))
            self.show_photo(self.arr_photo[self.current_index_photo])
            self.show_all_photo()

    def show_all_photo(self):
        mygroupbox = QGroupBox("Images")
        myform = QFormLayout()
        scroll = QScrollArea()
        area_images = QVBoxLayout()
        if len(self.arr_photo) != 0:
            for photo in self.arr_photo:
                try:
                    pixmap = QPixmap(photo)
                    new_pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio,
                                               Qt.SmoothTransformation)
                    label = QLabel()
                    label.setPixmap(new_pixmap)
                    label.mousePressEvent = functools.partial(
                        self.clicked_image, source_obj=pixmap)
                    myform.addRow(label)
                except Exception as e:
                    print(e)
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
        self.clear_layout(self.grid)
        self.grid.addWidget(label, 0, 1)

    def show_photo(self, name_photo):
        self.clear_layout(self.grid)
        pixmap = QPixmap(name_photo)
        new_pixmap = pixmap.scaled(600, 600, Qt.KeepAspectRatio,
                                   Qt.SmoothTransformation)
        label = QLabel()
        label.setPixmap(new_pixmap)
        self.grid.addWidget(label, 0, 1)

    def clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            if isinstance(item, QWidgetItem):
                item.widget().close()
                layout.removeItem(item)

    def get_next_photo(self):
        if len(self.arr_photo) > 0:
            if self.current_index_photo + 1 < len(self.arr_photo):
                self.current_index_photo += 1
                self.show_photo(self.arr_photo[self.current_index_photo])

    def get_prev_photo(self):
        if len(self.arr_photo) > 0:
            if self.current_index_photo - 1 >= 0:
                self.current_index_photo -= 1
                self.show_photo(self.arr_photo[self.current_index_photo])

    def do_clustering(self):
        reply = QMessageBox.question(
            self, 'Message',
            "Are you sure to cluster "
            "images in this directory?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.progressbar = QProgressBar(self)
            self.progressbar.setRange(0, 100)
            self.grid.addWidget(self.progressbar, 3, 1)
            self.task = TaskThread(self.current_path)
            self.task.task_finished.connect(self.on_progress)
            self.on_start()

    def on_start(self):
        # self.progressbar.setRange(0, 0)
        self.task.start()

    def on_progress(self, i):
        # self.progressbar.setRange(0, 1)
        self.progressbar.setValue(i)


class TaskThread(QThread):
    task_finished = pyqtSignal(int)

    def __init__(self, path):
        super().__init__()
        self.path = path

    def run(self):
        clustering_image.start_clustering(self.path)
        for i in range(101):
            self.task_finished.emit(i)
            time.sleep(0.1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())



