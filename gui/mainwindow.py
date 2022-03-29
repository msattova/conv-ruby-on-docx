
from pathlib import Path
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (QWidget,
                               QMainWindow,
                               QLineEdit,
                               QLabel,
                               QPushButton,
                               QMessageBox,
                               QVBoxLayout,
                               QHBoxLayout,
                               QFileDialog)


import modules.fileproc as fpc

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        with open('./style/style.qss', mode='r', encoding='utf-8') as f:
            style = f.read()

        self.setWindowTitle('カクヨム記法のルビをWordのルビにする')
        self.setFixedSize(QSize(500, 200))  # ウインドウサイズ
        self.setAcceptDrops(True)  # ドラッグアンドドロップ可に
        self.setStyleSheet(style)

        self.status = self.statusBar()
        self.status.setFixedHeight(30)

        self.description_label = QLabel(self)
        self.description_label.setText('変換したいファイル(ドラッグ&ドロップできます)：')

        self.input_path = QLineEdit('', self)
        self.input_path.setFixedWidth(260)

        self.choose_file_button = QPushButton('参照', self)
        self.choose_file_button.clicked.connect(self.choose_file)

        self.run_button = QPushButton('実行', self)
        self.run_button.clicked.connect(self.run)

        vbl = QVBoxLayout()
        hbl = QHBoxLayout()

        vbl.addWidget(self.description_label)
        hbl.addWidget(self.input_path)
        hbl.addWidget(self.choose_file_button)
        vbl.addLayout(hbl)

        vbl.addWidget(self.run_button, 0,
                      Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        central = QWidget()
        central.setLayout(vbl)

        self.setCentralWidget(central)

    def dragEnterEvent(self, e) -> None:
        m = e.mimeData()
        if m.hasText() or m.hasUrls():
            e.accept()

    def dropEvent(self, e) -> None:
        url = e.mimeData().urls()
        url = url[0].toLocalFile()
        self.input_path.setText(url)

    def choose_file(self):
        filename = QFileDialog.getOpenFileName(self,
                                               'ファイル選択',
                                               '.',
                                               'docx ファイル (*.docx)')
        self.input_path.setText(filename[0])

    def save_file(self):
        filename = QFileDialog.getSaveFileName(self,
                                               '変換したファイルを保存',
                                               '.',
                                               'docx ファイル (*.docx)')
        return filename[0]

    def run(self):
        input = Path(self.input_path.text())
        template = Path('')
        ruby_font = ''
        em_style = 'dot'
        #output = 'out.docx'
        output = Path(self.save_file())
        p = fpc.FileProc(template, input, output, ruby_font, em_style)
        p.process()
        QMessageBox.information(None, "成功", "実行に成功しました！")
