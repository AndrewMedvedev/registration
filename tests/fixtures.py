from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient
from pytest import fixture

from main import app


@fixture
def client():
    return TestClient(app)


@fixture
def authorization_mock():
    with patch("src.controllers.AuthorizationControl") as mock:
        instance = mock.return_value
        instance.sql_authorization = AsyncMock()
        instance.jwt_create = AsyncMock()
        instance.hash = AsyncMock()
        yield instance


@fixture
def get_user_data_mock():
    with patch("src.controllers.GetUserDataControl") as mock:
        instance = mock.return_value
        instance.sql_authorization = AsyncMock()
        yield instance


@fixture
def vk_mock():
    with patch("src.controllers.VKControl") as mock:
        instance = mock.return_value
        instance.sql_vk = AsyncMock()
        instance.jwt_create = AsyncMock()
        instance.vk_api = AsyncMock()
        yield instance


@fixture
def yandex_mock():
    with patch("src.controllers.YandexControl") as mock:
        instance = mock.return_value
        instance.sql_yandex = AsyncMock()
        instance.jwt_create = AsyncMock()
        instance.yandex_api = AsyncMock()
        yield instance
