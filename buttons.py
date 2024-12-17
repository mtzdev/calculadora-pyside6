import math
from PySide6.QtWidgets import QPushButton, QGridLayout
from PySide6.QtCore import Slot

from utils import convertNumber, isValidNumber
from variables import MEDIUM_FONT_SIZE
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from display import Display
    from info import Info
    from main_window import MainWindow
    from PySide6.QtWidgets import QMessageBox

class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(70, 70)


class ButtonsGrid(QGridLayout):
    def __init__(self, display: 'Display', info: 'Info', window: 'MainWindow', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.display = display
        self.info = info
        self.window = window
        self._equation = ''
        self._left: float = None
        self._right: float = None
        self._op = None

        self._grid_mask = [
            ['C', '◀', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['+/-', '0', '.', '='],
        ]

        self.apply_buttons()
        self.display.enterPressed.connect(self._calculate)
        self.display.delPressed.connect(self.display.backspace)
        self.display.escPressed.connect(self._clear)
        self.display.operatorPressed.connect(lambda x: self._operatorClicked(key_text=x))

    @property
    def equation(self):
        return self._equation

    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)

    def apply_buttons(self):
        for k, i in enumerate(self._grid_mask):
            for v, button_name in enumerate(i):
                button = Button(button_name)
                if button_name not in '0123456789. ':
                    button.setProperty('cssClass', 'specialButton')
                    self._configSpecialButton(button)

                self.addWidget(button, k, v)

                buttonslot = self._makeSlot(
                    self._insertButtonTextToDisplay,
                    button
                )
                button.clicked.connect(buttonslot)

    def _connectButtonClicked(self, button, slot):
        button.clicked.connect(slot)

    def _configSpecialButton(self, button):
        text = button.text()
        if text == 'C':
            self._connectButtonClicked(button, self._clear)

        if text in '+-*/^':
            self._connectButtonClicked(button, self._makeSlot(self._operatorClicked, button))

        if text == '=':
            self._connectButtonClicked(button, self._calculate)

        if text == '◀':
            self._connectButtonClicked(button, self._backspace)

        if text == '+/-':
            self._connectButtonClicked(button, self._invertNumber)

    def _makeSlot(self, func, *args, **kwargs):
        @Slot()
        def realSlot():
            func(*args, **kwargs)
        return realSlot

    @Slot()
    def _invertNumber(self):
        displayText = self.display.text()
        self.display.setFocus()

        if not isValidNumber(displayText):
            self._showInfoBox('Insira um número antes de inverter o sinal!')
            return

        number = float(displayText) * -1
        self.display.setText(str(number))

    def _insertButtonTextToDisplay(self, button):
        buttonText = button.text()
        self.display.setFocus()

        if not isValidNumber(self.display.text() + buttonText):
            return

        self.display.insert(buttonText)

    @Slot()
    def _clear(self):
        self.display.clear()
        self.display.setFocus()
        self._left = None
        self._right = None
        self._op = None
        self.equation = 'Sua conta'

    @Slot()
    def _backspace(self):
        self.display.backspace()
        self.display.setFocus()

    @Slot()
    def _operatorClicked(self, button = None, key_text = None):
        buttonText = button.text() if button else key_text  # Necessário para funcionar com button, como também com Signal (operatorPressed)
        displayText = self.display.text()
        self.display.clear()
        self.display.setFocus()

        # É um operador e não há 1º valor ainda (permite mudar operador qnd já inserido 1º valor)
        if not isValidNumber(displayText) and self._left is None:
            self._showInfoBox('Insira um valor antes de selecionar um operador!')
            return

        # Se já tiver o 1º valor, aguarda 2º e não modifica 1º
        if self._left is None:
            self._left = convertNumber(displayText)

        self._op = buttonText
        self.equation = f'{self._left} {self._op}'

    # Slot quando o botão igual é clicado
    @Slot()
    def _calculate(self):
        displayText = self.display.text()
        self.display.setFocus()
        # display válido (right), left não é vazio e operador já foi selecionado
        if not isValidNumber(displayText) or self._left is None or self._op is None:
            return

        self._right = convertNumber(displayText)
        self.equation = f'{self._left} {self._op} {self._right} ='

        try:
            if self._op == '^':
                result = str(math.pow(self._left, self._right))
            else:
                result = str(round(eval(f'{self._left} {self._op} {self._right}'), 14))
        except ZeroDivisionError:
            result = '0'
            self._showErrorBox('Divisão por zero não é possível!')
        except OverflowError:
            result = '0'
            self._showErrorBox('O número calculado é muito grande!')
        self.display.setText(result)
        self._left = convertNumber(result)
        self._right = None
        self._op = None

    def _showInfoBox(self, text):
        msgBox: QMessageBox = self.window.makeMessageBox()
        msgBox.setText(text)
        msgBox.setWindowTitle("AVISO!")
        msgBox.setIcon(msgBox.Icon.Information)
        msgBox.exec()
        self.display.setFocus()

    def _showErrorBox(self, text):
        msgBox: QMessageBox = self.window.makeMessageBox()
        msgBox.setText(text)
        msgBox.setWindowTitle("ERRO!")
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.exec()
        self.display.setFocus()