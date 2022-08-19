
class TableColumn:

    def __init__(self, column_detail):
        self.name = column_detail[0] if column_detail[0][-1] != '?' else column_detail[0][0:-1]
        self.nullable = '?' == column_detail[0][-1]  # checking if ? is at end
        self.type_sample = column_detail[1]
        """ Creating PHP TYPE variable """
        self.php_type = '?' if self.nullable else ''
        if type(column_detail[1]) is str:
            self.php_type = f'{self.php_type}string'
        elif type(column_detail[1]) is int:
            self.php_type = f'{self.php_type}int'
        elif type(column_detail[1]) is float:
            self.php_type = f'{self.php_type}float'
        elif type(column_detail[1]) is bool:
            self.php_type = f'{self.php_type}bool'
        self.length = column_detail[2]
        self.has_default_value = len(column_detail) == 4
        self.default_value = column_detail[-1] if self.has_default_value else None

    def get_type(self):
        return type(self.type_sample)
