from .iterable_file_writer import write_from_iterable


class EnvironmentGenerator:

    def __init__(self, project_root, data_dirs):
        self.project_root = project_root
        self.data_dirs = data_dirs

    def build_environment(self):
        with open(f'{self.project_root}/app/core/Environment.php', 'w+') as environment_file:
            environment_file.write('<?php\n\n')
            environment_file.write('trait Environment {\n\n')

            write_from_iterable(environment_file, [
                '    private function getServerNameWithAvailableProtocol(): string {',
                '        $server_name = $_SERVER["SERVER_NAME"];',
                "        return 'http' . (isset($_SERVER['HTTPS']) ? 's' : '') . '://' . $server_name;",
                '    }\n',

                '    private function getServerUrlUptoDataDir(): string {',
                '        return $this->getServerNameWithAvailableProtocol() . "/data";',
                '    }\n',

                '    public function getDataDirectoryPath(): string {',
                '        return Manifest::getAppSystemRoot() . "/data";',
                '    }\n'
            ], suffix='\n')

            for data_dir in self.data_dirs:
                write_from_iterable(environment_file, [
                    f'    /**',
                    f'     * <{data_dir[0]}>',
                    f'     */',
                    f'    public function get{data_dir[0]}DirPath(): string {{',
                    f'        return $this->getDataDirectoryPath() . \'{data_dir[1]}\';',
                    f'    }}\n',
                    f'    public function createLinkFor{data_dir[0]}(string $file_name): string {{',
                    f'        return $this->getServerUrlUptoDataDir() . "{data_dir[1]}/" . $file_name;',
                    f'    }}',
                    f'    /** ----------------- </{data_dir[0]}> */\n',
                ], suffix='\n')

            environment_file.write('}\n')
