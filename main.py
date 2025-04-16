import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QGridLayout
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtCore import Qt
from settings import SettingsWindow  # Импортируем настройки

class Calculator(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("HomeCalc")
        self.setGeometry(100, 100, 320, 500)  # Увеличил высоту для кнопки "Настройки"
        self.setStyleSheet("background-color: black; border-radius: 20px;")

        layout = QVBoxLayout()

        font_id = QFontDatabase.addApplicationFont("fonts/SFPRODISPLAYBOLD.OTF")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0] if font_id != -1 else "Arial"

        self.display = QLineEdit()
        self.display.setFont(QFont(font_family, 24, QFont.Bold))
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setStyleSheet("""
            background-color: #333;
            color: white;
            border: none;
            padding: 20px;
            border-radius: 10px;
            height: 60px;
        """)
        layout.addWidget(self.display)

        button_layout = QGridLayout()
        buttons = [
            ('AC', 0, 0), ('±', 0, 1), ('%', 0, 2), ('÷', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('×', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
            ('0', 4, 0, 1, 2), ('.', 4, 2), ('=', 4, 3)
        ]

        for text, row, col, rowspan, colspan in [(b + (1, 1) if len(b) == 3 else b) for b in buttons]:
            btn = QPushButton(text)
            btn.setFont(QFont(font_family, 24, QFont.Bold))
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {'#FF9500' if text in ['÷', '×', '-', '+', '='] else '#505050'};
                    color: white;
                    border: none;
                    padding: 20px;
                    border-radius: 50%;
                    min-width: 60px;
                    min-height: 60px;
                }}
                QPushButton:pressed {{
                    background-color: {'#CC7600' if text in ['÷', '×', '-', '+', '='] else '#808080'};
                }}
            """)

            btn.clicked.connect(self.on_button_click)
            button_layout.addWidget(btn, row, col, rowspan, colspan)

        layout.addLayout(button_layout)

        # 🔹 Добавляем кнопку "Настройки"
        self.settings_button = QPushButton("⚙️ Settings")
        self.settings_button.setFont(QFont(font_family, 18))
        self.settings_button.setStyleSheet("background-color: #222; color: white; border-radius: 10px; padding: 10px;")
        self.settings_button.clicked.connect(self.open_settings)
        layout.addWidget(self.settings_button)  # Добавляем в основной layout

        self.setLayout(layout)

    def open_settings(self):
        """Открывает окно настроек."""
        self.settings_window = SettingsWindow()
        self.settings_window.show()

    def on_button_click(self):
        sender = self.sender()
        text = sender.text()

        if text == '=':
            try:
                result = str(eval(self.display.text().replace('÷', '/').replace('×', '*')))
                self.display.setText(result)
            except:
                self.display.setText("Ошибка")
        elif text == 'AC':
            self.display.clear()
        else:
            self.display.setText(self.display.text() + text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec_())
