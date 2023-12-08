from math import ceil

def encode_message(message:str) -> bytes:
    message_len = len(message)
    message_len_bit_length = message_len.bit_length()
    message_len_byte_length = 2 if ceil(message_len_bit_length/8.0) < 3 else ceil(message_len_bit_length/8.0)
    message_len_length = 1 if message_len_byte_length < 3 else 2
    print(f"Lala : {message_len_length} Lolo : {message_len}")
    
    header = message_len_length.to_bytes(1, byteorder='big')
    sequence = header + message_len.to_bytes(message_len_byte_length, byteorder='big') + message.encode()
    
    return sequence

def decode_message(message:bytes) -> str:
    pass