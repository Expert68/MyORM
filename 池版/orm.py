from 池版 import Mysql

class Field:
    def __init__(self,name,column_type,primary_key,default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default


class StringField(Field):
    def __init__(self,name,column_type='varchar(32)',primary_key=False,default=None):
        super().__init__(name,column_type,primary_key,default)

class IntegerField(Field):
    def __init__(self,name,column_type='int',primary_key=False,default=0):
        super().__init__(name,column_type,primary_key,default)


class Modelmetaclass(type):
    def __new__(cls, name,bases,attrs):
        if name == 'Model':
            return type.__new__(name,bases,attrs)
        table_name = attrs.get('table_name',None)
        if not table_name:
            table_name = name
        primary_key = None
        mapping = {}
        for k,v in attrs.items():
            if isinstance(v,Field):
                mapping[k] = v
                if v.primary_key:
                    if primary_key:
                        raise KeyError('主键重复')
                    primary_key = v

        for k in mapping:
            attrs.pop(k)

        attrs['table_name'] = table_name
        attrs['mapping'] = mapping
        attrs['primary_key'] = primary_key

        return type.__new__(name,bases,attrs)








class Model(dict,metaclass=Modelmetaclass):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def __getattr__(self, item):
        try:
            return self[item]
        except Exception:
            raise TypeError('没有该属性')

    def __setattr__(self, key, value):
        self[key] = value


    @classmethod
    def select_one(cls,**kwargs):
        ms = Mysql.Mysql()
        # kwargs = {'id' = 1}
        key = list(kwargs.keys())[0]
        #key = 'id' value = 1
        value = kwargs[key]

        #select * from user where id = ?
        sql = 'select * from %s where %s = ?' %(cls.table_name,key)
        sql.replace('?','%s')
        res = ms.execute(sql,value)
        if res:
            u = cls(**res[0])
            return u
        else:
            return None

    @classmethod
    def select_many(cls,**kwargs):
        ms = Mysql.Mysql()
        key = list(kwargs.keys())
        value = kwargs[key]
        if kwargs:
            sql = 'select * from %s where %s = ?' % (cls.table_name, key)
            sql.replace('?', '%s')
        else:
            sql = 'select * from %s' %(cls.table_name)
        res = ms.execute(sql,value)
        if res:
            list_obj = [cls(**r) for r in res]

            return list_obj
        else:
            return None


    def update(self):
        ms = Mysql.Mysql()

        filed = []
        primary = None
        args = []
        for k,v in self.mapping.items():
            if v.primary_key:
                primary.getattr(self,v.name,None)
            else:
                filed.append(v.name + '=?')
                args.append(getattr(self,v.name,v.default))
        sql = 'update %s set %s where %s=%s' %(self.table_name,','.join(filed),self.primary_key,primary)
        sql = sql.replace('?','%s')

        ms.execute(sql,args)

    def save(self):
        ms = Mysql.Mysql()
        filed = []
        values = []
        args = []
        for k,v in self.mapping.items():
            # table_name = 'user'
            # id = IntegerField('id', primary_key=True)
            # name = StringField('name')
            #mapping = {'id':IntegerField,'name':StringField}
            if not v.primary_key:
                #v=name
                filed.append(v.name)
                values.append('?')
                args= append(getattr(self,'name',None))

                user=User(

                )
                # user
                # getattr(user,'name')

                sql = 'insert into %s(%s) values (%s)' %(self.table_name,','.join(filed),','.join(values))
                sql = sql.replace('?','%s')
                ms.execute(sql,args)


class User(Model):
    table_name = 'user'
    id = IntegerField('id',primary_key=True)
    name = StringField('name')


