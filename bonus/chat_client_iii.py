import asyncio
from aioconsole import ainput
from os.path import isfile, exists
from json import load
from argparse import ArgumentParser
from encoding import encode_message, read_header, read_message, write_message


async def async_input(writer: asyncio.StreamWriter):
    while True:
        user_message = await ainput("")
        if user_message == "":
            continue
        
        print(f"Vous avez dit : {user_message}")
        
        encoded_message = encode_message(user_message)
        write_message(writer, encoded_message)
        
async def async_receive(reader: asyncio.StreamReader):
    while True:
        header = await read_header(reader)
        
        if header == b'':
            raise Exception("Le serveur s'est déconnecté. Aurevoir")
        
        data = await read_message(reader, header)
        
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
    encoded_message = encode_message(f"Hello|{room_number}|{pseudo}")
    writer.write(encoded_message)
    
    tasks = [ async_input(writer), async_receive(reader) ]
    
    await asyncio.gather(*tasks)
    
    
if __name__ == "__main__":
    asyncio.run(main())