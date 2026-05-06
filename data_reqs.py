from dataclasses import dataclass

@dataclass
class UARTFrame:
    start_bit: int
    data_bits: list
    parity_bit: int | None
    stop_bit: int
    raw_byte: int