from shutil import which

SELENIUM_DRIVER_NAME = 'chrome'
SELENIUM_DRIVER_EXECUTABLE_PATH = which('chromedriver')
SELENIUM_DRIVER_ARGUMENTS=['--headless']  # Puedes remover '--headless' para ver el navegador en acción

DOWNLOADER_MIDDLEWARES = {
    'scrapy_selenium.SeleniumMiddleware': 800,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    'scrapy_proxies.RandomProxy': 100,
}

# Lista de proxies
PROXY_LIST = 'path/to/proxy/list.txt'  # archivo de texto con proxies, uno por línea
PROXY_MODE = 0  # 0 significa rotación aleatoria de proxies

# Añade tus cabeceras aquí
DEFAULT_REQUEST_HEADERS = {
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    # Añade otras cabeceras necesarias
}
