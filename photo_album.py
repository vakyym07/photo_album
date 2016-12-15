from PyQt5.QtWidgets import \
    QWidget, QMainWindow, \
    QAction, QFormLayout, \
    QScrollArea, QDesktopWidget, \
    QGroupBox, QPushButton, \
    QVBoxLayout, QLabel, \
    QGridLayout, QApplication, \
    QWidgetItem, QFileDialog, \
    QMessageBox, QProgressBar, \
    QHBoxLayout, QLineEdit
from PyQt5.QtGui import \
    QPixmap, QPalette, \
    QBrush
from PyQt5.QtCore import \
    Qt, QThread, \
    pyqtSignal

import sys
import os
import os.path
import functools
import clustering_image
import time
import search_photo as sp


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_widget = Photo(self)
        self.do_clustering = None
        self.main_widget.init_ui()
        self.init_ui()

    def init_ui(self):
        self.resize(800, 600)
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

        self.do_clustering = QAction('Cluster images', self)
        self.do_clustering.triggered.connect(self.main_widget.do_clustering)
        self.change_state_button(False)
        file_menu.addAction(open_file_action)
        file_menu.addAction(self.do_clustering)

        find_photo = menubar.addMenu('&Find photo')
        search_action = QAction('Find photos', self)
        search_action.triggered.connect(self.main_widget.searching_photo)
        find_photo.addAction(search_action)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def change_state_button(self, flag):
        self.do_clustering.setEnabled(flag)


class Photo(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.current_path = None
        self.arr_photo = []
        self.start = None
        self.grid = QGridLayout()
        self.progressbar = None
        self.task = None
        self.count_photo_on_page = 10
        self.edit_window = None

    def init_ui(self):
        button = QPushButton("Open directory", self)
        button.clicked.connect(self.open_path)
        button.setFixedWidth(300)
        button.setFixedHeight(200)
        self.grid.addWidget(button, 4, 4)
        self.setLayout(self.grid)

    def open_path(self):
        path = QFileDialog.getExistingDirectory(self, 'Select Directory', '/home')
        if os.path.exists(path):
            self.current_path = path
            self.arr_photo = [os.path.join(path, e)
                              for e in os.listdir(path)
                              if os.path.isfile(os.path.join(path, e))]
            self.clear_layout(self.grid)
            self.start = 0
            self.draw_layout()

    def draw_layout(self):
        self.show_photo(self.arr_photo[self.start])
        self.show_all_photo()
        self.draw_buttons()
        self.parent.change_state_button(True)

    def draw_buttons(self):
        b_prev = QPushButton("Prev", self)
        b_next = QPushButton("Next", self)
        self.grid.addWidget(b_prev, 2, 1)
        self.grid.addWidget(b_next, 2, 2)
        b_prev.clicked.connect(self.get_prev_page)
        b_next.clicked.connect(self.get_next_page)

    def get_prev_page(self):
        if self.start - self.count_photo_on_page >= 0:
            self.clear_layout(self.grid)
            self.start -= self.count_photo_on_page
            self.draw_layout()

    def get_next_page(self):
        if self.start + self.count_photo_on_page < \
                        len(self.arr_photo):
            self.clear_layout(self.grid)
            self.start += self.count_photo_on_page
            self.draw_layout()

    def show_all_photo(self):
        mygroupbox = QGroupBox("Images")
        myform = QFormLayout()
        scroll = QScrollArea()
        area_images = QVBoxLayout()
        start = self.start
        end = min(self.start + self.count_photo_on_page, len(self.arr_photo))
        if len(self.arr_photo) != 0:
            for photo in self.arr_photo[start: end]:
                try:
                    pixmap = QPixmap(photo)
                    new_pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio,
                                               Qt.SmoothTransformation)
                    label = QLabel()
                    label.setPixmap(new_pixmap)
                    label.mousePressEvent = functools.partial(
                        self.clicked_image, source_obj=photo)
                    myform.addRow(label)
                except Exception:
                    pass
            mygroupbox.setLayout(myform)
            scroll.setWidget(mygroupbox)
            scroll.setWidgetResizable(True)
            scroll.setFixedHeight(600)
            area_images.addWidget(scroll)
            self.grid.addLayout(area_images, 0, 2)

    def clicked_image(self, event, source_obj=None):
        self.show_photo(source_obj)

    def show_photo(self, name_photo):
        self.delete_widget(self.grid, QLabel)
        try:
            pixmap = QPixmap(name_photo)
            new_pixmap = pixmap.scaled(600, 600, Qt.KeepAspectRatio,
                                       Qt.SmoothTransformation)
            label = QLabel()
            label.setPixmap(new_pixmap)
            self.grid.addWidget(label, 0, 1)
        except OSError:
            pass

    def delete_widget(self, layout, instance):
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if isinstance(item, QWidgetItem):
                if isinstance(item.widget(), instance):
                    item.widget().close()
                    layout.removeItem(item)

    def clear_layout(self, layout):
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item is not None:
                if isinstance(item, QWidgetItem):
                    item.widget().close()
                else:
                    self.clear_layout(item.layout())
                layout.removeItem(item)

    def do_clustering(self):
        reply = QMessageBox.question(
            self, 'Message',
            "Are you sure to cluster "
            "images in this directory?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.current_path is not None:
                self.parent.change_state_button(False)
                self.progressbar = QProgressBar(self)
                self.progressbar.setRange(0, 100)
                self.grid.addWidget(self.progressbar, 3, 1)
                self.task = TaskThread(self.current_path)
                self.task.task_finished.connect(self.on_progress)
                try:
                    self.on_start()
                except PermissionError:
                    pass
                except FileNotFoundError:
                    pass

    def on_start(self):
        self.task.start()

    def on_progress(self, i):
        self.progressbar.setValue(i)

    def set_arr_photo(self, arr_photo):
        self.arr_photo = arr_photo

    def set_start(self, start):
        self.start = start

    def searching_photo(self):
        if len(self.arr_photo) != 0:
            self.edit_window = EditWindow(self)
            self.edit_window.init_ui()


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


class EditWindow(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.column = ['Comment', 'Title',
                       'Topic', 'Author',
                       "Key word"]
        self.edits = {}
        self.dic_edit_label = {}
        self.parent_window = parent_window

    def init_ui(self):
        grid = QGridLayout()
        grid.setSpacing(10)
        hbox_button = QHBoxLayout()
        list_edits = []
        list_labels = []

        position_label = [(i, 0) for i in range(len(self.column))]
        position_edit = [(i, 1) for i in range(len(self.column))]

        for label, pos in zip(self.column, position_label):
            lb = QLabel(label)
            list_labels.append(lb)
            grid.addWidget(lb, *pos)

        for pos in position_edit:
            qle = QLineEdit(self)
            list_edits.append(qle)
            qle.textChanged[str].connect(self.on_changed)
            grid.addWidget(qle, *pos)

        self.dic_edit_label = \
            {x[0]: x[1] for x in zip(list_edits, list_labels)}

        ok_button = QPushButton('Ok', self)
        ok_button.clicked.connect(self.is_ok)
        cancel_button = QPushButton('Cancel', self)
        cancel_button.clicked.connect(self.close)

        hbox_button.addWidget(ok_button)
        hbox_button.addWidget(cancel_button)

        grid.addLayout(hbox_button, len(self.column) + 1, 0)

        self.setLayout(grid)

        self.setGeometry(900, 300, 350, 300)
        self.setWindowTitle('Edit information')
        self.show()

    def on_changed(self, text):
        self.edits[self.sender()] = text

    def is_ok(self):
        dic_req = {}
        for edit in self.dic_edit_label:
            if self.edits.get(edit) is not None:
                name = self.dic_edit_label[edit].text()
                dic_req[name] = self.edits[edit]
        self.edits = {}
        self.dic_edit_label = {}
        self.update_window(dic_req)
        self.close()

    def update_window(self, dic_req):
        new_arr_photo = sp.response(dic_req, self.parent_window.arr_photo)
        if len(new_arr_photo) != 0:
            self.parent_window.set_arr_photo(new_arr_photo)
            self.parent_window.set_start(0)
            self.parent_window.draw_layout()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())



