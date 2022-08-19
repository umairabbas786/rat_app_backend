import os


class SshConnection:

    def __init__(self, eevee_config):
        self.eevee_config = eevee_config
        self.hostname = self.eevee_config.get_ssh_hostname()
        self.username = self.eevee_config.get_ssh_username()
        self.password = self.eevee_config.get_ssh_password()
        self.port = self.eevee_config.get_ssh_port()

    def connect(self):
        print("Launching SSH Session")
        print(f'SSH PASSWORD: {self.password}')
        os.system(f'ssh {self.username}@{self.hostname} -p {self.port}')
