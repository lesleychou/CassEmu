from enum import Enum


KEY_SPACE = 'ycsb'
TABLE_NAME = 'usertable'
KEY = 'y_id'


class QueryType(Enum):
    READ = 'read'
    UPDATE = 'update'
    SCAN = 'scan'
    INSERT = 'insert'

INSERT_query = """
    insert into usertable (y_id, field0)
    values(%s, %s)
"""

UPDATE_query = "update usertable set field0=%s where y_id=%s"

READ_query = "select * from usertable where y_id=%s limit 1"

SCAN_query = "select * from usertable where token(y_id) >= token(%s)"
