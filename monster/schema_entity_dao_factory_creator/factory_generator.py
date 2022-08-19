import os
from ..case_converters import snake_to_pascal
from ..TableColumn import TableColumn
from ..iterable_file_writer import write_from_iterable


class FactoryGenerator:

    def __init__(self, project_root, slug, table_cols):
        self.project_root = project_root
        self.slug = slug
        self.table_cols = table_cols

    def _get_param_str(self, table_col):
        main_getter_phrase = f'$result[{self.slug}TableSchema::{table_col.name.upper()}]'

        if table_col.get_type() is bool:
            params_str = f'((int) {main_getter_phrase}) === 1'
        elif table_col.get_type() is float:
            params_str = f'(float) {main_getter_phrase}'
        elif table_col.get_type() is int:
            params_str = f'(int) {main_getter_phrase}'
        else:
            params_str = main_getter_phrase

        if table_col.nullable:
            params_str = f'{main_getter_phrase} === null ? null : {params_str}'

        return params_str

    def create_factory(self):
        if not os.path.exists(f'{self.project_root}/app/database/factories'):
            os.mkdir(f'{self.project_root}/app/database/factories')

        with open(f'{self.project_root}/app/database/factories/{self.slug}Factory.php', 'w+') as slug_factory:
            write_from_iterable(slug_factory, [
                '<?php\n\n',
                f'class {self.slug}Factory {{',
            ], suffix='\n')

            table_cols_with_default_values = []
            table_cols_without_default_values = []

            for table_col in self.table_cols:
                table_col = TableColumn(table_col)
                if table_col.has_default_value:
                    table_cols_with_default_values.append(table_col)
                else:
                    table_cols_without_default_values.append(table_col)

            write_from_iterable(slug_factory, [
                f'/**',
                f' * @param string[]|null|false $result',
                f' * @return {self.slug}Entity',
                f' */',
                f'public static function mapFromDatabaseResult($result): {self.slug}Entity {{',
                f'    $entity = new {self.slug}Entity(',
                f'        $result[{self.slug}TableSchema::UID],',
            ], prefix=' ' * 4, suffix='\n')

            for table_col in table_cols_without_default_values:
                slug_factory.write(f'{" " * 12}{self._get_param_str(table_col)},\n')

            write_from_iterable(slug_factory, [
                f'        $result[{self.slug}TableSchema::CREATED_AT],',
                f'        $result[{self.slug}TableSchema::UPDATED_AT]',
                f'    );',
                f'    $entity->setId($result[{self.slug}TableSchema::ID]);',
            ], prefix=' ' * 4, suffix='\n')

            for table_col in table_cols_with_default_values:
                setter_name = f'set{snake_to_pascal(table_col.name)}'
                slug_factory.write(f'{" " * 8}$entity->{setter_name}({self._get_param_str(table_col)});\n')

            write_from_iterable(slug_factory, [
                f'{" " * 8}return $entity;',
                '    }',
                '}',
            ], suffix='\n')
