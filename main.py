import sys
from display import Display
from PySide6.QtWidgets import QApplication
from main_window import MainWindow
from info import Info
from buttons import ButtonsGrid
from styles import setupTheme


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    setupTheme(app)

    window.setWindowTitle("Calculadora")

    # Info
    info = Info('Sua conta')
    window.addWidgetToVLayout(info)

    # Display
    display = Display()
    window.addWidgetToVLayout(display)

    # Grid + Buttons
    buttonsGrid = ButtonsGrid(display, info, window)
    window.vLayout.addLayout(buttonsGrid)

    window.adjustFixedSize()
    window.show()
    app.exec()