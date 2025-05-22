from dotenv import dotenv_values, find_dotenv

env_path = find_dotenv()


def load_config() -> dict:
    env_path = find_dotenv(".env")

    if not env_path:
        env_path = find_dotenv(".test.env")

    return dotenv_values(env_path)


config = load_config()


class Settings:
    POSTGRES_HOST: str = config["POSTGRES_HOST"]
    POSTGRES_PORT: str = config["POSTGRES_PORT"]
    POSTGRES_PASSWORD: str = config["POSTGRES_PASSWORD"]
    POSTGRES_USER: str = config["POSTGRES_USER"]
    POSTGRES_DB: str = config["POSTGRES_DB"]

    REDIS_HOST: str = config["REDIS_HOST"]
    REDIS_PORT: str = config["REDIS_PORT"]
    REDIS_PASSWORD: str = config["REDIS_PASSWORD"]

    SECRET_KEY: str = config["SECRET_KEY"]
    ALGORITHM: str = config["ALGORITHM"]

    SECRET_KEY_HASH: str = config["SECRET_KEY_HASH"]

    VK_APP_ID: int = config["VK_APP_ID"]
    VK_APP_SECRET: str = config["VK_APP_SECRET"]
    VK_REDIRECT_URI: str = config["VK_REDIRECT_URI"]
    VK_AUTH_URL: str = config["VK_AUTH_URL"]
    VK_TOKEN_URL: str = config["VK_TOKEN_URL"]
    VK_API_URL: str = config["VK_API_URL"]
    STATE_VK: str = config["STATE_VK"]
    CLIENT_SECRET: str = config["CLIENT_SECRET"]

    YANDEX_APP_ID: str = config["YANDEX_APP_ID"]
    YANDEX_APP_SECRET: str = config["YANDEX_APP_SECRET"]
    YANDEX_REDIRECT_URI: str = config["YANDEX_REDIRECT_URI"]
    YANDEX_AUTH_URL: str = config["YANDEX_AUTH_URL"]
    YANDEX_TOKEN_URL: str = config["YANDEX_TOKEN_URL"]
    YANDEX_API_URL: str = config["YANDEX_API_URL"]
    STATE_YANDEX: str = config["STATE_YANDEX"]
    YANDEX_SCOPE: str = config["YANDEX_SCOPE"]


settings = Settings()


def get_db_url() -> str:
    return f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
