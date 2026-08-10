from PyQt6.QtWidgets import QDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QSizePolicy
from src.translations import STRINGS


class SettingsDialog(QDialog):
    def __init__(self, parent=None, current_language="English"):
        super().__init__(parent)
        self.current_language = current_language
        self.setWindowTitle(STRINGS[self.current_language]["settings_title"])
        self.setMinimumSize(480, 360)

        layout = QVBoxLayout()
        lang_label = QLabel(STRINGS[self.current_language]["lang_label"])
        lang_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        layout.addWidget(lang_label)
        self.lang_field = QComboBox()
        self.lang_field.addItems(["English", "Русский"])
        index = self.lang_field.findText(current_language)
        if index >= 0:
            self.lang_field.setCurrentIndex(index)

        lang_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        layout.addWidget(self.lang_field)

        layout.addStretch()

        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        self.btn_add = QPushButton(STRINGS[self.current_language]["btn_save"])
        self.btn_add.clicked.connect(self.accept)
        self.btn_cancel = QPushButton(STRINGS[self.current_language]["btn_cancel"])
        self.btn_cancel.clicked.connect(self.reject)

        button_layout.addWidget(self.btn_cancel, 1)
        button_layout.addWidget(self.btn_add, 1)
        button_container.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        layout.addWidget(button_container)

        self.setLayout(layout)

    def get_data(self):
        return self.lang_field.currentText()