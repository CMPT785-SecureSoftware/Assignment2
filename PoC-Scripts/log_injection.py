import requests
import os

# get token from env
token = os.environ.get("TOKEN")

url = "http://localhost:9090/file"
cookies = {
    'token': token,
    'admin': 'true'
}

# Filename with actual newline
files = {
    'file': ('normal.jpg\nServer Unreachable', b'content of file')
}

response = requests.post(url, cookies=cookies, files=files)
print(response.text)
