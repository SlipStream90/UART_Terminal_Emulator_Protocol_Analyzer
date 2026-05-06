import sys
import time
from dataclasses import dataclass
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QPushButton,
    QLabel,
    QLineEdit,
    QComboBox,
    QGroupBox,
    QTableWidget,
    QTableWidgetItem,
)
from PyQt6.QtCore import Qt, QTimer

from data_reqs import UARTFrame


class UARTEmulator:
    def __init__(self, baud_rate=9600, parity="None"):
        self.baud_rate = baud_rate
        self.parity = parity

    def calculate_parity(self, bits):
        ones = sum(bits)

        if self.parity == "Even":
            return 0 if ones % 2 == 0 else 1

        if self.parity == "Odd":
            return 1 if ones % 2 == 0 else 0

        return None

    def create_frame(self, byte):
        bits = [(byte >> i) & 1 for i in range(8)]

        parity_bit = self.calculate_parity(bits)

        frame = UARTFrame(
            start_bit=0,
            data_bits=bits,
            parity_bit=parity_bit,
            stop_bit=1,
            raw_byte=byte,
        )

        return frame

    def bit_time(self):
        return 1 / self.baud_rate


class UARTAnalyzerGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("UART Terminal Emulator + Protocol Analyzer")
        self.setGeometry(200, 100, 1200, 850)

        self.uart = UARTEmulator()

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        title = QLabel("UART Terminal Emulator and Protocol Analyzer")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")

        main_layout.addWidget(title)

        # ============================
        # UART CONFIG
        # ============================

        config_group = QGroupBox("UART Configuration")
        config_layout = QHBoxLayout()

        self.baud_combo = QComboBox()
        self.baud_combo.addItems(["1200", "2400", "4800", "9600", "19200", "115200"])
        self.baud_combo.setCurrentText("9600")

        self.parity_combo = QComboBox()
        self.parity_combo.addItems(["None", "Even", "Odd"])

        apply_button = QPushButton("Apply Settings")
        apply_button.clicked.connect(self.apply_uart_settings)

        config_layout.addWidget(QLabel("Baud Rate:"))
        config_layout.addWidget(self.baud_combo)
        config_layout.addWidget(QLabel("Parity:"))
        config_layout.addWidget(self.parity_combo)
        config_layout.addWidget(apply_button)

        config_group.setLayout(config_layout)

        main_layout.addWidget(config_group)

        # ============================
        # TERMINAL
        # ============================

        terminal_group = QGroupBox("UART Terminal")
        terminal_layout = QVBoxLayout()

        self.terminal_output = QTextEdit()
        self.terminal_output.setReadOnly(True)
        self.terminal_output.setStyleSheet(
            "background-color: black; color: lime; font-family: Consolas; font-size: 14px;"
        )

        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Type UART message...")

        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_uart_data)

        terminal_layout.addWidget(self.terminal_output)
        terminal_layout.addWidget(self.input_line)
        terminal_layout.addWidget(send_button)

        terminal_group.setLayout(terminal_layout)

        main_layout.addWidget(terminal_group)

        # ============================
        # FRAME VIEWER
        # ============================

        frame_group = QGroupBox("UART Frame Viewer")
        frame_layout = QVBoxLayout()

        self.frame_display = QTextEdit()
        self.frame_display.setReadOnly(True)

        frame_layout.addWidget(self.frame_display)

        frame_group.setLayout(frame_layout)

        main_layout.addWidget(frame_group)

        # ============================
        # PACKET ANALYZER
        # ============================

        analyzer_group = QGroupBox("Packet Analyzer")
        analyzer_layout = QVBoxLayout()

        self.packet_table = QTableWidget()
        self.packet_table.setColumnCount(4)
        self.packet_table.setHorizontalHeaderLabels(
            ["Character", "ASCII", "HEX", "Binary"]
        )

        analyzer_layout.addWidget(self.packet_table)

        analyzer_group.setLayout(analyzer_layout)

        main_layout.addWidget(analyzer_group)

        # ============================
        # INTERRUPT LOG
        # ============================

        interrupt_group = QGroupBox("Interrupt / Status Log")
        interrupt_layout = QVBoxLayout()

        self.interrupt_log = QTextEdit()
        self.interrupt_log.setReadOnly(True)

        interrupt_layout.addWidget(self.interrupt_log)

        interrupt_group.setLayout(interrupt_layout)

        main_layout.addWidget(interrupt_group)

        # ============================
        # ARM REGISTER VIEW
        # ============================

        register_group = QGroupBox("ARM Register Viewer")
        register_layout = QVBoxLayout()

        self.register_display = QTextEdit()
        self.register_display.setReadOnly(True)

        register_layout.addWidget(self.register_display)

        register_group.setLayout(register_layout)

        main_layout.addWidget(register_group)

        self.update_register_view()

        self.setLayout(main_layout)

    # ======================================
    # UART SETTINGS
    # ======================================

    def apply_uart_settings(self):
        baud = int(self.baud_combo.currentText())
        parity = self.parity_combo.currentText()

        self.uart.baud_rate = baud
        self.uart.parity = parity

        self.log_interrupt(
            f"[CONFIG] UART configured: {baud} baud, {parity} parity"
        )

    # ======================================
    # SEND DATA
    # ======================================

    def send_uart_data(self):
        text = self.input_line.text()

        if not text:
            return

        self.terminal_output.append(f"> {text}")

        for ch in text:
            byte = ord(ch)

            frame = self.uart.create_frame(byte)

            self.display_frame(frame)
            self.display_packet(byte)

            self.simulate_interrupt(byte)

            time.sleep(self.uart.bit_time())

        self.input_line.clear()

    # ======================================
    # FRAME DISPLAY
    # ======================================

    def display_frame(self, frame):
        data_string = ''.join(str(bit) for bit in frame.data_bits)

        parity_text = (
            str(frame.parity_bit)
            if frame.parity_bit is not None
            else "NONE"
        )

        frame_text = (
            f"START({frame.start_bit}) | "
            f"DATA({data_string}) | "
            f"PARITY({parity_text}) | "
            f"STOP({frame.stop_bit})"
        )

        self.frame_display.append(frame_text)

        waveform = self.generate_waveform(frame)

        self.frame_display.append(waveform)
        self.frame_display.append("-" * 70)

    # ======================================
    # WAVEFORM GENERATION
    # ======================================

    def generate_waveform(self, frame):
        bits = [frame.start_bit] + frame.data_bits

        if frame.parity_bit is not None:
            bits.append(frame.parity_bit)

        bits.append(frame.stop_bit)

        waveform = ""

        for bit in bits:
            if bit == 1:
                waveform += "‾‾‾|"
            else:
                waveform += "___|"

        return waveform

    # ======================================
    # PACKET ANALYZER
    # ======================================

    def display_packet(self, byte):
        row = self.packet_table.rowCount()
        self.packet_table.insertRow(row)

        ch = chr(byte)
        ascii_val = str(byte)
        hex_val = hex(byte)
        binary_val = format(byte, '08b')

        self.packet_table.setItem(row, 0, QTableWidgetItem(ch))
        self.packet_table.setItem(row, 1, QTableWidgetItem(ascii_val))
        self.packet_table.setItem(row, 2, QTableWidgetItem(hex_val))
        self.packet_table.setItem(row, 3, QTableWidgetItem(binary_val))

    # ======================================
    # INTERRUPT SIMULATION
    # ======================================

    def simulate_interrupt(self, byte):
        self.log_interrupt("[IRQ] UART RX Interrupt Triggered")
        self.log_interrupt(f"[ISR] Received Byte: {hex(byte)}")
        self.log_interrupt("[ISR] Stored byte into RX Buffer")

    def log_interrupt(self, message):
        self.interrupt_log.append(message)

    # ======================================
    # ARM REGISTER VIEW
    # ======================================

    def update_register_view(self, byte=0x00, tx_empty=True):
    # ==========================================
    # ARM GENERAL PURPOSE REGISTERS
    # ==========================================
        r0 = byte

    # UART0 Base Address
        r1 = 0xE000C000

    # Line Status Register
        # Bit 5 = THRE
        r2 = 0x20 if tx_empty else 0x00

    # Stack Pointer
        sp = 0x40001000

    # Link Register
        lr = 0x00000084

    # Program Counter
        pc = 0x00000020

    # ==========================================
    # CPSR FLAGS
    # ==========================================
        n_flag = 1 if (byte & 0x80) else 0
        z_flag = 1 if byte == 0 else 0
        c_flag = 0
        v_flag = 0

    # ==========================================
    # UART REGISTERS
    # ==========================================

        u0thr = byte
        u0rbr = byte

    # U0LSR
    # Bit 5 = THRE
        u0lsr = 0x20 if tx_empty else 0x00

    # ==========================================
    # HUMAN READABLE STATUS
    # ==========================================

        thr_status = "TRUE" if tx_empty else "FALSE"

    # ==========================================
    # REGISTER DISPLAY STRING
    # ==========================================

        register_text = (
        f"R0   : 0x{r0:08X}\\n"
        f"R1   : 0x{r1:08X}\\n"
        f"R2   : 0x{r2:08X}\\n"
        f"R13/SP : 0x{sp:08X}\\n"
        f"R14/LR : 0x{lr:08X}\\n"
        f"R15/PC : 0x{pc:08X}\\n"
        f"CPSR : N={n_flag} Z={z_flag} C={c_flag} V={v_flag}\\n"
        "\\n"
        "UART REGISTERS\\n"
        "-------------------------\\n"
        f"U0THR : 0x{u0thr:02X}\\n"
        f"U0RBR : 0x{u0rbr:02X}\\n"
        f"U0LSR : 0x{u0lsr:02X}\\n"
        f"THR Empty = {thr_status}\\n"
    )

        self.register_display.setText(register_text)


