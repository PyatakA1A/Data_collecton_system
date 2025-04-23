import asyncio
import websockets
import json
import logging
from threading import Thread
from time import sleep
from crypto_utils import key_load_from_flash, decrypt_data
from monitoring import send_alert
from db import init_db, save_to_db, get_users
from monitoring import send_alert

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='system.log',
                    filemode="a",
                    encoding = 'utf-8')
logger = logging.getLogger(__name__)

KEY = None

# функция сбора данных с WebSocket
async def collect_data():
    uri = "ws://45.67.56.214:8088/users"
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                logger.info("Подключение к WebSocket установлено")
                send_alert("Система запущена", "Подключение к WebSocket успешно")
                while True:
                    message = await websocket.recv()
                    encrypted_array = json.loads(message)
                    decrypted_data = [decrypt_data(item, KEY) for item in encrypted_array]
                    save_to_db(decrypted_data)
                    logger.info(f"Обработано и сохранено {len(encrypted_array)} записей")
        except Exception as e:
            logger.error(f"Ошибка WebSocket: {e}")
            send_alert("Сбой WebSocket", f"Произошла ошибка: {str(e)}")
            await asyncio.sleep(5)

# функция отображения в консоль
def display_users():
    while True:
        try:
            users = get_users()
            print("\n=== Список пользователей ===")
            print("ID | Фамилия | Номер | Адрес | Пароль | Время")
            print("-" * 80)
            for user in users:
                print(f"{user[0]} | {user[1]} | {user[2]} | {user[3]} | {user[4]} | {user[5]}")
            print("-" * 80)
        except Exception as e:
            logger.error(f"Ошибка отображения данных: {e}")
        sleep(10)

          
def main():
    global KEY
    KEY = key_load_from_flash()
    init_db()

    # Запуск интерфейса в отдельном потоке
    ui_thread = Thread(target=display_users)
    ui_thread.daemon = True
    ui_thread.start()

    # Запуск сбора данных
    asyncio.run(collect_data())

if __name__ == "__main__":
    main()



