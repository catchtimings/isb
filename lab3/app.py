import sys

from PyQt6 import QtCore

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QPushButton,
    QDialog,
    QFileDialog,
    QMessageBox,
)

from filehandler import FileHandler
from hybrid_crypto_system import HybridCryptoSystem
from constant import DEFAULT_DIRECTORY, IconTypes


class SelectLength(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select key length")
        self.setFixedSize(700, 100)

        self.button64 = QPushButton("64 bit")
        self.button128 = QPushButton("128 bit")
        self.button256 = QPushButton("256 bit")

        self.button64.setStyleSheet("height: 130px;")
        self.button128.setStyleSheet("height: 130px;")
        self.button256.setStyleSheet("height: 130px;")

        layout = QHBoxLayout()
        layout.addWidget(self.button64)
        layout.addWidget(self.button128)
        layout.addWidget(self.button256)
        self.setLayout(layout)

        self.button64.clicked.connect(lambda: self.select_length(64))
        self.button128.clicked.connect(lambda: self.select_length(128))
        self.button256.clicked.connect(lambda: self.select_length(256))

        self.key_length = None

    def select_length(self, length):
        self.key_length = length
        self.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hybrid CryptoSystem")
        self.setFixedSize(1280, 320)
        (container := QWidget()).setLayout(layout := QHBoxLayout())

        self.open_settings_button = QPushButton("Open settings file")
        self.generator_button = QPushButton("Generate keys")

        self.open_settings_button.setStyleSheet("height: 130px;")
        self.generator_button.setStyleSheet("height: 130px;")

        self.open_settings_button.clicked.connect(self.open_settings)
        self.generator_button.clicked.connect(self.generation_key)
        layout.addWidget(self.open_settings_button)
        layout.addWidget(self.generator_button)
        self.setCentralWidget(container)

        self.settings = None
        self.dialog = None

    def open_settings(self):
        try:
            file, _ = QFileDialog.getOpenFileName(
                parent=QApplication.activeWindow(),
                caption="Select json file with settings",
                directory=DEFAULT_DIRECTORY,
                filter="JSON Files (*.json)",
            )
            if file:
                self.settings = FileHandler.read_data(file, "r")
                self.show_message("Success", "Settings loaded", IconTypes.Information)
                if not QtCore.QFile.exists(file):
                    self.show_message("Error!", "File not found", IconTypes.Critical)
            else:
                self.show_message(
                    "Error", "Please select a valid json file", IconTypes.Critical
                )
        except Exception as e:
            self.show_message(
                "Error!",
                f"An error occurred while opening the file: {e}",
                IconTypes.Critical,
            )

    def show_message(self, title: str, text: str, icon_type: IconTypes):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        icon = QMessageBox.Icon.NoIcon
        match icon_type:
            case IconTypes.Critical:
                icon = QMessageBox.Icon.Critical
            case IconTypes.Warning:
                icon = QMessageBox.Icon.Warning
            case IconTypes.Information:
                icon = QMessageBox.Icon.Information
            case IconTypes.Question:
                icon = QMessageBox.Icon.Question
        msg.setIcon(icon)
        msg.exec()

    def generation_key(self):
        try:
            if not self.settings:
                self.show_message(
                    "Settings was not found", "Load settings first", IconTypes.Warning
                )
                return
            self.dialog = SelectLength()
            self.dialog.exec()
            key_length = self.dialog.key_length
            HybridCryptoSystem.generate_keys(
                self.settings["symmetric_key"],
                self.settings["public_key"],
                self.settings["private_key"],
                key_length,
            )
            self.show_message(
                "Success", "Keys were saved to files", IconTypes.Information
            )
        except Exception as e:
            print(e)
            self.show_message(
                "Error!",
                f"An error occurred when generating keys: {e}",
                IconTypes.Critical,
            )


def launch_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
