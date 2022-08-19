
class RouteCreator:

    def __init__(self, agent):
        self.agent = agent
        self.route = ''

    # Provides a name with case change, PascalCase to snake_case
    # RegisterUser.php => register_user.php
    def get_route_name(self):
        self.route = ''
        for i in range(len(self.agent)):
            if self.agent[i].isupper() and i > 0:
                self.route = self.route + '_{}'.format(self.agent[i])
            else:
                self.route = self.route + self.agent[i]
        return self.route.lower()

    # Writes Content to Route File,
    # destination param = destination directory, where route will be created
    def create_route(self, destination):
        with open(f'{destination}/{self.get_route_name()}', 'w+') as routeFile:
            routeFile.write('<?php require "app/Manifest.php";\n')
            routeFile.write('(new {}())->launch();'.format(self.agent[:-4]))
