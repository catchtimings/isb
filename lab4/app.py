import os
from sys import argv

from PyQt6 import QtCore
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QMessageBox,
    QFileDialog,
    QHBoxLayout, QPushButton
)

from app_assest.app_const import CARD_NUMBER_DIRECTORY, DEFAULT_DIRECTORY, IconTypes
from hash_function_collision.hash_function_collision import HashFunctionCollision
from filehandler import FileHandler


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hash Function Collision")
        self.setFixedSize(720, 320)
        (container := QWidget()).setLayout(layout := QHBoxLayout())

        self.match_card_number_button = QPushButton("Match a card number")
        self.check_card_number_button = QPushButton("Check card number")

        self.match_card_number_button.setStyleSheet("height: 130px; font-size: 18px;")
        self.check_card_number_button.setStyleSheet("height: 130px; font-size: 18px;")

        self.match_card_number_button.clicked.connect(self.match_card_number)
        self.check_card_number_button.clicked.connect(self.check_card_number)

        layout.addWidget(self.match_card_number_button)
        layout.addWidget(self.check_card_number_button)

        self.setCentralWidget(container)

    def select_file(self, caption_):
        try:
            directory, _ = QFileDialog.getOpenFileName(
                parent=self,
                caption=caption_,
                directory=DEFAULT_DIRECTORY,
            )
            if directory:
                if not QtCore.QFile.exists(directory):
                    self.show_message("Error", "File not found", IconTypes.Critical)
                    return None
                return directory
            else:
                self.show_message(
                    "Error", "Please select a valid file", IconTypes.Critical
                )
                return None
        except Exception as e:
            self.show_message(
                "Error",
                f"An error occurred while opening the file: {e}",
                IconTypes.Critical,
            )
            return None

    def select_directory(self, caption_):
        try:
            directory = QFileDialog.getExistingDirectory(
                parent=self,
                caption=caption_,
                directory=DEFAULT_DIRECTORY,
            )
            if not directory:
                self.show_message("Error", "Directory not selected", IconTypes.Critical)
                return None
            else:
                return directory
        except Exception as e:
            self.show_message("Error", f"An error occurred while selecting the directory: {e}", IconTypes.Critical)
            return None

    def show_message(self, title: str, text: str, icon_type: IconTypes):
        msg = QMessageBox()
        msg.setStyleSheet("font-size: 14px;")
        msg.setWindowTitle(title)
        msg.setText(text)
        match icon_type:
            case IconTypes.Critical:
                icon = QMessageBox.Icon.Critical
            case IconTypes.Warning:
                icon = QMessageBox.Icon.Warning
            case IconTypes.Information:
                icon = QMessageBox.Icon.Information
            case IconTypes.Question:
                icon = QMessageBox.Icon.Question
            case _:
                icon = QMessageBox.Icon.NoIcon
        msg.setIcon(icon)
        msg.exec()

    def match_card_number(self):
        try:
            hash_value = FileHandler.read_data(self.select_file("Select file with card hash"), "r")
            last_four_digits = FileHandler.read_data(self.select_file("Select file with last four digits"), "r")
            bin_value = FileHandler.read_data_tuple(self.select_file("Select file with card bin"),"r")  # Сбебранк использует номера 427XX-4279XX
            dir_to_ser = os.path.join(self.select_directory("Select directory to serialization card number"), CARD_NUMBER_DIRECTORY)
            HashFunctionCollision.match_card_number(
                hash_value,
                last_four_digits,
                bin_value,
                dir_to_ser
            )
            self.show_message("Success", "Card number was matched and serialized to file", IconTypes.Information)
        except Warning as w:
            self.show_message("Fail", f"{w}", IconTypes.Information)
        except ValueError as ve:
            self.show_message("Error", f"Something is wrong with data: {ve}", IconTypes.Critical)
        except Exception as e:
            self.show_message("Error", f"An error occurred when trying to select the card number: {e}", IconTypes.Critical)

    def check_card_number(self):
        try:
            card_number = FileHandler.read_data(self.select_file("Select json file with card number"), "r")["card_number"]
            if HashFunctionCollision.check_validate(str(card_number)):
                self.show_message("Success", "Your card number is correct", IconTypes.Information)
            else:
                self.show_message("Fail", "Your card number isn't correct", IconTypes.Information)
        except ValueError as ve:
            self.show_message("Error", f"Something is wrong with data: {ve}", IconTypes.Critical)
        except Exception as e:
            self.show_message("Error", f"An error occurred when trying to check card number validate: {e}", IconTypes.Critical)


if __name__ == "__main__":
    app = QApplication(argv)
    window = MainWindow()
    window.show()
    app.exec()
