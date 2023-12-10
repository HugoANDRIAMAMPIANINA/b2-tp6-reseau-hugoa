from math import ceil
import asyncio

def encode_message(message: bytes) -> bytes:
    message_len = len(message)
    message_len_bit_length = message_len.bit_length()
    message_len_byte_length = 2 if ceil(message_len_bit_length/8.0) < 3 else ceil(message_len_bit_length/8.0)
    message_len_length = 1 if message_len_byte_length < 3 else 2
    
    header = message_len_length.to_bytes(1, byteorder='big')
    sequence = header + message_len.to_bytes(message_len_byte_length, byteorder='big') + message.encode()
    
    return sequence

async def write_message(writer: asyncio.StreamWriter, message: bytes) -> None:
    writer.write(message)
    await writer.drain()

async def read_header(reader: asyncio.StreamReader) -> bytes:
    header = await reader.read(1)
    return header

async def read_message(reader: asyncio.StreamReader, header) -> bytes:
    next_bytes_to_read = int.from_bytes(header, byteorder='big')
    print(next_bytes_to_read)
    if next_bytes_to_read == 1:
        next_bytes_to_read = 2
    message_len = await reader.read(next_bytes_to_read)
    message_len = int.from_bytes(message_len, byteorder='big')
    data = await reader.read(message_len)
    return data
