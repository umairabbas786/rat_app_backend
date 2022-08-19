import os


class ManifestBuilder:

    def __init__(self, project_root, eevee_config, manifest_path):
        self.eevee_config = eevee_config
        self.project_root = project_root
        self.manifest_path = manifest_path
        self.env_list = self.eevee_config.get_env_list()
        self.entities = list(map(  # UserEntity.php -> User  (Removing Suffixes)
            lambda e: e[:-10],
            os.listdir(f'{self.project_root}/app/database/entities')
        ))

    def build_manifest(self):
        with open(self.manifest_path, 'w+') as mf:
            mf.write('<?php\n\n')
            mf.write('class Manifest {\n')

            for env_item in self.env_list:
                if isinstance(env_item[1], str):  # value is of type string
                    mf.write(f'{" " * 4}const {env_item[0][2:-2].upper()} = "{env_item[1]}";\n')
                elif isinstance(env_item[1], bool):  # value is of type BOOL
                    mf.write(f'{" " * 4}const {env_item[0][2:-2].upper()} = {"true" if env_item[1] else "false"};\n')
                elif isinstance(env_item[1], int) or isinstance(env_item[1], float):  # value is of type int or float
                    mf.write(f'{" " * 4}const {env_item[0][2:-2].upper()} = {env_item[1]};\n')

            mf.write(f'\n{" " * 4}private const COMPOSER_VENDOR = [\n')
            mf.write(f'{" " * 8}\'dir_path\' => \'../\',\n')
            mf.write(f'{" " * 8}\'vendor\' => [\n')
            mf.write(f'{" " * 12}\'autoload\'\n')
            mf.write(f'{" " * 8}]\n')
            mf.write(f'{" " * 4}];\n\n')

            # LIBS START
            mf.write(f'{" " * 4}private const LIBS = [\n')
            mf.write(f'{" " * 8}\'dir_path\' => \'./libs\',\n')

            mf.write(f'{" " * 8}\'magician\' => [\n')
            for magician_lib in ['MagicianSpell::class', 'MagicianPasswordSpell::class', 'Magician::class']:
                mf.write(f'{" " * 12}{magician_lib},\n')
            mf.write(f'{" " * 8}],\n')

            mf.write(f'{" " * 8}\'query_builder\' => [\n')
            query_builder_libs = [
                'QueryType::class',
                'Query::class',
                'InsertQuery::class',
                'WhereApplicableQuery::class',
                'SelectQuery::class',
                'UpdateQuery::class',
                'DeleteQuery::class',
                'QueryBuilder::class'
            ]
            for query_builder_lib in query_builder_libs:
                mf.write(f'{" " * 12}{query_builder_lib},\n')
            mf.write(f'{" " * 8}],\n')

            mf.write(f'{" " * 8}\'db_libs\' => [\n')
            for table_lib in ['TableDao::class', 'TableSchema::class']:
                mf.write(f'{" " * 12}{table_lib},\n')
            mf.write(f'{" " * 8}],\n')

            mf.write(f'{" " * 4}];\n\n')
            # LIBS END

            """ DATABASE Entities Schema Factories Dao START """
            mf.write(f'{" " * 4}private const DATABASE = [\n')
            mf.write(f'{" " * 8}\'dir_path\' => \'./database\',\n')

            mf.write(f'{" " * 8}\'entities\' => [\n')
            for entity in self.entities:
                mf.write(f'{" " * 12}{entity}Entity::class,\n')
            mf.write(f'{" " * 8}],\n')

            mf.write(f'{" " * 8}\'schema\' => [\n')
            for entity in self.entities:
                mf.write(f'{" " * 12}{entity}TableSchema::class,\n')
            mf.write(f'{" " * 8}],\n')

            mf.write(f'{" " * 8}\'factories\' => [\n')
            for entity in self.entities:
                mf.write(f'{" " * 12}{entity}Factory::class,\n')
            mf.write(f'{" " * 8}],\n')

            mf.write(f'{" " * 8}\'dao\' => [\n')
            for entity in self.entities:
                mf.write(f'{" " * 12}{entity}Dao::class,\n')
            mf.write(f'{" " * 8}],\n')

            mf.write(f'{" " * 8}\'db\' => [\n')
            mf.write(f'{" " * 12}AppDB::class\n')
            mf.write(f'{" " * 8}],\n')
            mf.write(f'{" " * 4}];\n\n')
            # Database Entities Schema Factories Dao END -

            """ CORE START """
            mf.write(f'{" " * 4}private const CORE = [\n')
            mf.write(f'{" " * 8}\'dir_path\' => \'./\',\n')
            mf.write(f'{" " * 8}\'core\' => [\n')
            for core_item in ['Environment::class', 'ElectroResponse::class', 'ElectroMagicalExtensions::class', 'ElectroApi::class']:
                mf.write(f'{" " * 12}{core_item},\n')
            mf.write(f'{" " * 8}],\n')
            mf.write(f'{" " * 4}];\n\n')
            # CORE END

            """ UTILS START """
            mf.write(f'{" " * 4}private const UTILS = [\n')
            mf.write(f'{" " * 8}\'dir_path\' => \'./utils\',\n')
            mf.write(f'{" " * 8}\'image_uploader\' => [\n')
            mf.write(f'{" " * 12}ImageUploader::class,\n')
            mf.write(f'{" " * 8}],\n')
            mf.write(f'{" " * 4}];\n\n')
            # UTILS END

            """ MODELS START """
            mf.write(f'{" " * 4}private const MODELS = [\n')
            mf.write(f'{" " * 8}\'dir_path\' => \'./\',\n')
            mf.write(f'{" " * 8}\'models\' => [\n')
            models = list(map(
                lambda m: m.split('.php')[0],
                os.listdir(f'{self.project_root}/app/models')
            ))
            for model in models:
                mf.write(f'{" " * 12}{model}::class,\n')
            mf.write(f'{" " * 8}]\n')
            mf.write(f'{" " * 4}];\n\n')
            # Models END

            """ AGENTS START """
            mf.write(f'{" " * 4}private const AGENTS = [\n')
            mf.write(f'{" " * 8}\'dir_path\' => \'./\',\n')
            mf.write(f'{" " * 8}\'agents\' => [\n')
            api_agents = list(map(
                lambda a: a.split('.php')[0],
                os.listdir(f'{self.project_root}/app/agents')
            ))
            for api_agent in api_agents:
                mf.write(f'{" " * 12}{api_agent}::class,\n')
            mf.write(f'{" " * 8}]\n')
            mf.write(f'{" " * 4}];\n\n')
            # Agents END

            manifest_content = [
                '    public static function getAppSystemRoot(): string {',
                '        return substr(self::devisePath(\'../\'), 0, -1);',
                '    }\n',

                '    public static function devisePath($path): string {',
                '        $root_path = explode(\'/\', __DIR__);\n',

                '        if (substr($path, 0, 2) === \'./\') {',
                '            $path = substr($path, 2);',
                '        } else {',
                '            while (substr($path, 0, 3) === \'../\') {',
                '                $path = substr($path, 3);',
                '                array_pop($root_path);',
                '            }',
                '        }\n',

                '        return implode(\'/\', $root_path) . \'/\' . $path;',
                '    }\n',

                '    private function requireItems(array $package) {',
                '        foreach ($package as $key => $value) {',
                '            if ($key !== \'dir_path\') {',
                '                foreach ($value as $module) {',
                '                    $dir_path = $package[\'dir_path\'];',
                '                    $path = $dir_path;',
                '                    if ($dir_path !== \'./\' && $dir_path !== \'../\') {',
                '                        $path = $path . \'/\';',
                '                    }',
                '                    $path = $path . $key . \'/\' . $module . \'.php\';',
                '                    require self::devisePath($path) . \'\';',
                '                }',
                '            }',
                '        }',
                '    }\n',

                '    private function loadRequirements() {',
                '        self::requireItems(self::COMPOSER_VENDOR);',
                '        self::requireItems(self::LIBS);',
                '        self::requireItems(self::DATABASE);',
                '        self::requireItems(self::CORE);',
                '        self::requireItems(self::UTILS);',
                '        self::requireItems(self::MODELS);',
                '        self::requireItems(self::AGENTS);',
                '    }\n',

                '    private function __construct() {',
                '        $this->loadRequirements();',
                '    }\n',

                '    public static function create() {',
                '        new Manifest();',
                '    }',
                '}'
            ]
            for manifest_line in manifest_content:
                mf.write(f'{manifest_line}\n')
            mf.write('\nManifest::create();\n')
