import sys
from tabulate import tabulate
from .electro_colors import alert_warning
from .electro_colors import text_primary


class HelpManual:

    def __init__(self):
        self.content = [
            (('-v', 'Displays current version of eevee'), './eevee -v'),
            (('-h', 'Shows this help menu'), './eevee -h'),
            (('-u', 'Updates eevee to latest version'), './eevee -u'),
            (('--create-agent', 'Creates an Agent'), './eevee --create-agent RegisterUser'),
            (('--create-table', 'Create a Table'), './eevee --create-table User'),
            (('--glance', 'Displays array pushed class objects names'), './eevee --glance YourAgentName'),
            (('--serve', 'Serves App Locally on specified PORT'), './eevee --serve 8000'),
            (
                (
                    '--build',
                    'Creates Production Build, tarball is default, other formats can be set.'
                ),
                './eevee --build --tar --zip --rar --7z'
            ),
            (
                (
                    '--ftp',
                    'Establishes ftp connection with config defined in eevee_config.json'
                ),
                './eevee --ftp'
            ),
            (
                (
                    '--ssh',
                    'Establishes ssh connection with config defined in eevee_config.json'
                ),
                './eevee --ssh'
            )
        ]

    def show(self):
        print(tabulate(
            list(map(lambda x: [
                x[0][0],
                text_primary(f' {x[1]} '),
                x[0][1]
            ], self.content)),
            headers=['Arguments', 'Usage', 'Description']
        ))

    def kill_if_any_invalid_argument(self, args):
        if args[0] not in list(map(lambda t: t[0][0], self.content)):
            sys.exit(alert_warning(f"Invalid Argument {args[0]}"))
