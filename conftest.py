import pytest
from api import register_user, login_user, delete_user
from helpers import generate_user_payload

@pytest.fixture
def registered_user():
    payload = generate_user_payload()
    response = register_user(payload)
    
    # Если юзер не создался, выводим сообщение с ошибкой
    assert response.status_code == 200, f"Не удалось создать юзера: {response.text}"
    
    access_token = response.json()["accessToken"]
    
    yield payload
    
    # Удаление юзера после теста
    delete_user(access_token)

@pytest.fixture
def auth_token(registered_user):
    login_response = login_user(registered_user)
    assert login_response.status_code == 200
    return login_response.json()["accessToken"]

# Создает и удаляет юзера
@pytest.fixture
def user_cleanup():
    created_tokens = []
    
    def _create_and_cleanup(payload):
        response = register_user(payload)
        if response.status_code == 200:
            created_tokens.append(response.json()["accessToken"])
        return response
        
    yield _create_and_cleanup

    for token in created_tokens:
        delete_user(token)