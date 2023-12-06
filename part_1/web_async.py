from sys import argv
import asyncio
import aiohttp
import aiofiles

async def get_content(url: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    content = await response.read()
                    return content
                else:
                    print(f"Une erreur est survenue : {response.status}")
                    return None

    except Exception as e:
        print(e)
        return None
    
async def write_content(content, file_path):
    try:
        async with aiofiles.open(file_path, "wb") as web_page_file:
            await web_page_file.write(content)
    except Exception as e:
        print(e)
        exit(1)
    
async def main():
    if len(argv) != 2:
        print("Veuillez entrer un url en argument")
        exit(1)

    url = argv[1]
    file_path = "/tmp/web_page"
    
    content = await get_content(url)
    if content is not None:
        await write_content(content, file_path)
    else:
        exit(0)
    
    
if __name__ == "__main__":
    asyncio.run(main())
