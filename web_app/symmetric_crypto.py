import base64

def simple_encrypt(message: str, key: str) -> str:
    repeated_key = (key * (len(message) // len(key) + 1))[:len(message)]
    encrypted_bytes = [ord(m) ^ ord(k) for m, k in zip(message, repeated_key)]
    encrypted_data = bytes(encrypted_bytes)
    return base64.b64encode(encrypted_data).decode('utf-8')

def simple_decrypt(encrypted_data: str, key: str) -> str:
    encrypted_bytes = base64.b64decode(encrypted_data.encode('utf-8'))
    repeated_key = (key * (len(encrypted_bytes) // len(key) + 1))[:len(encrypted_bytes)]
    decrypted_chars = [chr(b ^ ord(k)) for b, k in zip(encrypted_bytes, repeated_key)]
    return ''.join(decrypted_chars)