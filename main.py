import os
import random
import string
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Generate a random AES key
KEY = ''.join(random.choices(string.ascii_letters + string.digits, k=16)).encode()

def encrypt_file(file_path):
    """Encrypts a file using AES."""
    try:
        with open(file_path, "rb") as file:
            data = file.read()
        
        cipher = AES.new(KEY, AES.MODE_CBC, iv=b'0123456789abcdef')
        encrypted_data = cipher.encrypt(pad(data, AES.block_size))

        with open(file_path, "wb") as file:
            file.write(cipher.iv + encrypted_data)  # Store IV at the beginning

        print(f"[+] Encrypted: {file_path}")
    except Exception as e:
        print(f"[-] Error encrypting {file_path}: {e}")

def decrypt_file(file_path, key):
    """Decrypts an AES-encrypted file."""
    try:
        with open(file_path, "rb") as file:
            iv = file.read(16)  # Extract IV
            encrypted_data = file.read()
        
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

        with open(file_path, "wb") as file:
            file.write(decrypted_data)

        print(f"[+] Decrypted: {file_path}")
    except Exception as e:
        print(f"[-] Error decrypting {file_path}: {e}")

def encrypt_directory(directory):
    """Encrypts all files in a directory."""
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            encrypt_file(file_path)

def decrypt_directory(directory, key):
    """Decrypts all files in a directory."""
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            decrypt_file(file_path, key)

if __name__ == "__main__":
    action = input("Choose (1) Encrypt or (2) Decrypt: ")
    directory = input("Enter directory path: ")

    if action == "1":
        encrypt_directory(directory)
        print(f"\n🔐 Save this key to decrypt your files: {KEY.decode()}")

    elif action == "2":
        key_input = input("Enter decryption key: ").encode()
        decrypt_directory(directory, key_input)

    else:
        print("[-] Invalid choice.")
