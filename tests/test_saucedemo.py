"""Tests de automatizacion para saucedemo.com.

Cubren los 3 flujos obligatorios de la pre-entrega:
1. Login (TestLogin)
2. Navegacion y verificacion del catalogo (TestCatalog)
3. Interaccion con productos / carrito (TestCart)

Cada test hace su propio login cuando lo necesita para que los tests
sean independientes entre si (la falla de uno no afecta a los demas).
"""

from datos.test_data import EXPECTED_BROWSER_TAB_TITLE, EXPECTED_INVENTORY_TITLE, VALID_USER
from utils.pages import CartPage, InventoryPage, LoginPage


def iniciar_sesion_y_obtener_inventario(driver):
    """Helper interno: hace login con un usuario valido y devuelve el InventoryPage ya cargado."""
    login_page = LoginPage(driver).load()
    login_page.login(VALID_USER["username"], VALID_USER["password"])

    inventory_page = InventoryPage(driver)
    inventory_page.wait_until_loaded()
    return inventory_page


class TestLogin:
    """Automatizacion de Login (criterio obligatorio #1)."""

    def test_login_exitoso_redirige_a_pagina_de_inventario(self, driver):
        inventory_page = iniciar_sesion_y_obtener_inventario(driver)

        assert "/inventory.html" in driver.current_url
        assert driver.title == EXPECTED_BROWSER_TAB_TITLE
        assert inventory_page.get_page_title() == EXPECTED_INVENTORY_TITLE


class TestCatalog:
    """Navegacion y verificacion del catalogo (criterio obligatorio #2)."""

    def test_titulo_de_pagina_de_inventario_es_correcto(self, driver):
        inventory_page = iniciar_sesion_y_obtener_inventario(driver)

        assert inventory_page.get_page_title() == EXPECTED_INVENTORY_TITLE

    def test_existen_productos_visibles_en_el_catalogo(self, driver):
        inventory_page = iniciar_sesion_y_obtener_inventario(driver)
        productos = inventory_page.get_products()

        assert len(productos) > 0

    def test_elementos_importantes_de_la_interfaz_estan_presentes(self, driver):
        inventory_page = iniciar_sesion_y_obtener_inventario(driver)

        assert inventory_page.is_menu_present() is True
        assert inventory_page.is_sort_filter_present() is True

    def test_lista_nombre_y_precio_del_primer_producto(self, driver):
        inventory_page = iniciar_sesion_y_obtener_inventario(driver)
        nombre, precio = inventory_page.get_first_product_name_and_price()

        assert nombre != ""
        assert precio.startswith("$")
        print(f"Primer producto encontrado -> Nombre: {nombre} | Precio: {precio}")


class TestCart:
    """Interaccion con productos / carrito (criterio obligatorio #3)."""

    def test_agregar_producto_incrementa_contador_del_carrito(self, driver):
        inventory_page = iniciar_sesion_y_obtener_inventario(driver)

        inventory_page.add_first_product_to_cart()

        assert inventory_page.get_cart_badge_count() == 1

    def test_producto_agregado_aparece_correctamente_en_el_carrito(self, driver):
        inventory_page = iniciar_sesion_y_obtener_inventario(driver)
        nombre_producto, _ = inventory_page.get_first_product_name_and_price()

        inventory_page.add_first_product_to_cart()
        inventory_page.go_to_cart()

        cart_page = CartPage(driver)
        cart_page.wait_until_loaded()

        assert nombre_producto in cart_page.get_cart_item_names()
