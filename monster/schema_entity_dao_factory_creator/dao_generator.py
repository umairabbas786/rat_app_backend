import os
from ..case_converters import pascal_to_camel
from ..case_converters import snake_to_pascal
from ..TableColumn import TableColumn


class DaoGenerator:

    def __init__(self, project_root, slug, table_cols):
        self.project_root = project_root
        self.slug = slug
        self.table_cols = table_cols

    def create_dao(self):
        if not os.path.exists(f'{self.project_root}/app/database/dao'):
            os.mkdir(f'{self.project_root}/app/database/dao')

        start_tag = '<***_ELECTRO_GENERATED_DO_NOT_REMOVE_***>'
        end_tag = '</***_ELECTRO_GENERATED_DO_NOT_REMOVE_***>'

        electro_dao_content = [
            f'\n'
            f'    public function __construct(mysqli $connection) {{ // {start_tag}\n',
            f'        parent::__construct($connection);\n',
            f'    }} // {end_tag}\n',
            f'\n',
            f'    public function insert{self.slug}({self.slug}Entity ${pascal_to_camel(self.slug)}Entity): ?{self.slug}Entity {{ // {start_tag}\n',
            f'        $query = QueryBuilder::withQueryType(QueryType::INSERT)\n',
            f'            ->withTableName({self.slug}Entity::TABLE_NAME)\n',
            f'            ->columns([\n',
            f'                {self.slug}TableSchema::UID,\n'
        ]

        for table_col in self.table_cols:
            table_col = TableColumn(table_col)
            electro_dao_content.append(f'                {self.slug}TableSchema::{table_col.name.upper()},\n')

        electro_dao_content.extend([
            f'                {self.slug}TableSchema::CREATED_AT,\n',
            f'                {self.slug}TableSchema::UPDATED_AT\n',
            f'            ])\n',
            f'            ->values([\n',
            f'                $this->escape_string(${pascal_to_camel(self.slug)}Entity->getUid()),\n'
        ])

        for table_col in self.table_cols:
            table_col = TableColumn(table_col)
            if table_col.get_type() is bool:
                values_getter_text = f'${self.slug[0].lower() + self.slug[1:]}Entity->is{snake_to_pascal(table_col.name)}()'
                wrap_bool_getter_text = f'$this->wrapBool({values_getter_text})'
                if table_col.nullable:
                    electro_dao_content.append(f'{" " * 16}{values_getter_text} === null ? null : {wrap_bool_getter_text},\n')
                else:
                    electro_dao_content.append(f'{" " * 16}{wrap_bool_getter_text},\n')
            else:
                values_getter_text = f'${self.slug[0].lower() + self.slug[1:]}Entity->get{snake_to_pascal(table_col.name)}()'
                escape_str_getter_text = f'$this->escape_string({values_getter_text})'
                if table_col.nullable:
                    electro_dao_content.append(f'{" " * 16}{values_getter_text} === null ? null : {escape_str_getter_text},\n')
                else:
                    electro_dao_content.append(f'{" " * 16}{escape_str_getter_text},\n')

        electro_dao_content.extend([
            f'                $this->escape_string(${pascal_to_camel(self.slug)}Entity->getCreatedAt()),\n',
            f'                $this->escape_string(${pascal_to_camel(self.slug)}Entity->getUpdatedAt())\n',
            f'            ])\n',
            f'            ->generate();\n\n',

            f'        $result = mysqli_query($this->getConnection(), $query);\n\n',

            f'        if ($result) {{\n',
            f'            return $this->get{self.slug}WithId($this->inserted_id());\n',
            f'        }}\n',
            f'        return null;\n',
            f'    }} // {end_tag}\n\n',

            f'    public function get{self.slug}WithId(string $id): ?{self.slug}Entity {{ // {start_tag}\n',
            f'        $query = QueryBuilder::withQueryType(QueryType::SELECT)\n',
            f'             ->withTableName({self.slug}Entity::TABLE_NAME)\n',
            f'             ->columns([\'*\'])\n',
            f'             ->whereParams([\n',
            f'                [{self.slug}TableSchema::ID, \'=\', $this->escape_string($id)]\n',
            f'             ])\n',
            f'             ->generate();\n\n',

            f'        $result = mysqli_query($this->getConnection(), $query);\n\n',

            f'        if ($result && $result->num_rows >= 1) {{\n',
            f'            return {self.slug}Factory::mapFromDatabaseResult(mysqli_fetch_assoc($result));\n',
            f'        }}\n',
            f'        return null;\n',
            f'    }} // {end_tag}\n\n',

            f'    public function get{self.slug}WithUid(string $uid): ?{self.slug}Entity {{ // {start_tag}\n',
            f'        $query = QueryBuilder::withQueryType(QueryType::SELECT)\n',
            f'             ->withTableName({self.slug}Entity::TABLE_NAME)\n',
            f'             ->columns([\'*\'])\n',
            f'             ->whereParams([\n',
            f'                [{self.slug}TableSchema::UID, \'=\', $this->escape_string($uid)]\n',
            f'             ])\n',
            f'             ->generate();\n\n',

            f'        $result = mysqli_query($this->getConnection(), $query);\n\n',

            f'        if ($result && $result->num_rows >= 1) {{\n',
            f'            return {self.slug}Factory::mapFromDatabaseResult(mysqli_fetch_assoc($result));\n',
            f'        }}\n',
            f'        return null;\n',
            f'    }} // {end_tag}\n\n',

            # Getter for All
            f'    public function getAll{self.slug}(): array {{ // {start_tag}\n',
            f'        $query = QueryBuilder::withQueryType(QueryType::SELECT)\n',
            f'             ->withTableName({self.slug}Entity::TABLE_NAME)\n',
            f'             ->columns([\'*\'])\n',
            f'             ->generate();\n\n',

            f'        $result = mysqli_query($this->getConnection(), $query);\n\n',

            f'        ${self.slug[0].lower() + self.slug[1:]}s = [];\n\n',

            f'        if ($result) {{\n',
            f'            while($row = mysqli_fetch_assoc($result)) {{\n',
            f'                array_push(${pascal_to_camel(self.slug)}s, {self.slug}Factory::mapFromDatabaseResult($row));\n',
            f'            }}\n',
            f'        }}\n',
            f'        return ${self.slug[0].lower() + self.slug[1:]}s;\n',
            f'    }} // {end_tag}\n\n',

            f'    public function update{self.slug}({self.slug}Entity ${pascal_to_camel(self.slug)}Entity): ?{self.slug}Entity {{ // {start_tag}\n',
            f'        $query = QueryBuilder::withQueryType(QueryType::UPDATE)\n',
            f'            ->withTableName({self.slug}Entity::TABLE_NAME)\n',
            f'            ->updateParams([\n'
        ])

        """ GENERATING UPDATERS """

        for table_col in self.table_cols:
            table_col = TableColumn(table_col)
            if table_col.get_type() is bool:
                values_getter_text = f'${self.slug[0].lower() + self.slug[1:]}Entity->is{snake_to_pascal(table_col.name)}()'
                wrap_bool_getter_text = f'$this->wrapBool({values_getter_text})'
                if table_col.nullable:
                    params_str = f'{values_getter_text} === null ? null : {wrap_bool_getter_text}'
                else:
                    params_str = f'{wrap_bool_getter_text}'
            else:
                values_getter_text = f'${self.slug[0].lower() + self.slug[1:]}Entity->get{snake_to_pascal(table_col.name)}()'
                escape_str_getter_text = f'$this->escape_string({values_getter_text})'
                if table_col.nullable:
                    params_str = f'{values_getter_text} === null ? null : {escape_str_getter_text}'
                else:
                    params_str = escape_str_getter_text
            electro_dao_content.append(f'{" " * 16}[{self.slug}TableSchema::{table_col.name.upper()}, {params_str}],\n')

        params_str = f'$this->escape_string(${self.slug[0].lower() + self.slug[1:]}Entity->getCreatedAt())'
        electro_dao_content.append(f'{" " * 16}[{self.slug}TableSchema::CREATED_AT, {params_str}],\n')
        params_str = f'$this->escape_string(${self.slug[0].lower() + self.slug[1:]}Entity->getUpdatedAt())'
        electro_dao_content.append(f'{" " * 16}[{self.slug}TableSchema::UPDATED_AT, {params_str}]\n')
        electro_dao_content.append(f'{" " * 12}])\n')
        electro_dao_content.append(f'{" " * 12}->whereParams([\n')
        params_str = f'$this->escape_string(${self.slug[0].lower() + self.slug[1:]}Entity->getId())'
        electro_dao_content.append(f'{" " * 16}[{self.slug}TableSchema::ID, \'=\', {params_str}]\n')
        electro_dao_content.append(f'{" " * 12}])\n')
        electro_dao_content.append(f'{" " * 12}->generate();\n\n')

        electro_dao_content.append(f'{" " * 8}$result = mysqli_query($this->getConnection(), $query);\n\n')

        electro_dao_content.append(f'{" " * 8}if ($result) {{\n')
        electro_dao_content.append(f'{" " * 12}return $this->get{self.slug}WithId(${pascal_to_camel(self.slug)}Entity->getId());\n')
        electro_dao_content.append(f'{" " * 8}}}\n')
        electro_dao_content.append(f'{" " * 8}return null;\n')
        electro_dao_content.append(f'{" " * 4}}} // {end_tag}\n\n')

        """ GENERATING DELETE METHODS """
        electro_dao_content.append(f'    public function delete{self.slug}({self.slug}Entity ${pascal_to_camel(self.slug)}Entity) {{ // {start_tag}\n')
        electro_dao_content.append(f'        $query = QueryBuilder::withQueryType(QueryType::DELETE)\n')
        electro_dao_content.append(f'            ->withTableName({self.slug}Entity::TABLE_NAME)\n')
        electro_dao_content.append(f'            ->whereParams([\n')
        params_str = f'$this->escape_string(${pascal_to_camel(self.slug)}Entity->getId())'
        electro_dao_content.append(f'{" " * 16}[{self.slug}TableSchema::ID, \'=\', {params_str}]\n')
        electro_dao_content.append(f'{" " * 12}])\n')
        electro_dao_content.append(f'{" " * 12}->generate();\n\n')

        electro_dao_content.append(f'{" " * 8}while(true) {{\n')
        electro_dao_content.append(f'{" " * 12}if (mysqli_query($this->getConnection(), $query)) {{\n')
        electro_dao_content.append(f'{" " * 16}break;\n')
        electro_dao_content.append(f'{" " * 12}}}\n')
        electro_dao_content.append(f'{" " * 8}}}\n')
        electro_dao_content.append(f'{" " * 4}}} // {end_tag}\n\n')

        electro_dao_content.extend([
            f'    public function deleteAll{self.slug}s() {{ // {start_tag}\n',
            f'        $query = QueryBuilder::withQueryType(QueryType::DELETE)\n',
            f'            ->withTableName({self.slug}Entity::TABLE_NAME)\n',
            f'            ->generate();\n\n',
            f'        while(true) {{\n'
            f'            if (mysqli_query($this->getConnection(), $query)) {{\n'
            f'                break;\n'
            f'            }}\n'
            f'        }}\n'
            f'    }} // {end_tag}\n\n',
        ])

        user_defined_dao_content = []

        if os.path.exists(f'{self.project_root}/app/database/dao/{self.slug}Dao.php'):
            with open(f'{self.project_root}/app/database/dao/{self.slug}Dao.php', 'r') as slug_dao:
                dao_lock_mode = None
                for lin in slug_dao.readlines()[4:]:
                    if dao_lock_mode == start_tag:  # LOCKED
                        if end_tag in lin:
                            dao_lock_mode = None
                    else:  # Not Locked
                        if start_tag in lin:
                            dao_lock_mode = start_tag
                        else:
                            user_defined_dao_content.append(lin)

        user_defined_dao_content_functions = []

        is_function_started = False
        user_defined_dao_content_function = []
        while len(user_defined_dao_content) != 0:
            lin = user_defined_dao_content[0]
            user_defined_dao_content.pop(0)
            if lin[:19] == '    public function' and not is_function_started:
                is_function_started = True
                user_defined_dao_content_function = [lin]
                continue
            if lin[:5] == '    }':
                is_function_started = False
                user_defined_dao_content_function.append(lin)
                user_defined_dao_content_functions.append(user_defined_dao_content_function)
                continue
            if is_function_started:
                user_defined_dao_content_function.append(lin)

        for user_defined_dao_function in user_defined_dao_content_functions:
            for lin in user_defined_dao_function:
                electro_dao_content.append(lin)
            electro_dao_content.append('\n')

        with open(f'{self.project_root}/app/database/dao/{self.slug}Dao.php', 'w+') as slug_dao:
            slug_dao.write('<?php\n\n')
            slug_dao.write(f'class {self.slug}Dao extends TableDao {{\n\n')

            has_end = False
            for lin in electro_dao_content:
                slug_dao.write(lin)
                if '}\n' == lin:
                    has_end = True
            if not has_end:
                slug_dao.write('}\n')
