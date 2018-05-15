
class Field:
    def __init__(self,name,colunm_type,primary_key,default):
        self.name = name
        self.column_type = colunm_type
        self.primary_key = primary_key
        self.default = default


class StringField(Field):
    def __init__(self,name,column_type='varchar(32)',primary_key=False,default=None):
        super().__init__(name,column_type,primary_key,default)

class IntegerField(Field):
    def __init__(self, name, column_type='int', primary_key=False, default=0):
        super().__init__(name, column_type, primary_key, default)