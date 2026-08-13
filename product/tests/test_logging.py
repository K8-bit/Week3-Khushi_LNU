import logging

import pytest

from product.utils.logging_config import configure_logging


logger = logging.getLogger("product")


@pytest.fixture(autouse=True)
def reset_product_logging():
    root_logger = logging.getLogger()
    product_logger = logging.getLogger("product")

    original_root_handlers = root_logger.handlers[:]
    original_product_handlers = product_logger.handlers[:]
    original_root_level = root_logger.level
    original_product_level = product_logger.level

    yield

    for handler in root_logger.handlers[:]:
        if handler not in original_root_handlers:
            root_logger.removeHandler(handler)
            handler.close()

    for handler in product_logger.handlers[:]:
        if handler not in original_product_handlers:
            product_logger.removeHandler(handler)
            handler.close()

    root_logger.setLevel(original_root_level)
    product_logger.setLevel(original_product_level)


def test_configure_logging_writes_info_message(caplog):
    caplog.set_level(logging.INFO)

    configure_logging()
    logger.info("logging configuration test")

    assert "logging configuration test" in caplog.text
    assert "INFO" in caplog.text


