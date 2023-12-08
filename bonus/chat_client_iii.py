import asyncio
from aioconsole import ainput
from os.path import isfile, exists
from json import load
from argparse import ArgumentParser
from encoding import encode_message


async def async_input(writer):
    while True:
        user_message = await ainput("")
        if user_message == "":
            continue
        
        print(f"Vous avez dit : {user_message}")
        
        encoded_message = encode_message(user_message)
        writer.write(encoded_message)
        await writer.drain()
        
async def async_receive(reader):
    while True:
        header = await reader.read(1)
        
        if header == b'':
            raise Exception("Le serveur s'est déconnecté. Aurevoir")
        
        next_bytes_to_read = int.from_bytes(header, byteorder='big')
        message_len = await reader.read(next_bytes_to_read)
        message_len = int.from_bytes(message_len, byteorder='big')
        
        data = await reader.read(message_len)
        
        message = data.decode()
        print(f"{message}")
    
        
async def main():
    parser = ArgumentParser()
    parser.add_argument("-p", "--port", action="store")
    parser.add_argument("-a", "--address", action="store")
    
    args = parser.parse_args()
    
    host, port = args.address, args.port
    
    if (host is None) and (port is None) and exists("config.json") and isfile("config.json"):
        with open('config.json', 'r') as openfile:
            json_object = load(openfile)
        host, port = json_object["host"], json_object["port"]
    
    pseudo = input("Entrez votre pseudo : ")
    
    room_number = 0
    while room_number < 1 or room_number > 9:
        try:
            room_number = int(input("Choisissez une room à laquelle vous connecter (chiffre de 1 à 9) : "))
        except:
            print("Veuillez entrer un chiffre entre 1 et 9\n")
    
    reader, writer = await asyncio.open_connection(host, port)
    
    writer.write(f"Hello|{room_number}|{pseudo}".encode())
    
    tasks = [ async_input(writer), async_receive(reader) ]
    
    await asyncio.gather(*tasks)
    
    
if __name__ == "__main__":
    asyncio.run(main())