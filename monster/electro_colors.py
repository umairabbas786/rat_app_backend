from colorama import Fore, Back, Style


def get_alert_spacing(text):
    return " " * (len(text) + 2)


def alert_danger(text):
    return f'{Back.RED}{Fore.WHITE}{get_alert_spacing(text)}\n {text} \n{get_alert_spacing(text)}{Style.RESET_ALL}'


def alert_success(text):
    return f'{Back.BLACK}{Fore.CYAN}{get_alert_spacing(text)}\n {text} \n{get_alert_spacing(text)}{Style.RESET_ALL}'


def alert_warning(text):
    return f'{Back.YELLOW}{Fore.BLACK}{get_alert_spacing(text)}\n {text} \n{get_alert_spacing(text)}{Style.RESET_ALL}'


def alert_primary(text):
    return f'{Back.BLUE}{Fore.WHITE}{get_alert_spacing(text)}\n {text} \n{get_alert_spacing(text)}{Style.RESET_ALL}'


def alert_info(text):
    return f'{Back.CYAN}{Fore.BLACK}{get_alert_spacing(text)}\n {text} \n{get_alert_spacing(text)}{Style.RESET_ALL}'


def alert_secondary(text):
    return f'{Back.WHITE}{Fore.BLACK}{get_alert_spacing(text)}\n {text} \n{get_alert_spacing(text)}{Style.RESET_ALL}'


def text_danger(text):
    return f'{Back.RED}{Fore.WHITE}{text}{Style.RESET_ALL}'


def text_success(text):
    return f'{Back.BLACK}{Fore.CYAN}{text}{Style.RESET_ALL}'


def text_warning(text):
    return f'{Back.YELLOW}{Fore.BLACK}{text}{Style.RESET_ALL}'


def text_primary(text):
    return f'{Back.BLUE}{Fore.WHITE}{text}{Style.RESET_ALL}'


def text_info(text):
    return f'{Back.CYAN}{Fore.BLACK}{text}{Style.RESET_ALL}'


def text_secondary(text):
    return f'{Back.WHITE}{Fore.BLACK}{text}{Style.RESET_ALL}'
