# -*- coding: UTF-8 -*-
# Author  : LiuShuai
# Time    : 2020/2/24 16:21
# File    : staff_manage.py

import os

from tabulate import tabulate

DB_FILE = "staff.db"
COLUMNS = ['id', 'name', 'age', 'phone', 'dept', 'enrolled_date']


def print_log(msg, log_type="info"):
    if log_type == 'info':
        print("\033[32;1m%s\033[0m" % msg)
    elif log_type == 'error':
        print("\033[31;1m%s\033[0m" % msg)


def load_db(db_file):
    """
    加载员工信息表，并转成指定的格式
    :param db_file:
    :return:
    """
    data = {}
    for i in COLUMNS:
        data[i] = []
    f = open(db_file, "r", encoding="utf-8")
    for line in f:
        # print(line.split(','))
        staff_id, name, age, phone, dept, enrolled_date = line.split(',')
        data['id'].append(staff_id)
        data['name'].append(name)
        data['age'].append(age)
        data['phone'].append(phone)
        data['dept'].append(dept)
        data['enrolled_date'].append(enrolled_date)

    return data


def save_db():
    """把内存数据存回磁盘"""
    f = open("%s.new" % DB_FILE, 'w', encoding='utf-8')
    for index, staff_id in enumerate(STAFF_DATA['id']):
        row = []
        for col in COLUMNS:
            row.append(STAFF_DATA[col][index])
        f.write(",".join(row))
    f.close()

    os.remove(DB_FILE)
    os.rename("%s.new" % DB_FILE, DB_FILE)


STAFF_DATA = load_db(DB_FILE)  # 程序启动就执行


def op_gt(column, condtion_val):
    """

    :param column:  eg. age
    :param condtion_val: eg. 22
    :return: [[id,name,age,phone],...]  返回类似这样的列表结构
    """
    matched_records = []
    for index, val in enumerate(STAFF_DATA[column]):  # "age" : [23,22,34,12,3]
        if float(val) > float(condtion_val):  # 代表匹配上了,转成浮点类型进行大小匹配
            # print("match",val)
            # matched_records.append(STAFF_DATA['id'][index])
            # matched_records.append(STAFF_DATA['name'][index])
            # matched_records.append(STAFF_DATA['age'][index])
            record = []
            for col in COLUMNS:
                record.append(STAFF_DATA[col][index])
            matched_records.append(record)
    # print("matched records",matched_records)
    return matched_records
    # else:
    #     print("没走",val,condtion_val)


def op_lt(column, condtion_val):
    matched_records = []
    for index, val in enumerate(STAFF_DATA[column]):  # "age" : [23,22,34,12,3]
        if float(val) < float(condtion_val):  # 代表匹配上了,转成浮点类型进行大小匹配
            record = []
            for col in COLUMNS:
                record.append(STAFF_DATA[col][index])
            matched_records.append(record)
    return matched_records


def op_eq(column, condtion_val):
    matched_records = []
    for index, val in enumerate(STAFF_DATA[column]):  # "age" : [23,22,34,12,3]
        if val == condtion_val:  # 代表匹配上了,转成浮点类型进行大小匹配
            record = []
            for col in COLUMNS:
                record.append(STAFF_DATA[col][index])
            matched_records.append(record)
    return matched_records


def op_like(column, condtion_val):
    matched_records = []
    for index, val in enumerate(STAFF_DATA[column]):  # "age" : [23,22,34,12,3]
        if condtion_val in val:  # 代表匹配上了,转成浮点类型进行大小匹配
            record = []
            for col in COLUMNS:
                record.append(STAFF_DATA[col][index])
            matched_records.append(record)
    return matched_records


def syntax_where(clause):
    """
    解析where条件，并过滤数据
    :param clause: eg. age>22
    :return:
    """
    operators = {
        '>': op_gt,
        '<': op_lt,
        '=': op_eq,
        'like': op_like,
    }

    for op_key, op_func in operators.items():
        if op_key in clause:
            column, val = clause.split(op_key)
            matched_data = op_func(column.strip(), val.strip())  # 真正的查询数据
            # print_log(matched_data)
            return matched_data

    else:  # 只有for循环执行完成，且中间没有被break的情况才执行，表示没匹配上任何条件公式
        print_log("语法错误：where条件只能支持['>'|'<'|'='|'like']", 'error')


def syntax_find(data_set, query_clause):
    """
    解析查询语句，并从data_set中打印指定的列
    :param data_set:  eg. [['1', 'Alex Li', '22', '13651054608', 'IT', '2013-04-01\n'],
     ['8', 'Kevin Chen', '22', '13151054603', 'Sales', '2013-04-01\n']]
    :param query_clause: eg. find name,age from staff_table
    :return:
    """
    filter_cols_tmp = query_clause.split("from")[0][4:].split(",")
    # print_log(filter_cols_tmp)  == 下文中的headers 替代
    filter_cols = [i.strip() for i in filter_cols_tmp]  # 得到我们想要的columns   [' name', 'age ']

    if '*' in filter_cols[0]:
        print(tabulate(data_set, headers=COLUMNS, tablefmt="grid"))
    else:
        reformat_data_set = []
        for row in data_set:
            filtered_vals = []  # 把要打印的字段存放在这个列表里
            for col in filter_cols:
                col_index = COLUMNS.index(col)  # 拿到列的索引，依此取出每条记录里对应索引的值
                filtered_vals.append(row[col_index])
            reformat_data_set.append(filtered_vals)

        # print(reformat_data_set)   下文中的tabulate 替代

        # for r in reformat_data_set:
        #     print(r)
        print(tabulate(reformat_data_set, headers=filter_cols, tablefmt="grid"))
    print_log("匹配到%s条数据!" % len(data_set), 'info')


# def syntax_delete(data_set, query_clause):
#     pass


def syntax_update(data_set, query_clause):
    """

    :param data_set:
    :param query_clause:  eg. update staff_table set age=25
    :return:
    """
    formula_raw = query_clause.split('set')
    if len(formula_raw) > 1:  # 说明有set关键字
        col_name, new_val = formula_raw[1].strip().split('=')  # age=25
        # col_index = COLUMNS.index(col_name)
        # 思路：循环data_set 取到每条记录的id，拿着id到STAFF_DATA['id']里找对应的id的索引，
        # 再拿这个索引，去STAFF_DATA['age']列表里，改对应索引的值
        for matched_row in data_set:
            staff_id = matched_row[0]
            staff_id_index = STAFF_DATA['id'].index(staff_id)
            STAFF_DATA[col_name][staff_id_index] = new_val
        print(STAFF_DATA)

        save_db()  # 把修改后的数据刷到磁盘中
        print_log("成功修改了%s条数据!" % len(data_set), 'info')
    else:
        print_log("语法错误：未检测到set关键字！", 'error')


# def syntax_add(data_set, query_clause):
#     pass


def syntax_parser(cmd):
    """
    解析语句并执行
    :param cmd:
    :return:
    """
    syntax_list = {
        'find': syntax_find,
        # 'del': syntax_delete,
        'update': syntax_update,
        # 'add': syntax_add,
    }
    # find name,age from staff_table where age > 22
    if cmd.split()[0] in ('find', 'add', 'del', 'update'):
        if 'where' in cmd:
            query_clause, where_clause = cmd.split("where")
            print(query_clause, where_clause)
            matched_records = syntax_where(where_clause)
            # if query_clause.split()[0] == 'find':
            #     syntax_find()
            # elif query_clause.split[0] == 'del':
            #     syntax_delete()
        else:
            matched_records = []
            for index, staff_id in enumerate(STAFF_DATA['id']):
                record = []
                for col in COLUMNS:
                    record.append(STAFF_DATA[col][index])
                matched_records.append(record)
            query_clause = cmd
        cmd_action = cmd.split()[0]
        if cmd_action in syntax_list:
            syntax_list[cmd_action](matched_records, query_clause)

    else:
        print_log("语法错误：[find|add|del|update] [column1,..] from [staff_table] [where] [column] [>,<..] [condtion]\n",
                  'error')


def main():
    """
    让用户输入语句，并执行
    :return:
    """


while True:
    cmd = input("[staff_db]: ").strip()
    if not cmd:
        continue

    syntax_parser(cmd.strip())

main()
