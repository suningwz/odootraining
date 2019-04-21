# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import os
import sys
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO  #from StringIO import StringIO

try:
    import xlrd
    try:
        from xlrd import xlsx
    except ImportError:
        xlsx = None
except ImportError:
    xlrd = xlsx = None

try:
    import odf_ods_reader
except ImportError:
    odf_ods_reader = None
import xlwt
from xlutils.copy import copy


class DemoImport(models.TransientModel):
    _name = 'demo.import'
    _transient_max_hours = 12.0
    file = fields.Binary('File', help="File to check and/or import, raw binary (not base64)")
    file_name = fields.Char('File Name')
    test = fields.Char('test')

    @api.multi
    def read_test(self):
        self.ensure_one()
        # xlrd模块解析xls
        # xlsxfile = r'E:\ODOO\test.xlsx'
        # book = xlrd.open_workbook(xlsxfile)
        # book = xlrd.open_workbook(file_contents=self.file) # 读不出来
        temp_dir = os.path.join(os.getcwd(), u'temp')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        file_path = os.path.join(temp_dir, self.file_name)
        print('tempdir---------->', file_path)
        # write
        binary_data = self.file
        f = open(file_path, 'wb')
        f.write(binary_data.decode('base64'))
        f.close()
        book = xlrd.open_workbook(file_path)

        # 获取sheet对象
        sheet_name = book.sheet_names()[0]
        print('sheet_name-------> %s' % sheet_name)
        # 方法1：通过sheet的名字获取，如果知道sheet名字可以直接指定
        # sheet = book.sheet_by_name(sheet_name)
        # 方法2：通过sheet索引获取
        sheet = book.sheet_by_index(0)
        # 获取行数总数
        rows = sheet.nrows
        # 获取列总数
        cols = sheet.ncols
        print('rows--------->%s;cols----------->%s' % (rows, cols))
        # 获得指定行，列值，返回对象为一个值列表
        row_data = sheet.row_values(0)  # 或得第一行的数据列表
        col_data = sheet.col_values(0)  # 获得第一列的数据列表
        print('row_data---------->', row_data)
        # 通过cell的位置坐标获得指定cell的值
        cell_value1 = sheet.cell_value(2, 1)  # 只有值内容
        cell_value2 = sheet.cell(2, 1)  # 包含附加属性+内容
        print('cell1-------->%s;cell2-------->%s' % (cell_value1, cell_value2))
        # flag = u'test123'
        self.test = cell_value1
        print('file---------------->: %s, %s' % (self.file_name, self.test))
        # 删除文件
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            print(u"%s,文件不存在" % file_path)

    @api.multi
    def write_test(self):
        self.ensure_one()
        # E:\ODOO\test\export_test.xlsx
        xlsxfile = r'E:\ODOO\test\export_test.xlsx'
        book = xlrd.open_workbook(xlsxfile)
        w = copy(book)
        w.get_sheet(0).write(2, 2, "foo")
        w.save(r'E:\ODOO\test\export_test2.xls')