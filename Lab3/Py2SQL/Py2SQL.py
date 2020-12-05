import fdb
import os


class Py2SQL(object):
    __DBMS_name = "Firebird"

    def __init__(self):
        self.__connection = None
        self.__db_info = None

    def db_connect(self, db):
        self.__connection = fdb.connect(
            host=db.host,
            port=db.port,
            database=db.name,
            user=db.username,
            password=db.password
        )

        self.__db_info = db

    def db_disconnect(self):
        self.__connection.close()

    def db_engine(self):
        sql = """select rdb$get_context('SYSTEM', 'ENGINE_VERSION')
                 from rdb$database"""

        cursor = self.__connection.cursor()
        cursor.execute(sql)
        version = cursor.fetchone()[0]
        cursor.close()

        return f"{self.__DBMS_name} version {version}"

    def db_name(self):
        return os.path.split(self.__db_info.name)[1].split('.')[0]

    def db_size(self):
        sql = """select ((select count(*) from rdb$pages)) * 
                 (select mon$page_size from mon$database) / 1
                  from rdb$database;"""

        cursor = self.__connection.cursor()
        cursor.execute(sql)
        size = cursor.fetchone()[0] / 1000000
        cursor.close()

        return f"{size} MB"

    def db_tables(self):
        sql = """select a.RDB$RELATION_NAME
                 from RDB$RELATIONS a
                 where coalesce(RDB$SYSTEM_FLAG, 0) = 0 and RDB$RELATION_TYPE = 0"""

        cursor = self.__connection.cursor()
        cursor.execute(sql)
        tables = [x[0].strip() for x in cursor.fetchall()]
        cursor.close()

        return tables

    def db_table_structure(self, table):
        sql = f"""select row_number() over(), trim(rrf."RDB$FIELD_NAME"), trim(rt."RDB$TYPE_NAME") 
                  from RDB$RELATION_FIELDS rrf 
	                inner join RDB$FIELDS rf on rrf.RDB$FIELD_SOURCE = rf."RDB$FIELD_NAME" 
	                inner join RDB$TYPES rt on rf."RDB$FIELD_TYPE" = rt.RDB$TYPE 
                  where rt."RDB$FIELD_NAME" = 'RDB$FIELD_TYPE' and rrf."RDB$RELATION_NAME" = '{table}';"""

        cursor = self.__connection.cursor()
        cursor.execute(sql)
        columns = cursor.fetchall()
        cursor.close()

        return columns

    def db_table_size(self, table):
        sql = f"""select ((select count(*) from rdb$pages
                           where rdb$relation_id = (select rdb$relation_id
                                                    from rdb$relations
                                                    where rdb$relation_name = '{table}'))
                          ) * (select mon$page_size from mon$database) / 1
                  from rdb$database;"""

        cursor = self.__connection.cursor()
        cursor.execute(sql)
        size = cursor.fetchone()[0] / 1000000
        cursor.close()

        return f"{size} MB"

    def find_object(self, table, py_object):
        object_attributes = py_object.__dict__
        sql = f"""select * 
                  from {table}
                  where """

        i = 0
        for key in object_attributes:
            val = f"'{object_attributes[key]}'" if type(object_attributes[key]) == type("str") else object_attributes[
                key]
            and_str = "and" if i > 0 else ""
            sql += f"{and_str} {key} = {val} "
            i += 1

        main_sql = f"""select trim(rrf."RDB$FIELD_NAME"), trim(rt."RDB$TYPE_NAME") 
                      from RDB$RELATION_FIELDS rrf 
	                    inner join RDB$FIELDS rf on rrf.RDB$FIELD_SOURCE = rf."RDB$FIELD_NAME" 
	                    inner join RDB$TYPES rt on rf."RDB$FIELD_TYPE" = rt.RDB$TYPE 
                      where rt."RDB$FIELD_NAME" = 'RDB$FIELD_TYPE' and rrf."RDB$RELATION_NAME" = '{table}'
                            and exists ({sql});"""

        cursor = self.__connection.cursor()

        try:
            cursor.execute(main_sql)
        except:
            return []

        attributes = cursor.fetchall()
        cursor.close()

        result = []
        for attr in attributes:
            if attr[0].lower() in object_attributes:
                result.append((*attr, object_attributes[attr[0].lower()]))

        return result

    def find_objects_by(self, table, attributes):
        sql = f"""select * 
                          from {table}
                          where """
        where = ""

        i = 0
        for attr in attributes:
            val = f"'{attr[1]}'" if type(attr[1]) == str else attr[1]
            and_str = "and" if i > 0 else ""
            where += f"{and_str} {attr[0]} = {val} "
            i += 1

        sql += where
        main_sql = f"""select trim(rrf."RDB$FIELD_NAME"), trim(rt."RDB$TYPE_NAME") 
                              from RDB$RELATION_FIELDS rrf 
        	                    inner join RDB$FIELDS rf on rrf.RDB$FIELD_SOURCE = rf."RDB$FIELD_NAME" 
        	                    inner join RDB$TYPES rt on rf."RDB$FIELD_TYPE" = rt.RDB$TYPE 
                              where rt."RDB$FIELD_NAME" = 'RDB$FIELD_TYPE' and rrf."RDB$RELATION_NAME" = '{table}'
                                    and exists ({sql});"""

        cursor1 = self.__connection.cursor()

        try:
            cursor1.execute(main_sql)
        except:
            return []

        fields = cursor1.fetchall()
        cursor1.close()

        sql_results_count = f"""select count(id)
                              from {table}
                              where {where}"""
        cursor2 = self.__connection.cursor()

        try:
            cursor2.execute(sql_results_count)
        except:
            return []

        results_count = cursor2.fetchone()[0]
        cursor2.close()


        result = []
        for i in range(0, results_count):
            row_res = []
            for field in fields:
                sql_res = f"""select {field[0]}
                             from {table}
                             where {where}"""
                curr_cursor = self.__connection.cursor()
                curr_cursor.execute(sql_res)
                curr_res = curr_cursor.fetchall()[i][0]
                curr_cursor.close()
                row_res.append((*field, curr_res))
            result.append(row_res)

        return result