# utils/logger.py

import time


def timestamp():
    return time.strftime("[%Y-%m-%d %H:%M:%S]")


def info(msg: str):
    print(f"\033[94m{timestamp()} [INFO]\033[0m {msg}")


def success(msg: str):
    print(f"\033[92m{timestamp()} [SUCCESS]\033[0m {msg}")


def warn(msg: str):
    print(f"\033[93m{timestamp()} [WARN]\033[0m {msg}")


def error(msg: str):
    print(f"\033[91m{timestamp()} [ERROR]\033[0m {msg}")
