# Pre-Entrega de Proyecto — Automatización QA con Selenium y Pytest

## Propósito del proyecto

Suite de automatización de pruebas end-to-end sobre [saucedemo.com](https://www.saucedemo.com/), desarrollada como pre-entrega del curso de Automation Testing. Cubre tres flujos críticos de la aplicación:

1. **Login**: inicio de sesión con credenciales válidas y validación de redirección al inventario.
2. **Catálogo**: verificación del título de la página, presencia de productos y elementos de interfaz (menú, filtro de orden).
3. **Carrito**: agregado de un producto, verificación del contador del carrito y del listado de productos dentro del carrito.

## Tecnologías utilizadas

- **Python 3.12**
- **Selenium WebDriver 4** — automatización del navegador
- **Pytest** — framework de testing
- **pytest-html** — generación de reportes HTML
- **webdriver-manager** — gestión automática del ChromeDriver
- **Google Chrome** como navegador objetivo

## Estructura del proyecto

```
pre-entrega-automationtesting-robert-gonzalez/
├── tests/
│   ├── conftest.py          # Fixture del driver + hook de captura en fallos
│   └── test_saucedemo.py    # Casos de prueba: login, catálogo y carrito
├── utils/
│   ├── locators.py          # Localizadores (By) de cada página
│   └── pages.py             # Page Objects (LoginPage, InventoryPage, CartPage)
├── datos/
│   └── test_data.py         # Credenciales y valores esperados
├── reports/
│   ├── reporte.html         # Reporte HTML generado por pytest-html
│   └── screenshots/         # Capturas automáticas ante fallos
├── requirements.txt
├── pytest.ini
└── README.md
```

El proyecto sigue el patrón **Page Object Model**: los localizadores y las acciones sobre cada página viven en `utils/`, separados de los casos de prueba en `tests/`.

## Instalación de dependencias

1. Clonar el repositorio:
   ```bash
   git clone <url-del-repositorio>
   cd pre-entrega-automationtesting-robert-gonzalez
   ```

2. Crear y activar un entorno virtual:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux / Mac
   source venv/bin/activate
   ```

3. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

> No es necesario descargar ChromeDriver manualmente: `webdriver-manager` detecta la versión de Chrome instalada y descarga el driver correspondiente automáticamente. Se requiere tener Google Chrome instalado.

## Cómo ejecutar las pruebas

Ejecutar toda la suite con reporte HTML:

```bash
pytest tests/test_saucedemo.py -v --html=reports/reporte.html --self-contained-html
```

Ejecutar solo un grupo de pruebas (por clase):

```bash
pytest tests/test_saucedemo.py::TestLogin -v
pytest tests/test_saucedemo.py::TestCatalog -v
pytest tests/test_saucedemo.py::TestCart -v
```

El reporte se genera en `reports/reporte.html`. Si algún test falla, se guarda automáticamente una captura de pantalla en `reports/screenshots/`.

## Casos de prueba

| Clase | Test | Qué valida |
|---|---|---|
| `TestLogin` | `test_login_exitoso_redirige_a_pagina_de_inventario` | Login con `standard_user` redirige a `/inventory.html` y el título es "Products" |
| `TestCatalog` | `test_titulo_de_pagina_de_inventario_es_correcto` | El título de la página de inventario es correcto |
| `TestCatalog` | `test_existen_productos_visibles_en_el_catalogo` | Hay al menos un producto visible |
| `TestCatalog` | `test_elementos_importantes_de_la_interfaz_estan_presentes` | El menú y el filtro de orden están presentes |
| `TestCatalog` | `test_lista_nombre_y_precio_del_primer_producto` | Se obtiene correctamente el nombre y precio del primer producto |
| `TestCart` | `test_agregar_producto_incrementa_contador_del_carrito` | Al agregar un producto, el contador del carrito pasa a 1 |
| `TestCart` | `test_producto_agregado_aparece_correctamente_en_el_carrito` | El producto agregado aparece listado en la página del carrito |

Todos los tests son independientes entre sí: cada uno realiza su propio login mediante el helper `iniciar_sesion_y_obtener_inventario`, por lo que la falla de un test no afecta a los demás.
