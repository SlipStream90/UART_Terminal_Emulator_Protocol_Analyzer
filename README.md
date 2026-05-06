# UART Terminal Emulator + Protocol Analyzer

A software-based UART communication emulator and embedded serial protocol analyzer built using Python and PyQt6.

This project simulates UART transmission, ARM-style register behavior, interrupt handling, packet analysis, and serial waveform visualization without requiring physical embedded hardware.

Designed as an educational embedded systems project aligned with:
- ARM7TDMI architecture
- UART communication
- interrupt systems
- memory-mapped IO
- embedded debugging concepts

---

# Features

## UART Terminal Emulator
- Send and receive UART-style serial data
- Simulated TX/RX communication
- Configurable baud rate
- Configurable parity modes

---

## UART Frame Visualization

Visualizes UART frames in realtime:

```text
START(0) | DATA(11001110) | PARITY(1) | STOP(1)
```

Includes:
- Start bit
- Data bits
- Parity bit
- Stop bit

---

## Digital Waveform Generation

Displays UART signal timing:

```text
___|‾‾‾|‾‾‾|___|___|‾‾‾|
```

Represents:
- LOW signals
- HIGH signals
- serial bit timing

---

## Packet Analyzer

Realtime decoding of:
- ASCII
- HEX
- Binary

Example:

| Character | ASCII | HEX | Binary |
|---|---|---|---|
| A | 65 | 0x41 | 01000001 |

---

## ARM Register Viewer

Simulated ARM7TDMI register display:

```text
R0   : 0x00000041
R1   : 0xE000C000
R2   : 0x00000020
R13/SP : 0x40001000
R14/LR : 0x00000084
R15/PC : 0x00000020
CPSR : N=0 Z=0 C=0 V=0
```

Supports:
- General purpose registers
- Stack Pointer
- Link Register
- Program Counter
- CPSR flag simulation

---

## UART Register Simulation

Simulates LPC2148 UART registers:

```text
U0THR : 0x41
U0RBR : 0x41
U0LSR : 0x20
```

Includes:
- THR
- RBR
- LSR
- THRE status

---

## Interrupt Simulation

Simulated UART interrupt logging:

```text
[IRQ] UART RX Interrupt Triggered
[ISR] Received Byte: 0x41
[ISR] Stored byte into RX Buffer
```

---

# Concepts Covered

This project demonstrates practical understanding of:

- UART communication
- ARM7TDMI architecture
- serial communication protocols
- memory-mapped IO
- interrupt handling
- embedded debugging
- parity checking
- framing
- baud rate timing
- CPSR flags
- register-level hardware simulation

---

# Technologies Used

- Python 3
- PyQt6

---

# Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/uart-terminal-emulator.git
cd uart-terminal-emulator
```

---

## Install Dependencies

```bash
pip install PyQt6
```

---

# Run Application

```bash
python main.py
```

---

# Project Structure

```text
uart-terminal-emulator/
│
├── main.py
├── README.md
└── requirements.txt
```

---

# UART Frame Structure

The emulator simulates standard UART frames:

```text
START | DATA | PARITY | STOP
```

Example:

```text
START(0) | DATA(11001110) | PARITY(1) | STOP(1)
```

---

# UART Status Flags

Simulated UART Line Status Register flags:

| Flag | Meaning |
|---|---|
| RDR | Receiver Data Ready |
| OE | Overrun Error |
| PE | Parity Error |
| FE | Framing Error |
| BI | Break Interrupt |
| THRE | Transmit Holding Register Empty |
| TEMT | Transmitter Empty |

---

# ARM Concepts Simulated

## ARM Registers
- R0–R15
- SP
- LR
- PC

---

## CPSR Flags

| Flag | Meaning |
|---|---|
| N | Negative |
| Z | Zero |
| C | Carry |
| V | Overflow |

---

# Example Output

```text
R0   : 0x000000CE
R1   : 0xE000C000
R2   : 0x00000020

UART REGISTERS
-------------------------
U0THR : 0xCE
U0RBR : 0xCE
U0LSR : 0x20

THR Empty = TRUE
```

---

# Future Improvements

Planned extensions:
- Realtime UART timing animation
- COM port support
- FIFO buffer simulation
- DMA simulation
- ARM instruction execution
- ARM pipeline visualization
- UART error injection
- RTOS task simulation
- Live logic analyzer waveform rendering

---

# Educational Applications

Useful for:
- embedded systems learning
- ARM architecture visualization
- UART debugging demonstrations
- computer architecture labs
- serial communication analysis
- protocol debugging education


Embedded Systems • ARM Architecture • UART Simulation • Protocol Analysis
