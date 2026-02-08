from __future__ import annotations

import logging
import os
import time
from dataclasses import dataclass


@dataclass
class ProcessConfig:
    name: str
    command: str


def main() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
    logger = logging.getLogger("watchdog")
    logger.info("Watchdog placeholder started. Configure PM2 for production.")
    while True:
        time.sleep(60)


if __name__ == "__main__":
    main()
