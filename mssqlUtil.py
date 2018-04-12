# coding=utf-8
import pymssql


class MssqlHelper(object):

    def __init__(self):
        self._setting = Mssql_Setting
        self._conn = None
        self._cursor = None

    @property
    def conn(self):
        if self._conn is not None:
            return self._conn;
        self._conn = pymssql.connect(server=self._setting.server, database=self._setting.database,
                                     user=self._setting.user, password=self._setting.pwd, port=self._setting.port)
        return self._conn

    @property
    def cursor(self):
        if self._cursor is not None:
            return self._cursor
        self._cursor = self.conn.cursor()
        return self._cursor

    def execute(self, sql, parameters=()):
        self.cursor.execute(sql, parameters)

    def commit_tran(self):
        """提交事务"""
        self._conn.commit()

    def rollback_tran(self):
        """回滚事务"""
        self._conn.rollback()

    def close_cursor(self):
        if self._cursor is not None:
            self._cursor.close()

    def close(self):
        if self._conn is not None:
            self._conn.close()


class MssqlSetting(object):

    def __init__(self, server, port, user, pwd, database):
        self._host = server
        self._port = port
        self._user = user
        self._password = pwd
        self._database = database

    @property
    def user(self):
        return self._user

    @property
    def server(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def pwd(self):
        return self._password

    @property
    def database(self):
        return self._database


Mssql_Setting = MssqlSetting(server='192.168.100.20', port=20433, user='yjq', pwd='yjqyjq', database='YJQ')