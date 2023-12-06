from sys import argv
import requests

def get_content(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        content = response.content
        return content
    else:
        print(f"Le contenu de cette url n'a pas pu être récupéré : {response.status_code}")
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

if content is None:
    exit(0)
    
write_content(content, file_path)