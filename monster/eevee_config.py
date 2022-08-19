import os
import sys
import json
from .electro_colors import alert_warning


class EeveeConfig:

    def __init__(self, project_root):
        self.project_root = project_root
        self.config_file = f'{self.project_root}/eevee_config.json'

        if not os.path.exists(self.config_file):
            sys.exit(alert_warning("EEVEE CONFIG FILE COULDN'T BE FOUND!"))

        with open(self.config_file, 'r') as eevee_config:
            self.config = json.loads(eevee_config.read())

    def get_production_db_hostname(self):
        return self.config['__production_database__']['__hostname__']

    def get_production_db_username(self):
        return self.config['__production_database__']['__username__']

    def get_production_db_password(self):
        return self.config['__production_database__']['__password__']

    def get_production_db_name(self):
        return self.config['__production_database__']['__database__']

    def get_local_db_hostname(self):
        return self.config['__local_database__']['__hostname__']

    def get_local_db_username(self):
        return self.config['__local_database__']['__username__']

    def get_local_db_password(self):
        return self.config['__local_database__']['__password__']

    def get_local_db_name(self):
        return self.config['__local_database__']['__database__']

    def get_ftp_hostname(self):
        return self.config['__ftp_config__']['__hostname__']

    def get_ftp_username(self):
        return self.config['__ftp_config__']['__username__']

    def get_ftp_password(self):
        return self.config['__ftp_config__']['__password__']

    def get_ssh_hostname(self):
        return self.config['__ssh_config__']['__hostname__']

    def get_ssh_username(self):
        return self.config['__ssh_config__']['__username__']

    def get_ssh_password(self):
        return self.config['__ssh_config__']['__password__']

    def get_ssh_port(self):
        return self.config['__ssh_config__']['__port__']

    def get_env_list(self):
        return self.config['__env__']

    def get_data_dirs(self):
        return self.config['__data_dirs__']

    def get_android_app_config(self):
        return self.config['__android_app_config__']

    def get_android_app_package_names(self):
        return self.config['__android_app_config__']['__package_names__']

    def get_tink_master_key(self):
        return self.config['__android_app_config__']['__tink_master_key__']

    def get_android_tink_secret_key(self):
        return self.config['__android_app_config__']['__secret_key__']

    def get_server_base_url(self):
        return self.config['__android_app_config__']['__server_base_url__']
