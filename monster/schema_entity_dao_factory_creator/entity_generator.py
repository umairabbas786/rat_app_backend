import os
from ..TableColumn import TableColumn
from ..iterable_file_writer import write_from_iterable
from ..case_converters import snake_to_pascal
from ..php_utils import get_php_val_of_python_val


class EntityGenerator:

    def __init__(self, project_root, slug, table_name, table_cols):
        self.project_root = project_root
        self.slug = slug
        self.table_name = table_name
        self.table_cols = table_cols

    def _get_getter_func_definition(self, table_col):
        if table_col.get_type() is bool:
            return f'    public function is{snake_to_pascal(table_col.name)}(): {table_col.php_type} {{\n'
        return f'    public function get{snake_to_pascal(table_col.name)}(): {table_col.php_type} {{\n'

    def create_entity(self):
        if not os.path.exists(f'{self.project_root}/app/database/entities'):
            os.mkdir(f'{self.project_root}/app/database/entities')

        with open(f'{self.project_root}/app/database/entities/{self.slug}Entity.php', 'w+') as slug_entity:
            write_from_iterable(slug_entity, [
                '<?php\n',
                f'class {self.slug}Entity {{',
                f'    const TABLE_NAME = "{self.table_name}";\n'
                f'    private string $id;',
                f'    private string $uid;'
            ], suffix='\n')

            table_cols_with_default_values = []
            table_cols_without_default_values = []

            for table_col in self.table_cols:
                table_col = TableColumn(table_col)
                slug_entity.write(f'    private {table_col.php_type} ${table_col.name};\n')
                if table_col.has_default_value:
                    table_cols_with_default_values.append(table_col)
                else:
                    table_cols_without_default_values.append(table_col)

            slug_entity.write(f'    private string $created_at;\n')
            slug_entity.write(f'    private string $updated_at;\n\n')

            params_str = 'string $uid, '

            for table_col in table_cols_without_default_values:
                params_str = f'{params_str}{table_col.php_type} ${table_col.name}, '

            params_str = f'{params_str} string $created_at, string $updated_at'

            if len(table_cols_with_default_values) > 0:
                params_str = f'{params_str}, '

            for table_col in table_cols_with_default_values:
                params_str = f'{params_str}{table_col.php_type} ${table_col.name} = '
                params_str = params_str + get_php_val_of_python_val(table_col.default_value)
                if table_col != table_cols_with_default_values[-1]:
                    params_str = f'{params_str}, '

            slug_entity.write(f'    public function __construct({params_str}) {{\n')
            slug_entity.write(f'        $this->uid = $uid;\n')

            for table_col in table_cols_without_default_values:
                slug_entity.write(f'        $this->{table_col.name} = ${table_col.name};\n')

            for table_col in table_cols_with_default_values:
                slug_entity.write(f'        $this->{table_col.name} = ${table_col.name};\n')

            write_from_iterable(slug_entity, [
                '    $this->created_at = $created_at;',
                '    $this->updated_at = $updated_at;',
                '}\n',

                'public function getId(): ?string {',
                '    return $this->id;',
                '}\n',

                'public function setId(string $id): void {',
                '    $this->id = $id;',
                '}\n',

                'public function getUid(): string {',
                '    return $this->uid;',
                '}\n',

                'public function setUid(string $uid): void {',
                '    $this->uid = $uid;',
                '}\n'
            ], prefix=' ' * 4, suffix='\n')

            for table_col in table_cols_without_default_values:
                slug_entity.write(self._get_getter_func_definition(table_col))
                slug_entity.write(f'        return $this->{table_col.name};\n')
                slug_entity.write(f'    }}\n\n')

                params_str = f'{table_col.php_type} ${table_col.name}'
                slug_entity.write(f'    public function set{snake_to_pascal(table_col.name)}({params_str}): void {{\n')
                slug_entity.write(f'        $this->{table_col.name} = ${table_col.name};\n')
                slug_entity.write(f'    }}\n\n')

            for table_col in table_cols_with_default_values:
                slug_entity.write(self._get_getter_func_definition(table_col))
                slug_entity.write(f'        return $this->{table_col.name};\n')
                slug_entity.write(f'    }}\n\n')

                params_str = f'{table_col.php_type} ${table_col.name} = '
                params_str = params_str + get_php_val_of_python_val(table_col.default_value)

                slug_entity.write(f'    public function set{snake_to_pascal(table_col.name)}({params_str}): void {{\n')
                slug_entity.write(f'        $this->{table_col.name} = ${table_col.name};\n')
                slug_entity.write(f'    }}\n\n')

            write_from_iterable(slug_entity, [
                'public function getCreatedAt(): string {',
                '    return $this->created_at;',
                '}\n',

                'public function setCreatedAt(string $created_at): void {',
                '    $this->created_at = $created_at;',
                '}\n',

                'public function getUpdatedAt(): string {',
                '    return $this->updated_at;',
                '}\n',

                'public function setUpdatedAt(string $updated_at): void {',
                '    $this->updated_at = $updated_at;',
                '}\n',
            ], prefix=' ' * 4, suffix='\n')

            slug_entity.write('}\n')
