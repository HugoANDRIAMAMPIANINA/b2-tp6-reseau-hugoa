import asyncio
from aioconsole import ainput
from os.path import isfile, exists
from json import load
from argparse import ArgumentParser

global HOST 
HOST = "10.1.1.11"
global PORT
PORT = 8888

async def async_input(writer):
    while True:
        user_message = await ainput("")
        if user_message == "":
            continue
        
        print(f"Vous avez dit : {user_message}")
        writer.write(user_message.encode())
        await writer.drain()
        
async def async_receive(reader):
    while True:
        server_response = await reader.read(1024)
        if server_response == b'':
            raise Exception("Le serveur s'est déconnecté. Aurevoir")
        
        message = server_response.decode()
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
    
    reader, writer = await asyncio.open_connection(host=HOST, port=PORT)
    
    writer.write(f"Hello|{pseudo}".encode())
    
    tasks = [ async_input(writer), async_receive(reader) ]
    
    await asyncio.gather(*tasks)
    
    
if __name__ == "__main__":
    asyncio.run(main())