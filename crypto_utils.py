import base64 #для декодирования данных в двоичный вид
import json # для преобразования расшифрованных данных в словарь
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms,modes #для шифрования(здесь AES)
from cryptography.hazmat.backends import default_backend #для выполнения криптографических операций
import logging # для логгирования


logger = logging.getLogger(__name__) #создаётся объекст логгера с именем текущего модуля, чтобы просматривать ошибки

def key_load_from_flash('path', binary=False):
    key = b"8888888888888888"
    return key
#     try:
#         with open ("path", "rb") as f:
#             key = f.read().strip()
#             return key
#     except Exception as e:
#         logging.error(f"Ошибка при чтении ключа из файла {e}")


def decrypt_data(encrypted_data, key):
    try:
        decrypt_data = base64.b64decode(encrypted_data) #преобразует входные данные из строки base64 в двоичный(в итоге получается посл-ть байтов в кот IV и зашифрованные данные)
        iv = decrypt_data[:16]# разделение данных первые 16 байт - IV, нужен для CBC
        ciphertext=decrypt_data[16:]# сам зашифрованный текст
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv),backend=default_backend())
        #создается объект шифра AES с ключом key в режиме CBC c IV для уникальности шифрования default_backend-стандартная криптографиская реализация
        decryptor = cipher.decryptor() #создаётся объект для расшифровки
        padded_data = decryptor.update(ciphertext)+decryptor.finalize() #дешифрует и завершает дешшифрование
        padding_len = padded_data[-1]#последний байт указывает длину набивки 
        plaintext = padded_data[:-padding_len] #удаляет набивку, оставляя чистый текст
        return json.loads(plaintext.decode("UTF-8"))
    except Exception as e:
        logger.error(f"Ошибка расшифровки {e}")
        return None

    



