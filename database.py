import os
import sqlite3
from dotenv import load_dotenv
from cryptography.fernet import Fernet

load_dotenv()

key = os.getenv('ENCRYPT_KEY')
cipher_suite = Fernet(key)

conn = sqlite3.connect("password.db")
cursor = conn.cursor()

#this code only needs to run one time.run it one time then comment it.
# cursor.execute("""CREATE TABLE passwords (
#                website text,
#                email text,
#                password text
#                )""")


def encrypt_password(password):
    encrypted_password = cipher_suite.encrypt(password.encode('utf-8'))
    return encrypted_password


def decrypt_password(password):
    decrypted_password = cipher_suite.decrypt(password).decode('utf-8')
    return decrypted_password


def insert_record(website, email, password):
    encrypted_password = encrypt_password(password)
    cursor.execute("INSERT INTO passwords (website, email, password) VALUES (?,?,?)", (website, email, encrypted_password))
    conn.commit()


def read_record(website):
    cursor.execute("SELECT email, password FROM passwords WHERE website = (?)", (website,))
    result = cursor.fetchone()
    print(result)
    if result:
        decrypted_password = decrypt_password(result[1])
        return result[0], decrypted_password
    return "No result found"
