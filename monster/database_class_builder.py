import os


class DatabaseClassBuilder:

    def __init__(self, project_root, hostname, username, password, db_name, db_path):
        self.project_root = project_root
        self.hostname = hostname
        self.username = username
        self.password = password
        self.db_name = db_name
        self.db_path = db_path
        self.entities = list(map(  # UserEntity.php -> User  (Removing Suffixes)
            lambda e: e[:-10],
            os.listdir(f'{self.project_root}/app/database/entities')
        ))

    def build_db(self):
        with open(self.db_path, 'w+') as db:
            db.write('<?php\n\n')
            db.write('class AppDB {\n')
            db.write(f'{" " * 4}const HOSTNAME = "{self.hostname}";\n')
            db.write(f'{" " * 4}const USERNAME = "{self.username}";\n')
            db.write(f'{" " * 4}const PASSWORD = "{self.password}";\n')
            db.write(f'{" " * 4}const DATABASE = "{self.db_name}";\n\n')
            db.write(f'{" " * 4}private mysqli $conn;\n\n')

            for model in self.entities:
                db.write(f'{" " * 4}private {model}Dao ${model[0].lower() + model[1:]}Dao;\n')

            db.write(f'\n{" " * 4}function __construct() {{\n')
            db.write(f'{" " * 8}$temp_conn = mysqli_connect(self::HOSTNAME, self::USERNAME, self::PASSWORD, '
                     f'self::DATABASE);\n\n')

            db.write(f'{" " * 8}if (!$temp_conn) {{\n')
            db.write('{}die("{}");\n'.format(' ' * 12, "Couldn't Connect to DB!"))
            db.write(f'{" " * 8}}}\n\n')

            db.write(f'{" " * 8}$this->conn = $temp_conn;\n\n')

            for model in self.entities:
                db.write(f'{" " * 8}mysqli_query($this->conn, (new {model}TableSchema())->getBlueprint());'
                         f' // Creates {model} Table\n')
                db.write(f'{" " * 8}$this->{model[0].lower() + model[1:]}Dao = new {model}Dao($this->conn);'
                         f' // Initialize {model} Dao\n\n')

            db.write(f'{" " * 4}}}\n\n')

            db.write(f'{" " * 4}public function getConnection(): mysqli {{\n')
            db.write(f'{" " * 8}return $this->conn;\n')
            db.write(f'{" " * 4}}}\n\n')

            db.write(f'{" " * 4}public function closeConnection() {{\n')
            db.write(f'{" " * 8}$this->conn->close();\n')
            db.write(f'{" " * 4}}}\n\n')

            for model in self.entities:
                db.write(f'{" " * 4}public function get{model}Dao(): {model}Dao {{\n')
                db.write(f'{" " * 8}return $this->{model[0].lower() + model[1:]}Dao;\n')
                end_line = '\n' if model != self.entities[-1] else ''
                db.write(f'{" " * 4}}}\n{end_line}')

            db.write('}\n\n')
