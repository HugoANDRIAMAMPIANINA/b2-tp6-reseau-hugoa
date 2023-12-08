from math import ceil
import asyncio

def encode_message(message:str) -> bytes:
    message_len = len(message)
    message_len_bit_length = message_len.bit_length()
    message_len_byte_length = 2 if ceil(message_len_bit_length/8.0) < 3 else ceil(message_len_bit_length/8.0)
    message_len_length = 1 if message_len_byte_length < 3 else 2
    print(f"Lala : {message_len_length} Lolo : {message_len}")
    
    header = message_len_length.to_bytes(1, byteorder='big')
    sequence = header + message_len.to_bytes(message_len_byte_length, byteorder='big') + message.encode()
    
    return sequence

def write_message(writer) -> None:
    pass

async def read_header(reader) -> bytes:
    header = await reader.read(1)
    return header

async def read_message(reader, header) -> bytes:
    next_bytes_to_read = int.from_bytes(header, byteorder='big')
    if next_bytes_to_read == 1:
        next_bytes_to_read = 2
    message_len = await reader.read(next_bytes_to_read)
    message_len = int.from_bytes(message_len, byteorder='big')
    data = await reader.read(message_len)
    return data

def decode_message(message:bytes) -> str:
    pass