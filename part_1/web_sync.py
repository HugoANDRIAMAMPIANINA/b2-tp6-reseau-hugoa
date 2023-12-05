from sys import argv
from urllib.request import urlopen

def get_content(url: str):
    try:
        with urlopen(url) as response:
            content = response.read().decode('utf-8')
            return content
    except Exception as e:
        print(e)
        return None

def write_content(content, file_path):
    try:
        with open(file_path, "w") as web_page_file:
            web_page_file.write(content)
    except Exception as e:
        print(e)


if len(argv) < 2:
    print("Veuillez entrer un url en argument")
    exit(0)
    
url = argv[1]
file_path = "/tmp/web_page"
content = get_content(url)

if content == None:
    exit(0)
    
write_content(content, file_path)