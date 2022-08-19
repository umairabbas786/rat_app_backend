import os
from ..electro_colors import text_danger


# Creates Compressed Production Build,
# TarBall is default, can be changed to build in zip, rar and 7z
class CreateCompressedBuild:

    def __init__(self, project_root, tar=True, extension='.tar.gz', build_type='TarBall'):
        self.project_root = project_root
        self.tar = tar
        self.extension = extension
        self.build_type = build_type
        self.skip = False

    def create(self):
        if os.path.exists(f"{self.project_root}/SERVER{self.extension}"):
            while True:
                choice = input(f"SERVER{self.extension} production build exists. overwrite? [y/N]: ")
                if choice not in ['y', 'Y', 'N', 'n', '']:
                    print(text_danger("Wrong Input!"))
                    continue
                if choice in ['y', 'Y']:
                    os.system(f'rm "{self.project_root}/SERVER{self.extension}"')
                else:
                    self.skip = True
                break
        if self.skip:
            print(f"Skipped {self.build_type} Build.")
        else:
            print(f"Creating {self.build_type} Build...")
            if self.tar:
                os.system(f'cd "{self.project_root}/build" && tar -czf ../SERVER{self.extension} *')
            else:
                if self.extension == '.rar':
                    os.system(f'cd "{self.project_root}/build" && rar a ../SERVER{self.extension} *')
                else:
                    os.system(f'cd "{self.project_root}/build" && 7z a ../SERVER{self.extension} *')
            print(f"{self.build_type} Build Success: {self.project_root}/SERVER{self.extension}")
