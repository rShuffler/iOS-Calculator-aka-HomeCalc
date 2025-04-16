from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QSpinBox
from PyQt5.QtGui import QFont
import json
import os

class SettingsWindow(QWidget):
    FILE_PATH = "config.json"

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setGeometry(150, 150, 320, 450)

        font_family = "SF Pro Display"
        self.settings = self.load_settings()

        # 🔹 Проверяем, что `self.settings` – это словарь
        if not isinstance(self.settings, dict):
            print("⚠️ Ошибка загрузки `config.json`, создаем настройки заново...")
            self.settings = self.default_settings()
            self.save_settings(self.settings)

        self.setStyleSheet("background-color: black; border-radius: 20px;")

        layout = QVBoxLayout()

        title_label = QLabel("Customize Your Calculator")
        title_label.setFont(QFont(font_family, 20, QFont.Bold))
        title_label.setStyleSheet("color: white; padding: 10px;")
        layout.addWidget(title_label)

        self.color_label = QLabel("Select Button Color:")
        self.color_label.setFont(QFont(font_family, 18))
        self.color_label.setStyleSheet("color: white; padding: 5px;")
        layout.addWidget(self.color_label)

        self.color_dropdown = QComboBox()
        self.color_dropdown.addItems(["#FF9500", "#00FF00", "#0000FF", "#FF0000"])
        self.color_dropdown.setCurrentText(self.settings.get("button_color", "#FF9500"))
        self.color_dropdown.setStyleSheet("""
            background-color: #222;
            color: white;
            padding: 10px;
            border-radius: 10px;
        """)
        layout.addWidget(self.color_dropdown)

        self.size_label = QLabel("Select Button Size:")
        self.size_label.setFont(QFont(font_family, 18))
        self.size_label.setStyleSheet("color: white; padding: 5px;")
        layout.addWidget(self.size_label)

        self.size_spinner = QSpinBox()
        self.size_spinner.setRange(40, 80)
        self.size_spinner.setValue(self.settings.get("button_size", 60))
        self.size_spinner.setStyleSheet("""
            background-color: #222;
            color: white;
            padding: 10px;
            border-radius: 10px;
        """)
        layout.addWidget(self.size_spinner)

        self.save_button = QPushButton("Save Settings")
        self.save_button.setFont(QFont(font_family, 18, QFont.Bold))
        self.save_button.setStyleSheet("""
            background-color: #FF9500;
            color: white;
            padding: 10px;
            border-radius: 10px;
            min-height: 50px;
        """)
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def default_settings(self):
        """Возвращает стандартные настройки."""
        return {
            "button_color": "#FF9500",
            "button_size": 60
        }

    def load_settings(self):
        """Загружает настройки из JSON-файла, проверяет данные."""
        if os.path.exists(self.FILE_PATH):
            try:
                with open(self.FILE_PATH, "r") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        return data
            except json.JSONDecodeError:
                print("⚠️ Ошибка чтения `config.json`, сбрасываем настройки...")
        # Если файл поврежден, создаем новые настройки
        return self.default_settings()

    def save_settings(self):
        """Сохраняет текущие настройки в файл."""
        new_settings = {
            "button_color": self.color_dropdown.currentText(),
            "button_size": self.size_spinner.value()
        }
        with open(self.FILE_PATH, "w") as f:
            json.dump(new_settings, f, indent=4)
        self.close()  # Закрываем окно после сохранения
