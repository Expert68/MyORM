from 普通版.Mysql import *

class Field:
    def __init__(self,name,column_type,primary_key,default):
        self.name = name
        self.colunm_type = column_type
        self.primary_key = primary_key
        self.default = default

class Stringfield(Field):
    def __init__(self,name,column_type='varchar(200)',primary_key=False,default=None):
        super().__init__(name,column_type,primary_key,default)


class Integerfield(Field):
    def __init__(self,name,column_type='int',primary_key=False,default=0):
        super().__init__(name,column_type,primary_key,default)


class ModelMetaclass(type):
    def __new__(cls, name,bases,attrs):
        if name == 'Model':
            return type.__new__(name,bases,attrs)
        table_name = attrs.get('table_name',None)
        if not table_name:
            table_name = name
        primary_key = None
        mappings = {}
        for k,v in attrs.items():
            mappings[k] = v
            if v.primary_key:
                if primary_key:
                    raise TypeError('主键重复')
                primary_key = k

        for k in mappings.keys():
            attrs.pop(k)

        attrs['table_name'] = table_name
        attrs['primary_key'] = primary_key
        attrs['mappings'] = mappings
        return type.__new__(cls,name,bases,attrs)

class Models(dict,metaclass = ModelMetaclass):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise TypeError('没有该属性')

    @classmethod
    def select_one(cls,**kwargs):
        key = list(kwargs.keys())[0]
        value = kwargs[key]

        sql = 'select * from %s where %s = ?' %(cls.table_name,key)
        sql = sql.replace('?','%s')
        ms = mysql.singleton()
        res = ms.select(sql,value)
        if res:
            return cls(**res[0])
        else:
            return None

    # def save(self):
    #     ms = mysql.singleton()
    #     field = []
    #     params = []
    #     args = []
    #     for k, v in self.mappings.items():
    #         field.append(v.name)
    #         params.append('?')
    #         args.append(getattr(self, k, v.default_value))
    #
    #     sql = 'insert into %s (%s) values (%s)' % (self.table_name, ','.join(field), ','.join(params))
    #     sql.replace('?', '%s')
    #     ms.execute(sql, args)
    #
    # def update(self):
    #     ms = mysql.singleton()
    #     fields = []
    #     args = []
    #     pr = None
    #     for k, v in self.mappings.items():
    #         if v.primary_key:
    #             pr = getattr(self, k, v.default_value)
    #         else:
    #             fields.append(v.name + '=?')
    #             args.append(getattr(self, k, v.default_value))
    #     sql = "update %s set %s where %s = %s" % (
    #         self.table_name, ', '.join(fields), self.primary_key, pr)
    #
    #     sql = sql.replace('?', '%s')
    #     print(sql)
    #     ms.execute(sql, args)
class User(Models):
    table_name = 'user'
    id = Integerfield('id',primary_key=True,default=0)
    name = Stringfield('name')
    balance = Integerfield('balance')


if __name__ == '__main__':
    user = User.select_one(id=1)
    print(user.name)









