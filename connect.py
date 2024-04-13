import configparser
from mongoengine import connect
from pathlib import Path

# Шлях до файлу конфігурації
file_config = Path(__file__).parent.joinpath("config.ini")
config = configparser.ConfigParser()
config.read(file_config)

# Отримання даних для підключення до MongoDB з конфігураційного файлу
mongo_user = config.get("DB", "USER")
mongodb_pass = config.get("DB", "PASSWORD")
db_name = config.get("DB", "DB_NAME")
domain = config.get("DB", "DOMAIN")

# Підключення до кластера AtlasDB MongoDB
connect(
    host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority""",
    ssl=True,
)

# Доступ до підключення з інших файлів
def get_database():
    from mongoengine import get_db

    return get_db()
