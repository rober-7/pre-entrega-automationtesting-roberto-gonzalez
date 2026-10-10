"""Datos de prueba utilizados por los tests de saucedemo.com."""

BASE_URL = "https://www.saucedemo.com/"

VALID_USER = {
    "username": "standard_user",
    "password": "secret_sauce",
}

LOCKED_OUT_USER = {
    "username": "locked_out_user",
    "password": "secret_sauce",
}

INVALID_USER = {
    "username": "usuario_inexistente",
    "password": "password_incorrecta",
}

EXPECTED_INVENTORY_TITLE = "Products"
EXPECTED_BROWSER_TAB_TITLE = "Swag Labs"
EXPECTED_LOGIN_ERROR_MESSAGE = "Epic sadface: Username and password do not match any user in this service"
