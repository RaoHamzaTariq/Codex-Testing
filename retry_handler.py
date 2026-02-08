from __future__ import annotations

import functools
import logging
import time
from collections.abc import Callable
from typing import Any, TypeVar


LOGGER = logging.getLogger("retry_handler")
T = TypeVar("T")


def with_retry(max_attempts: int = 3, base_delay: int = 1, max_delay: int = 60) -> Callable[[Callable[..., T]], Callable[..., T]]:
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            attempt = 0
            delay = base_delay
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as exc:  # noqa: BLE001
                    attempt += 1
                    if attempt >= max_attempts:
                        LOGGER.exception("Max retry attempts reached: %s", exc)
                        raise
                    LOGGER.warning("Retrying after error: %s", exc)
                    time.sleep(min(delay, max_delay))
                    delay *= 2

        return wrapper

    return decorator


@with_retry(max_attempts=3, base_delay=1, max_delay=60)
def api_call() -> None:
    """Placeholder for API calls requiring retry logic."""
    raise NotImplementedError("Replace with real API call")
