import os
import sys
import distro
from shutil import which
from .electro_colors import alert_danger
from .electro_colors import alert_primary
import pkg_resources


class DependenciesChecker:

    def __init__(self):
        self.tabulate = 'tabulate'
        self.colorama = 'colorama'
        self.p7zip = '7z'
        self.rar = 'rar'
        self.php = 'php'

    def check(self):
        pip_packages = [pkg.key for pkg in pkg_resources.working_set]
        if self.colorama not in pip_packages:
            print(alert_primary(f'{self.colorama} module is not installed, starting installation now...'))
            os.system(f'pip install {self.colorama}')

        if 'tabulate' not in pip_packages:
            print(alert_primary(f'{self.tabulate} module is not installed, starting installation now...'))
            os.system(f'pip install {self.tabulate}')

        if which(self.php) is None:
            sys.exit(alert_danger('php interpreter not found in PATH'))

        if which(self.p7zip) is None:
            if distro.name() == 'Manjaro Linux':
                print("7-ZIP is not installed, Enter Your Password to install it.")
                os.system('sudo pacman -Sy && sudo pacman -S p7zip')
            else:
                sys.exit(alert_danger("7z not found in path, please install it."))

        if which(self.rar) is None:
            if distro.name() == 'Manjaro Linux':
                print("RAR is not installed, Enter Your Password to install it.")
                os.system('sudo pacman -Sy && sudo pamac install rar')
            else:
                sys.exit(alert_danger("rar not found in path, please install it."))
