import threading
import base64
import json
from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings

class EmailThreading(threading.Thread):
    def __init__(self, email_obj):
        threading.Thread.__init__(self)
        self.email_obj=email_obj

    def run(self):
        self.email_obj.send()


def get_fernet():
    key=settings.FERNET_SECRET_KEY.encode()
    return Fernet(key)

def generate_encrypted_token(data:dict)->str:
    fernet=get_fernet()
    json_data=json.dumps(data).encode()
    return fernet.encrypt(json_data).decode()

def decrypt_encrypted_token(token:str)->dict:
    fernet = get_fernet()  
    try:
        # for 5 minutes
        decrypted = fernet.decrypt(token.encode(), ttl=300)  

    except InvalidToken:
        raise ValueError("Token is expired or invalid")

    payload = json.loads(decrypted)
    return payload
