from PyQt6.QtWidgets import QApplication
import sys
from uart_terminal_emulator_protocol_analyzer_pyqt_6 import UARTAnalyzerGUI



if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = UARTAnalyzerGUI()
    window.show()

    sys.exit(app.exec())