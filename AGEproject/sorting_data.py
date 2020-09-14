import json
import pymysql
import os,datetime,time
from settings import DATABASE


error_list = []

def get_all_file(file_dir='.'):
    anime_file_list = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.json':
                anime_file_list.append(os.path.join(root, file))
    return anime_file_list

def test_db():
    try:
        db = pymysql.connect(DATABASE['ip'], DATABASE['user'], DATABASE['pass'], DATABASE['schema'])
        cursor = db.cursor()
        cursor.execute("SELECT VERSION()")
        data = cursor.fetchone()
        print("Database version : %s " % data)
        db.close()
    except :
        raise Exception("数据库连接失败")

def insert_data(table, data):
    db = pymysql.connect(DATABASE['ip'], DATABASE['user'], DATABASE['pass'], DATABASE['schema'])
    # db = pymysql.connect("192.168.43.193", "root", "root", "test")
    cursor = db.cursor()
    # 修复时间错误
    fix_time = data['time'].split('-')
    if len(fix_time) == 2:
        fix_time.append("01")
    elif fix_time[0] == "暂无":
        fix_time[0] = '0000'
        fix_time.append('00')
        fix_time.append('00')
    elif len(fix_time) == 1:
        fix_time.append('01')
        fix_time.append('01')
    if fix_time[-1] == "" or int(fix_time[-1]) > 31:
        fix_time[-1] = "01"
    data['time'] = "-".join(fix_time)

    keys = ",".join(data.keys())
    values = ",".join(['%s'] * len(data))
    sql = """insert into {table}({keys})
            values ({values})""".format(table=table, keys=keys, values=values)
    try:
        # print(sql)
        cursor.execute(sql, tuple(data.values()))
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
        print("{} : 该记录插入失败".format(data['chinese_name']))
        error_list.append(data['chinese_name'])
        time.sleep(3)
    finally:
        db.close()


def sorting_data_to_one_file(data):
    with open('anime.json', 'w', encoding='UTF-8') as f:
        json.dump(data, f, ensure_ascii=False)

def create_table(table_name):
    db = pymysql.connect(DATABASE['ip'], DATABASE['user'], DATABASE['pass'], DATABASE['schema'])
    cursor = db.cursor()
    create_table_sql = """CREATE TABLE `{}` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `chinese_name` varchar(255) DEFAULT NULL,
        `region` varchar(255) DEFAULT NULL,
        `anime_type` varchar(255) DEFAULT NULL,
        `original_name` varchar(255) DEFAULT NULL,
        `other_name` varchar(255) DEFAULT NULL,
        `detail` text DEFAULT NULL,
        `author` varchar(255) DEFAULT NULL,
        `company` varchar(255) DEFAULT NULL,
        `time` date DEFAULT NULL,
        `status` varchar(255) DEFAULT NULL,
        `plot_type` varchar(255) DEFAULT NULL,
        `tag` varchar(255) DEFAULT NULL,
        `website` varchar(255) DEFAULT NULL,
        `origin_url` varchar(255) DEFAULT NULL,
        `download_site1` varchar(255) CHARACTER SET latin1 DEFAULT NULL,
        `download_site2` varchar(255) CHARACTER SET latin1 DEFAULT NULL,
        `pwd1` varchar(255) DEFAULT NULL,
        `pwd2` varchar(255) DEFAULT NULL,
        PRIMARY KEY (`id`)
        ) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;""".format(table_name)
    check_sql = "DROP TABLE IF EXISTS `{}`;".format(table_name)
    try:
        cursor.execute(check_sql)
        cursor.execute(create_table_sql)
        db.commit()
    except:
        db.rollback()
        raise Exception("创建表失败")
    db.close()

if __name__ == '__main__':

    test_db()
    table_name = "anime_test"
    choice = input("是否创建表? y/n  ")
    if choice == 'y':
        create_table(table_name)
    with open("../anime.json", 'r', encoding='UTF-8') as f:
        data = json.load(f)
        # print(len(data))
    for i in data:
        print("当前插入: " + i['chinese_name'])
        insert_data(table_name, i)
    print("完成自动插入")
    print("以下记录自动插入失败，请手动处理")
    print(error_list)
