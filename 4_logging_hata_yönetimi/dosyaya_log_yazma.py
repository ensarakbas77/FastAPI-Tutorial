"""
Amaç:
    - logları dosyaya yazma, logları kalıcı hale getirme ve log takibi yapabilme
"""

import logging

logging.basicConfig(
    filename="uygulama.log",
    level=logging.DEBUG,
    format="%(levelname)s | %(asctime)s | %(message)s",
    encoding="utf-8"
)

def log_ornekleri():
    logging.debug("debug kaydı")
    logging.info("info kaydı")
    logging.warning("warning kaydı")
    logging.error("error kaydı")
    logging.critical("critical kaydı")

if __name__ == "__main__":
    log_ornekleri()