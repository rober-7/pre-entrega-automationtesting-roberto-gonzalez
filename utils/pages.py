"""Page Objects para saucedemo.com.

Cada clase encapsula las acciones y validaciones posibles sobre una
pagina del sitio, usando esperas explicitas (WebDriverWait) en lugar de
sleeps fijos para interactuar de forma confiable con los elementos.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.locators import CartPageLocators, InventoryPageLocators, LoginPageLocators

DEFAULT_TIMEOUT = 10


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT)


class LoginPage(BasePage):
    URL = "https://www.saucedemo.com/"

    def load(self):
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(LoginPageLocators.USERNAME_INPUT))
        return self

    def login(self, username, password):
        self.driver.find_element(*LoginPageLocators.USERNAME_INPUT).send_keys(username)
        self.driver.find_element(*LoginPageLocators.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*LoginPageLocators.LOGIN_BUTTON).click()

    def get_error_message(self):
        elemento = self.wait.until(EC.visibility_of_element_located(LoginPageLocators.ERROR_MESSAGE))
        return elemento.text


class InventoryPage(BasePage):
    def wait_until_loaded(self):
        self.wait.until(EC.url_contains("/inventory.html"))
        self.wait.until(EC.visibility_of_element_located(InventoryPageLocators.INVENTORY_CONTAINER))
        return self

    def get_page_title(self):
        elemento = self.wait.until(EC.visibility_of_element_located(InventoryPageLocators.PAGE_TITLE))
        return elemento.text

    def get_products(self):
        return self.driver.find_elements(*InventoryPageLocators.PRODUCT_ITEMS)

    def is_menu_present(self):
        return self.driver.find_element(*InventoryPageLocators.MENU_BUTTON).is_displayed()

    def is_sort_filter_present(self):
        return self.driver.find_element(*InventoryPageLocators.PRODUCT_SORT_FILTER).is_displayed()

    def get_first_product_name_and_price(self):
        primer_producto = self.get_products()[0]
        nombre = primer_producto.find_element(*InventoryPageLocators.PRODUCT_NAME).text
        precio = primer_producto.find_element(*InventoryPageLocators.PRODUCT_PRICE).text
        return nombre, precio

    def add_first_product_to_cart(self):
        self.driver.find_element(*InventoryPageLocators.FIRST_ADD_TO_CART_BUTTON).click()

    def get_cart_badge_count(self):
        badge = self.wait.until(EC.visibility_of_element_located(InventoryPageLocators.CART_BADGE))
        return int(badge.text)

    def go_to_cart(self):
        self.driver.find_element(*InventoryPageLocators.CART_LINK).click()


class CartPage(BasePage):
    def wait_until_loaded(self):
        self.wait.until(EC.url_contains("/cart.html"))
        return self

    def get_cart_items(self):
        return self.driver.find_elements(*CartPageLocators.CART_ITEMS)

    def get_cart_item_names(self):
        return [
            item.find_element(*CartPageLocators.CART_ITEM_NAME).text
            for item in self.get_cart_items()
        ]
