import os
import sys
from .create_compressed_build import CreateCompressedBuild
from ..route_creator import RouteCreator
from ..database_class_builder import DatabaseClassBuilder
from ..electro_colors import alert_danger
from shutil import copyfile
from shutil import copytree


class ProductionBuild:

    def __init__(self, eevee_config, project_root, args):
        self.eevee_config = eevee_config
        self.project_root = project_root
        self.args = args
        if len(self.args) > 1:
            if len(self.args[1:]) > 4:
                sys.exit(alert_danger('Invalid number of build parameters, Maximum 4 are accepted.'))
            for arg in args[1:]:
                if arg not in ['--tar', '--zip', '--rar', '--7z']:
                    sys.exit(alert_danger(f"Invalid build argument: {arg}"))

        if os.path.exists(f'{self.project_root}/build'):
            os.system(f'rm -rf "{self.project_root}/build"')
            os.mkdir(f'{self.project_root}/build')

        self.ignore = [
            '.idea',
            '.gitignore',
            'data',
            '.git',
            'eevee',
            'build',
            'composer.json',
            'composer.lock',
            'eevee_config.json',
            'SERVER.zip',
            'SERVER.tar.gz',
            'SERVER.7z',
            'SERVER.rar'
        ]

        for item in os.listdir(self.project_root):
            if item not in self.ignore:
                if os.path.isdir(f'{self.project_root}/{item}'):
                    copytree(f'{self.project_root}/{item}', f'{self.project_root}/build/{item}')
                else:
                    copyfile(f'{self.project_root}/{item}', f'{self.project_root}/build/{item}')

        os.system(f'rm -rf "{self.project_root}/build/app/android"')
        os.system(f'rm -rf "{self.project_root}/build/app/database/design"')
        os.system(f'rm -rf "{self.project_root}/build/app/database/structures"')

        DatabaseClassBuilder(
            self.project_root,
            self.eevee_config.get_production_db_hostname(),
            self.eevee_config.get_production_db_username(),
            self.eevee_config.get_production_db_password(),
            self.eevee_config.get_production_db_name(),
            f'{self.project_root}/build/app/database/db/AppDB.php'
        ).build_db()

        os.system(f'rm "{self.project_root}/build/app/libs/query_builder/QueryBuilderUsage.txt"')
        os.system(f'rm "{self.project_root}/build/app/utils/image_uploader/ImageUploaderUsage.txt"')

        """ Writing Routes content in route files under build directory """
        for agent in os.listdir(f'{self.project_root}/app/agents'):
            RouteCreator(agent).create_route(f'{self.project_root}/build')

        if len(self.args) == 1 or '--tar' in self.args:
            CreateCompressedBuild(self.project_root).create()  # Creates TarBall Build (default)

        if len(self.args) > 1:
            for arg in self.args[1:]:
                if arg == '--zip':
                    CreateCompressedBuild(self.project_root, tar=False, extension='.zip', build_type='ZIP').create()
                if arg == '--rar':
                    CreateCompressedBuild(self.project_root, tar=False, extension='.rar', build_type='RAR').create()
                if arg == '--7z':
                    CreateCompressedBuild(self.project_root, tar=False, extension='.7z', build_type='7-ZIP').create()

        os.system(f'rm -rf "{self.project_root}/build"')
