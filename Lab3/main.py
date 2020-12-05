from Py2SQL.Py2SQL import Py2SQL
from Py2SQL.db.Database import Database
from entity.Dog import Dog
from entity.Dog2 import Dog2
from Py2SQL.generators.FileGenerator import FileGenerator

if __name__ == '__main__':
    db = Database('localhost', 3050, 'path', 'SYSDBA', 'admin')
    dbms = Py2SQL()
    dbms.db_connect(db)
    print(dbms.db_engine())
    print(dbms.db_name())
    print(dbms.db_size())
    print(dbms.db_tables())
    print(dbms.db_table_structure('DOGS'))
    print(dbms.db_table_size('CATS'))

    dog = Dog(1, "Toto", 12, "black")
    attributes = [('age', 12), ('id', 1)]
    print(dbms.find_object('DOGS', dog))
    print(dbms.find_objects_by('DOGS', attributes))

