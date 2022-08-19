import os
from ..TableColumn import TableColumn
from ..iterable_file_writer import write_from_iterable


class TableSchemaGenerator:

    def __init__(self, project_root, slug, table_cols):
        self.project_root = project_root
        self.slug = slug
        self.table_cols = table_cols

    def create_schema(self):
        if not os.path.exists(f'{self.project_root}/app/database/schema'):
            os.mkdir(f'{self.project_root}/app/database/schema')

        with open(f'{self.project_root}/app/database/schema/{self.slug}TableSchema.php', 'w+') as slug_schema:

            write_from_iterable(slug_schema, [
                '<?php\n',
                f'class {self.slug}TableSchema extends TableSchema {{\n',

                '    const ID = "id";',
                '    const UID = "uid";',
            ], suffix='\n')

            for table_col in self.table_cols:
                table_col = TableColumn(table_col)
                slug_schema.write(f'    const {table_col.name.upper()} = "{table_col.name}";\n')

            write_from_iterable(slug_schema, [
                'const CREATED_AT = "created_at";',
                'const UPDATED_AT = "updated_at";\n',

                f'public function __construct() {{ parent::__construct({self.slug}Entity::TABLE_NAME); }}\n',

                'public function getBlueprint(): string {',
                '    return "CREATE TABLE IF NOT EXISTS " . $this->getTableName() . "(',
                '        " . self::ID . " INT AUTO_INCREMENT PRIMARY KEY NOT NULL,',
                '        " . self::UID . " VARCHAR(50) NOT NULL,',
            ], prefix=' ' * 4, suffix='\n')

            for table_col in self.table_cols:
                table_col = TableColumn(table_col)
                slug_schema.write(f'            " . self::{table_col.name.upper()} . " ')
                if table_col.get_type() is bool or table_col.get_type() is int:
                    slug_schema.write('INT')
                else:
                    slug_schema.write(f'VARCHAR({table_col.length})')
                if not table_col.nullable:
                    slug_schema.write(' NOT NULL')
                slug_schema.write(',\n')

            write_from_iterable(slug_schema, [
                '            " . self::CREATED_AT . " VARCHAR(100) NOT NULL,',
                '            " . self::UPDATED_AT . " VARCHAR(100) NOT NULL',
                '        )";',
                '    }',
                '}',
            ], suffix='\n')
