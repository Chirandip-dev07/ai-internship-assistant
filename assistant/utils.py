import sys
import logging

class Colors:
    """Standard ANSI escape sequences for CLI coloring."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def setup_logger(name: str) -> logging.Logger:
    """Sets up a clean, centralized logger."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(f'{Colors.WARNING}[%(levelname)s] %(message)s{Colors.ENDC}')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

def print_header(title: str, color: str = Colors.CYAN) -> None:
    """Prints a beautiful, colored section header."""
    print(f"\n{color}{Colors.BOLD}" + "═" * 50)
    print(f"{title.center(50)}")
    print("═" * 50 + f"{Colors.ENDC}\n")

def get_user_input(prompt: str) -> str:
    """Prompts the user with a distinct colored icon."""
    return input(f"{Colors.GREEN}👉 {prompt}{Colors.ENDC}\n> ").strip()

def print_success(message: str) -> None:
    print(f"{Colors.GREEN}✔ {message}{Colors.ENDC}")

def print_error(message: str) -> None:
    print(f"{Colors.FAIL}✖ {message}{Colors.ENDC}")

def print_info(message: str) -> None:
    print(f"{Colors.CYAN}ℹ {message}{Colors.ENDC}")
