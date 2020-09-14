import json
import pymysql
import os
from settings import DATABASE


def get_all_file(file_dir='.'):
    anime_file_list = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.json':
                anime_file_list.append(os.path.join(root, file))
    return anime_file_list

def test_db(db):
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()
    print("Database version : %s " % data)
    db.close()

def insert_data(table, data):
    db = pymysql.connect(DATABASE['ip'], DATABASE['user'], DATABASE['pass'], DATABASE['schema'])
    # db = pymysql.connect("192.168.43.193", "root", "root", "test")
    cursor = db.cursor()

    keys = ",".join(data.keys())
    values = ",".join(['%s'] * len(data))
    sql = """insert into {table}({keys})
            values ({values})""".format(table=table, keys=keys, values=values)
    try:
        # print(sql)
        cursor.execute(sql, tuple(data.values()))
        print("success!")
        db.commit()
    except:
        db.rollback()
    db.close()


def sorting_data_to_one_file(data):
    with open('anime.json', 'w', encoding='UTF-8') as f:
        json.dump(data, f, ensure_ascii=False)


if __name__ == '__main__':
   
    with open("anime.json", 'r', encoding='UTF-8') as f:
        data = json.load(f)
        # print(len(data))

    # test_db(db)
    a = 1
    for i in data:
        print(a)
        a += 1
        insert_data("anime", i)
    print("all success!")
