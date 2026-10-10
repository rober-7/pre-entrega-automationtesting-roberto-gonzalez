"""Fixtures y hooks compartidos por todos los tests.

- `driver`: crea y cierra el navegador Chrome para cada test (tests independientes).
- `pytest_runtest_makereport`: si un test falla, guarda automaticamente
  una captura de pantalla en reports/screenshots/.

Uso:
    pytest tests/                 # con ventana de Chrome visible
    pytest tests/ --headless      # sin interfaz grafica (mas rapido, ideal para CI)
"""

import os
from datetime import datetime

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")
SCREENSHOTS_DIR = os.path.join(REPORTS_DIR, "screenshots")


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Ejecuta el navegador Chrome sin interfaz grafica (modo headless).",
    )


@pytest.fixture
def driver(request):
    """Inicializa el WebDriver de Chrome para un test y lo cierra al finalizar."""
    options = Options()
    options.add_argument("--start-maximized")

    if request.config.getoption("--headless"):
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=service, options=options)

    yield navegador

    navegador.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Genera una captura de pantalla cuando un test falla durante su ejecucion."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        navegador = item.funcargs.get("driver")
        if navegador is not None:
            os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"{item.name}_{timestamp}.png"
            navegador.save_screenshot(os.path.join(SCREENSHOTS_DIR, nombre_archivo))
