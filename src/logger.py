from colors import Colors

def log_debug(message):
    print(message)

def log_info(message):
    print(Colors.GREEN + message + Colors.RESET)

def log_warning(message):
    print(Colors.YELLOW + message + Colors.RESET)

def log_error(message):
    print(Colors.RED + message + Colors.RESET)