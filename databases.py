import sqlite3
import datetime
import sys

create_table = lambda path: (open(f"static/sql/{path}.sql", 'r').read())  # ssh
GetLine = lambda: sys._getframe(1).f_lineno

Status: str = str
Statuses: dict = {
    "LoggerDataBase": {
        'LogText': str,
        'NullLog': '001',
        'NotFoundFile': '002',
    },
    'FeedBackDataBase': {
        'good': '101',
        'bad': '102',
        'null': '103',
        'NoSuchFile': '104',
        'CantCreateTable': '105',
    }
}


class LoggerDataBase(object):
    def __init__(self) -> None:
        self.files: dict = {
            "FeedBack": ["static/Logs/feedback.txt", "FeedBack"],
            "ViewsDataBase": ["static/Logs/ViewsDataBase.txt", "Views"],
        }

    def NewLog(self, *, _from=None, Log: str = None, line: int = 0, _type: str = None, data: dict = None) -> Status:
        if not Log: return Statuses['LoggerDataBase']['NullLog']
        if self.files.get(_from, None) is None: return Statuses['LoggerDataBase']['NotFoundFile']
        if _type is not None:
            if _type == 'simple':
                Log = self.GenerateSimpleLog(_from, Log, line, data)
            elif _type == 'error':
                Log = self.GenerateErrorLog(_from, Log, line, data)
        else:
            return Statuses['LoggerDataBase']['NullLog']

        with open(self.files[_from][0], "a", encoding='utf8') as LogFile:
            LogFile.write(Log + "\n")
            print(Log)

    def GenerateSimpleLog(self, _from: str, Log: str, line: int, data: dict = None) -> Statuses['LoggerDataBase'][
        'LogText']:
        return f"[ {self.files[_from][1]} ] : ( {datetime.datetime.today().strftime('%d.%m.%Y')} ~ {datetime.datetime.today().strftime('%H:%M:%S')} ) [ Line {str(line)}  in databases.py ] : {Log} ~ {data if data else None}"

    def GenerateErrorLog(self, _from: str, Log: str, line: int, data: dict = None) -> Statuses['LoggerDataBase'][
        'LogText']:
        return f"[ ERROR {self.files[_from][1]} ] : ( {datetime.datetime.today().strftime('%d.%m.%Y')} ~ {datetime.datetime.today().strftime('%H:%M:%S')} ) [ Line {str(line)}  in databases.py ] : {Log} ~ {data if data else None}"


Logs = LoggerDataBase()


class FeedBackDataBase(object):

    def __init__(self, *, path: str = 'static/databases/FeedBackDataBase.db') -> None:
        try:
            self.__connection__ = sqlite3.connect(path)
            self.__cursor = self.__connection__.cursor()
            self.__CreateTable()
            Logs.NewLog(_from='FeedBack', Log="Connect to Data Base Success", line=GetLine(), _type='simple')
        except Exception as e:
            Logs.NewLog(_from='FeedBack', Log=str(e), line=GetLine(), _type='error')

    def __CreateTable(self, *, TableName: str = 'FeedBackDataBase') -> None:
        try:
            self.__connection__.execute(create_table(TableName))
            self.__connection__.commit()
            Logs.NewLog(_from='FeedBack', Log="Create Table Data Base Success", line=GetLine(), _type='simple')
        except Exception as e:
            Logs.NewLog(_from='FeedBack', Log=str(e), line=GetLine(), _type='error')

    def NewFeedBack(self, category, fio, feedback, contact) -> Status:
        Error = False
        id = self.GetID() + 1
        try:
            sql = f"INSERT INTO FeedBack values ('{str(id)}', '{fio}', '{category}', '{contact}', '{feedback}')"
            try:
                self.__cursor.execute(sql)
                try:
                    self.__connection__.commit()
                except Exception as e:
                    Error = True
                    Logs.NewLog(_from='FeedBack', Log=str(e), line=GetLine(), _type='error', data={
                        'fio': fio,
                        'category': category,
                        'contact': contact,
                        'feedback': feedback
                    })
            except Exception as e:
                Error = True
                Logs.NewLog(_from='FeedBack', Log=str(e), line=GetLine(), _type='error', data={
                    'fio': fio,
                    'category': category,
                    'contact': contact,
                    'feedback': feedback
                })
        except Exception as e:
            Error = True
            Logs.NewLog(_from='FeedBack', Log=str(e), line=GetLine(), _type='error', data={
                'fio': fio,
                'category': category,
                'contact': contact,
                'feedback': feedback
            })
        Logs.NewLog(_from='FeedBack', Log="Success", line=GetLine(), _type='simple', data={
            'fio': fio,
            'category': category,
            'contact': contact,
            'feedback': feedback
        })
        return Statuses['FeedBackDataBase']['good'] if not Error else Statuses['FeedBackDataBase']['bad']

    def GetAllFeedBackData(self, category: int = None):
        if category is None:
            try:
                sql = 'SELECT * FROM FeedBack'
                result = self.__cursor.execute(sql).fetchall()
                Logs.NewLog(_from='FeedBack', Log="Success", line=GetLine(), _type='simple')
                return result
            except Exception as e:
                Logs.NewLog(_from='FeedBack', Log=str(e), line=GetLine(), _type='error')
        else:
            try:
                sql = f'SELECT * FROM FeedBack WHERE category = "{category}"'
                result = self.__cursor.execute(sql).fetchall()
                Logs.NewLog(_from='FeedBack', Log="Success", line=GetLine(), _type='simple')
                return result
            except Exception as e:
                Logs.NewLog(_from='FeedBack', Log=str(e), line=GetLine(), _type='error')

    def GetID(self):
        try:
            sql = "SELECT * FROM FeedBack"
            res = self.__cursor.execute(sql).fetchall()
            print(res)
            print(res[0])
            print(res[-1][0])
            return int(res[-1][0])
        except:
            return 1


class ViewsDataBase(object):
    def __init__(self, *, path: str = 'static/databases/ViewsDataBase.db') -> None:
        try:
            self.__connection__ = sqlite3.connect(path)
            self.__cursor = self.__connection__.cursor()
            Logs.NewLog(_from='ViewsDataBase', Log="Connect to Data Base Success", line=GetLine(), _type='simple')
        except Exception as e:
            Logs.NewLog(_from='ViewsDataBase', Log=str(e), line=GetLine(), _type='error')
        self.__CreateTable()

    def __CreateTable(self, *, TableName: str = 'ViewsDataBase') -> None:
        try:
            self.__connection__.execute(create_table(TableName))
            self.__connection__.commit()
            Logs.NewLog(_from='ViewsDataBase', Log="Create Table Data Base Success", line=GetLine(), _type='simple')
        except Exception as e:
            Logs.NewLog(_from='ViewsDataBase', Log=str(e), line=GetLine(), _type='error')

    def NewView(self, page: str = None) -> None:
        date = datetime.datetime.today().strftime('%d.%m.%Y')
        time = datetime.datetime.today().strftime('%H:%M:%S')
        sql = f'INSERT INTO Views values("{date}", "{time}", "{page}")'
        try:
            self.__cursor.execute(sql)
            self.__connection__.commit()
            Logs.NewLog(_from='ViewsDataBase', Log='New Write', line=GetLine(), _type='simple', data={
                'date': date,
                'time': time,
                'page': page
            })
        except Exception as e:
            Logs.NewLog(_from='ViewsDataBase', Log=str(e), line=GetLine(), _type='error', data={
                'date': date,
                'time': time,
                'page': page
            })
