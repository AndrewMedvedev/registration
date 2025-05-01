from config import settings

STATUS_OK = 200
PATH_ENDPOINT = "/api/v1/"
MIN_STATUS_CODE = 100
BYTES_SECRET_KEY_HASH = bytes(settings.SECRET_KEY_HASH, "utf-8")
