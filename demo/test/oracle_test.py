# -*- coding: utf-8 -*-
import os
import xlwt
import cx_Oracle

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

conn = cx_Oracle.connect('oauser/oauser@192.168.70.6/orcl')
print conn.version
cursor = conn.cursor()
# stringinput = raw_input('input string')
# intinput = input('input:')
# eval将参数转为表达式/程序代码执行语句
# testinput = eval(input('input:'))
# print stringinput
cursor.execute("select h.lastname,cf.field31,cf.field32 from cus_fielddata cf,hrmresource h where cf.id = h.id")
# row = cursor.fetchone()
rows = cursor.fetchall()
print len(rows)
cursor.close()
conn.close()
# book = xlwt.Workbook(encoding='utf-8')
# sheet = book.add_sheet("test 1sheet", cell_overwrite_ok=True)
# for i in range(len(rows)):
#     sheet.write(i, 0, rows[i][0])
#     sheet.write(i, 1, rows[i][1])
#     sheet.write(i, 2, rows[i][2])
# book.save("test.xls")
# raw_input('Press Enter to exit...')
# __import__('os').system('dir') 当前目录文件及结构