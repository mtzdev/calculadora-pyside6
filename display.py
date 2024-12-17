from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QContextMenuEvent, QKeyEvent
from PySide6.QtWidgets import QLineEdit
from utils import isNumOrDot, isValidNumber
from variables import BIG_FONT_SIZE, MINIMUM_WIDTH, TEXT_MARGIN


class Display(QLineEdit):
    enterPressed = Signal()
    delPressed = Signal()
    escPressed = Signal()
    operatorPressed = Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        self.setStyleSheet(f'font-size: {BIG_FONT_SIZE}px;')
        self.setMinimumHeight(BIG_FONT_SIZE * 2)
        self.setMinimumWidth(MINIMUM_WIDTH)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setTextMargins(*[TEXT_MARGIN for _ in range(4)])

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:  # Desabilita menu ao clicar com o botão direito
        return event.ignore()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        key_pressed = event.key()
        key_text = event.text()
        keys = Qt.Key

        signals = {
            keys.Key_Enter: self.enterPressed.emit,
            keys.Key_Return: self.enterPressed.emit,
            keys.Key_Backspace: self.delPressed.emit,
            keys.Key_Delete: self.delPressed.emit,
            keys.Key_Escape: self.escPressed.emit
        }

        # Se for número/ponto, e for válido para adicionar na barra, então permite adicionar
        if isNumOrDot(key_text) and isValidNumber(self.displayText() + key_text):
            return super().keyPressEvent(event)

        # Signal para calcular (=), backspace e esc (clear)
        if key_pressed in signals.keys():
            signals[key_pressed]()
            return event.ignore()

        # Signal para os operadores +, -, *, /
        if key_pressed in [keys.Key_Plus, keys.Key_Minus, keys.Key_Asterisk, keys.Key_Slash]:
            self.operatorPressed.emit(key_text)
            return event.ignore()

        # Navegar pelos números usando setas ← →
        if key_pressed in [keys.Key_Left, keys.Key_Right]:
            return super().keyPressEvent(event)

        return event.ignore() #super().keyPressEvent(event)

