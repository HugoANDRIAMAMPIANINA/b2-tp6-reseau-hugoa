import asyncio

global HOST 
HOST = "10.1.1.11"
global PORT
PORT = 8888

async def handle_client_msg(reader, writer):
    while True:
        data = await reader.read(1024)
        client_host, client_port = writer.get_extra_info('peername')

        if data == b'':
            break

        message = data.decode()
        print(f"Message received from {client_host}:{client_port} : {message!r}")

        writer.write(f"Hello {client_host}:{client_port}".encode())
        await writer.drain()

async def main():
    server = await asyncio.start_server(handle_client_msg, HOST, PORT)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())