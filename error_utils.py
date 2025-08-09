import time
import logging
from functools import wraps
from logging_setup import get_logger

logger = get_logger(__name__)

def retry_on_exception(max_retries=3, initial_delay=1, backoff=2):
    """
    // [TASK]: Decorator to retry a function on exception
    // [GOAL]: Improve robustness of API calls and other potentially flaky operations
    """
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            retries = 0
            delay = initial_delay
            while retries < max_retries:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    logger.warning(f"Attempt {retries}/{max_retries} failed for {func.__name__}: {e}")
                    if retries < max_retries:
                        logger.info(f"Retrying in {delay} seconds...")
                        await asyncio.sleep(delay)
                        delay *= backoff
                    else:
                        log_and_raise(e, f"Max retries exceeded for {func.__name__}")
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            retries = 0
            delay = initial_delay
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    logger.warning(f"Attempt {retries}/{max_retries} failed for {func.__name__}: {e}")
                    if retries < max_retries:
                        logger.info(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
                        delay *= backoff
                    else:
                        log_and_raise(e, f"Max retries exceeded for {func.__name__}")
        
        # Check if the function is async or sync
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    return decorator

def log_and_raise(err, context="An error occurred"):
    """
    // [TASK]: Log an error and re-raise it
    // [GOAL]: Centralize error logging before re-raising
    """
    logger.error(f"{context}: {err}", exc_info=True)
    raise err
