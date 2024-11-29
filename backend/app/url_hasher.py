import secrets
import base64

def generate_random_base64(length:int=6) -> str:
    random_bytes = secrets.token_bytes(length)
    base64_string = base64.urlsafe_b64encode(random_bytes).rstrip(b'=').decode('utf-8')
    return base64_string