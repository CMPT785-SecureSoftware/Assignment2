import jwt 
import pickle
import os

SECRET_KEY="secret_key"
token = jwt.encode({ "username": "admin1" }, SECRET_KEY, algorithm="HS256")
obfuscate1 = pickle.dumps(token.encode())
obfuscate2 = obfuscate1.hex()
obfuscate3 = obfuscate2[len(obfuscate2)//2:] + obfuscate2[:len(obfuscate2)//2]

# put it as an environment variable
os.environ["TOKEN"] = str(obfuscate3)

