import hashlib

def calculaHash():
    print("introcuce la contraseña")
    contraseña= input()
    print("Hash:  ", hashlib.sha256(contraseña.encode()).hexdigest())

calculaHash() 