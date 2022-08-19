class TableStructureStub:

    def __init__(self, entity_name):
        self.entity_name = entity_name

    def get_code(self):
        return [
            '{\n',
            f'    "__table_name__": "{self.entity_name.lower()}s",\n',
            '    "__cols__": [\n',
            '        [ "first_name", "" , 50 ],\n',
            '        [ "last_name", "" , 50 ],\n',
            '        [ "username", "" , 50 ],\n',
            '        [ "email", "" , 50 ],\n',
            '        [ "magician_cipher", "" , 150 ],\n',
            '        [ "magician_iv", "" , 50 ],\n',
            '        [ "magician_key", "" , 50 ],\n',
            '        [ "magician_abracadabra", "" , 40 ],\n',
            '        [ "fcm_token?", "" , 170 , null],\n',
            '        [ "account_verified" , true , null, false],\n',
            '        [ "blocked" , true , null, false],\n',
            '        [ "posts", 1 , null, 0],\n',
            '        [ "rating", 5.0, 170 , 0.0]\n',
            '    ]\n',
            '} \n',
        ]
