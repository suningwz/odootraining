# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import logging
import base64
try:
    import xlrd
    try:
        from xlrd import xlsx
    except ImportError:
        xlsx = None
except ImportError:
    xlrd = xlsx = None
import xlwt
from xlutils.copy import copy
import io  #StringIO
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Project(models.Model):
    _inherit = 'mail.thread'
    _name = 'demo.project'
    _table = 'demo_project'

    no = fields.Char(string=u'项目编号', required=True, track_visibility='onchange')
    name = fields.Char(string=u'项目名称', required=True, track_visibility='onchange')
    startDate = fields.Date(string=u'开始时间', required=True)
    state = fields.Char(string=u'state')
    money = fields.Float(string=u'金额')
    # test = fields.Char(string=u'test', related='attachment_ids.test') # related只会关联many表数据的第一条
    test = fields.Char(string=u'test')
    file = fields.Binary(string=u'附件')
    file_name = fields.Char(string=u'附件名')
    total_receive_pay = fields.Float(string=u'合计', compute='_compute_total_rp', store=True)
    ir_attachment_file = fields.Binary(string=u'转存附件', compute='_compute_attachment_file',
                                       inverse='_inverse_attachment_file')
    ir_attachment_file_name = fields.Char(string=u'转存附件名')
    attachment_file = fields.Binary(string=u'附件属性文件', attachment=True)
    attachment_file_name = fields.Char(string=u'附件属性文件名')
    attachment_ids = fields.One2many('demo.attachment', 'project_id', string=u'附件列表')
    cus_attachment_ids = fields.One2many('demo.cus.attachment', 'project_id', string=u'附件列表')
    receivePay_ids = fields.One2many('demo.project.receivepay',
                                     'project_id', string=u'收付款', track_visibility='onchange')
    ir_attachment_ids = fields.One2many('ir.attachment', 'res_id', string=u'系统自带附件',
                                        domain=[('res_model', '=', 'demo.project'),
                                                ('res_field', '=', 'demo.project.ir_attachment_ids')])

    def _compute_attachment_file(self):
        """
        ir.attachment的上传文件存储于data_dir中
        根据当前字段信息获取对于在ir.attachment的文件bytes
        :return:
        """
        print('compute att get')
        # binary = self.env['demo.project'].search([])[0].file
        ir_attachment_obj = self.env['ir.attachment']
        for record in self:
            # 根据model filed等信息获取file的bytes
            ir_attachments = ir_attachment_obj.search([('res_model', '=', 'demo.project'),
                                                       ('res_id', '=', record.id),
                                                       ('res_field', '=', 'demo.project.ir_attachment_file')])
            if len(ir_attachments) > 0:
                datas = ir_attachments[0].datas
                # datas_name = ir_attachments[0].datas_fname
                # record.ir_attachment_file_name = datas_name
                record.ir_attachment_file = datas

    def _inverse_attachment_file(self):
        """
        截取上传文件的bytes，将bytes转入ir.attachment表中，通过该表逻辑将文件写入磁盘
        :return:
        """
        print('inverse att set')
        ir_attachment_obj = self.env['ir.attachment']
        for record in self:
            ir_attachments = ir_attachment_obj.search([('res_model', '=', 'demo.project'),
                                                       ('res_id', '=', record.id),
                                                       ('res_field', '=', 'demo.project.ir_attachment_file')])
            if record.ir_attachment_file:
                if len(ir_attachments) > 0:
                    val = {
                        'name': record.ir_attachment_file_name,
                        'datas_fname': record.ir_attachment_file_name,
                        'datas': record.ir_attachment_file
                    }
                    ir_attachments[0].write(val)
                elif len(ir_attachments) == 0:
                    val = {
                        'name': record.ir_attachment_file_name,
                        'datas_fname': record.ir_attachment_file_name,
                        'res_model': 'demo.project',
                        'res_id': record.id,
                        'res_field': 'demo.project.ir_attachment_file',
                        'datas': record.ir_attachment_file,
                        'type': 'binary',
                    }
                    ir_attachments.create(val)
            else:
                ir_attachments.unlink()
            # vals = {
            #     'ir_attachment_file_name': record.ir_attachment_file_name,
            #     'attachment_file': False
            # }
            # super(Project, record.sudo()).write(vals)

    @api.multi
    def copy_att(self):
        ir_attachment_obj = self.env['ir.attachment']
        copy_atts = self.env['demo.cus.attachment'].search([])
        print('start demo.cus.attachment')
        for copy_att in copy_atts:
            value = copy_att.attachment
            # bin_data = value and value.decode('base64') or ''
            ir_att_val = {
                # 'file_size': len(bin_data),
                # 'db_datas': value,
                'name': copy_att.name,
                'datas_fname': copy_att.name,
                'res_model': 'demo.cus.attachment',
                'res_id': copy_att.id,
                # 要与字段名称相同
                'res_field': 'attachment_location',
                'datas': value,
                'type': 'binary',
            }
            ir_attachment_obj.create(ir_att_val)
        print('end demo.cus.attachment')

    @api.multi
    def del_att(self):
        del_atts = self.env['demo.cus.attachment'].search([])
        print('start del demo.cus.attachment')
        value = ''
        data = value.encode('base64')
        for del_att in del_atts:
            att_val = {
                'attachment': data
            }
            del_att.write(att_val)
        print('end del demo.cus.attachment')

    @api.multi
    def add_att(self):
        p = self.env['demo.project'].search([])[0].file
        # 复制原二进制文件，存储到其他表中
        file_data = base64.decodestring(self.file)
        book = xlrd.open_workbook(file_contents=file_data)  # odoo存储的二进制进行了base64编码
        sheet = book.sheet_by_index(0)
        print(sheet.cell_value(1, 2))
        # w_book = xlwt.Workbook(encoding='utf-8')
        w_book = copy(book)
        w_sheet = w_book.get_sheet(0)
        w_sheet.write(1, 2, 'changed!')
        # xlwt修改后xls文件对象转为二进制的容器output
        output = io.StringIO        #StringIO.StringIO()
        book_output = io.StringIO   #StringIO.StringIO()
        w_book.save(book_output)
        # base64.encode内使用的stiringio.read方法，此方法使用需要先使用seek设置读取文件内容的位置
        book_output.seek(0)
        print(book_output.getvalue())
        base64.encode(book_output, output)
        print(output.getvalue())
        vals = {
            'project_id': self.id,
            'attachment': output.getvalue(),
            'test': self.test
        }
        self.env['demo.attachment'].create(vals)

    @api.onchange('file')
    def _onchange_file(self):
        if not self.file and self.file == '':
            return {
                'warning': {
                    'title': "Incorrect 'seats' value",
                    'message': "The number of available seats may not be negative",
                },
            }
        print('onchange')

    @api.depends('receivePay_ids')
    def _compute_total_rp(self):
        print('depends------------')
        for record in self:
            print(record.id)
            total = 0
            for recevie in record.receivePay_ids:
                record.total_receive_pay += recevie.receivables

    @api.onchange('money')
    def _onchange_file(self):
        if self.money == 1:
            self.money = 2
            # raise ValidationError(u'test')
            return {
                'warning': {
                    'title': "Incorrect 'seats' value",
                    'message': "The number of available seats may not be negative",
                },
            }
            print('onchange')

    @api.model
    def model_method(self):
        print(self.env.context)
        #  will print: {'lang': 'en_US', 'new_key': 'key_value', 'tz': 'Europe/Brussels', 'uid': 1}
        value = self.env.context['new_key']
        # record_id = self.env.context['record_id']
        # print(record_id)
        # project_record = self.env['demo.project'].search([('id', '=', record_id)])
        # project_record.name = value
        return {
            "keyName": "world"
        }

    @api.multi
    def method_in_pop(self):
        print('method')
        print(self.id)

    @api.multi
    def pop_map(self):
        self.ensure_one()
        print(self.id)
        return {
            'type': 'ir.actions.client',
            'tag': 'demo_baidu_map',
            'target': 'new',
            'context': {'record_id': self.id},
        }

    @api.multi
    def pop_window_view(self):
        self.ensure_one()
        return {
            'name': _('pop_window_view'),
            'domain': False,
            'res_model': 'demo.project',
            'type': 'ir.actions.act_window',
            'view_id': self.env.ref('demo.project_pop_form_view').id,
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': {'record_id': self.id},
        }

    def pop_window_url(self):
        return {
            'type': 'ir.actions.act_url',
            'name': "Redirect to the Website Projcet Rating Page",
            'target': 'new',
            # 'url': "/project/rating/%s" % (self.id,)
            'url': "/demo/demo/",
            'context': {
                'test': 'getTest'
            }
        }

    @api.model
    def create(self, data):
        demo = super(Project, self.with_context(mail_create_nolog=True)).create(data)
        demo.message_post(
            body=_('%s has been added to the project!') % demo.name)
        # print(self.env.user.name)
        _logger.info(u'%s 添加项目 %s !',
                     self.env.user.name, demo.name)
        return demo

    @api.multi
    def write(self, vals):
        """
        This function write an entry in the openchatter whenever we change important information
        on the model
        """
        print('write')
        print(vals)
        # for project in self:
        #     changes = []
        #     if 'receivePay_ids' in vals:
        #         print(vals['receivePay_ids'])
        #         # [[1, 1, {u'receivables': 111119}], [1, 2, {u'receivables': 20003}]]
        #         # op, id, change val
        #         for receive in vals['receivePay_ids']:
        #             print(receive)
        #             changes.append(_("Receive: OP:%s, ID: %s, VAL: %s ") % (receive[0], receive[1], receive[2]))
        #     # if 'receivePay_ids' in vals and project.receivePay_ids.id != vals['receivePay_ids']:
        #     #     value = self.env['fleet.vehicle.model'].browse(vals['model_id']).name
        #     #     oldmodel = vehicle.model_id.name or _('None')
        #     #     changes.append(_("Model: from '%s' to '%s'") % (oldmodel, value))
        #     # if 'model_id' in vals and vehicle.model_id.id != vals['model_id']:
        #     #     value = self.env['fleet.vehicle.model'].browse(vals['model_id']).name
        #     #     oldmodel = vehicle.model_id.name or _('None')
        #     #     changes.append(_("Model: from '%s' to '%s'") % (oldmodel, value))
        #     # if 'driver_id' in vals and vehicle.driver_id.id != vals['driver_id']:
        #     #     value = self.env['res.partner'].browse(vals['driver_id']).name
        #     #     olddriver = (vehicle.driver_id.name) or _('None')
        #     #     changes.append(_("Driver: from '%s' to '%s'") % (olddriver, value))
        #     # if 'state_id' in vals and vehicle.state_id.id != vals['state_id']:
        #     #     value = self.env['fleet.vehicle.state'].browse(vals['state_id']).name
        #     #     oldstate = vehicle.state_id.name or _('None')
        #     #     changes.append(_("State: from '%s' to '%s'") % (oldstate, value))
        #     # if 'license_plate' in vals and vehicle.license_plate != vals['license_plate']:
        #     #     old_license_plate = vehicle.license_plate or _('None')
        #     #     changes.append(_("License Plate: from '%s' to '%s'") % (old_license_plate, vals['license_plate']))
        #
        #     if len(changes) > 0:
        #         self.message_post(body=", ".join(changes))

        return super(Project, self).write(vals)


class Attachment(models.Model):
    _name = 'demo.attachment'
    _table = 'demo_attachment'

    name = fields.Char(string=u'附件名称')
    attachment = fields.Binary(string=u'附件', attachment=True)
    # test = fields.Char(string=u'test', related='project_id.test') # related会把所有条数据都变为关联的字段
    test = fields.Char(string=u'test')
    # 关联删除
    #  no atction：相互不影响
    # cascade:主键被删除，外键对应的记录也删除。直接删除外键的记录，不影响主键。
    # restrict: 如果存在外键，主键删除的时候报错。
    # set null：主键被删除，外键变为空值。
    # set default:主键被删除，外键变为默认值。
    project_id = fields.Many2one('demo.project', ondelete='cascade', string=u'所属项目')


class CustomizeAtt(models.Model):
    _name = 'demo.cus.attachment'

    name = fields.Char(string=u'附件名称')
    # attachment = fields.Binary(string=u'附件', compute='_compute_attachment_file', inverse='_inverse_attachment_file')
    attachment = fields.Binary(string=u'附件')
    attachment_location = fields.Binary(string=u'附件(磁盘)', attachment=True)
    project_id = fields.Many2one('demo.project', ondelete='cascade', string=u'所属项目')

    # def _compute_attachment_file(self):
    #     """
    #     ir.attachment的上传文件存储于data_dir中
    #     根据当前字段信息获取对于在ir.attachment的文件bytes
    #     :return:
    #     """
    #     print('compute att get')
    #     # binary = self.env['demo.project'].search([])[0].file
    #     ir_attachment_obj = self.env['ir.attachment']
    #     for record in self:
    #         # 根据model filed等信息获取file的bytes
    #         ir_attachments = ir_attachment_obj.search([('res_model', '=', 'demo.cus.attachment'),
    #                                                    ('res_id', '=', record.id),
    #                                                    ('res_field', '=', 'demo.cus.attachment.attachment')])
    #         if len(ir_attachments) > 0:
    #             datas = ir_attachments[0].datas
    #             # datas_name = ir_attachments[0].datas_fname
    #             # record.ir_attachment_file_name = datas_name
    #             record.attachment = datas
    #         else:
    #             a = self.search([('id', '=', record.id)])[0]
    #             # print(a.attachment) ->False
    #
    # def _inverse_attachment_file(self):
    #     """
    #     截取
    #     :return:
    #     """
    #     print('inverse att set')
    #     ir_attachment_obj = self.env['ir.attachment']
    #     for record in self:
    #         ir_attachments = ir_attachment_obj.search([('res_model', '=', 'demo.cus.attachment'),
    #                                                    ('res_id', '=', record.id),
    #                                                    ('res_field', '=', 'demo.cus.attachment.attachment')])
    #         if record.ir_attachment_file:
    #             if len(ir_attachments) > 0:
    #                 val = {
    #                     'name': record.name,
    #                     'datas_fname': record.name,
    #                     'datas': record.attachment
    #                 }
    #                 ir_attachments[0].write(val)
    #             elif len(ir_attachments) == 0:
    #                 val = {
    #                     'name': record.name,
    #                     'datas_fname': record.name,
    #                     'res_model': 'demo.cus.attachment',
    #                     'res_id': record.id,
    #                     'res_field': 'demo.cus.attachment.attachment',
    #                     'datas': record.attachment,
    #                     'type': 'binary',
    #                 }
    #                 ir_attachments.create(val)
    #         else:
    #             ir_attachments.unlink()


class ReceivePay(models.Model):
    _inherit = 'mail.thread'
    _name = 'demo.project.receivepay'

    receiveDate = fields.Date(string=u'收款日期', default=fields.Date.today)
    receiveCompany = fields.Char(string=u'收款单位')
    receivables = fields.Float(string=u'金额', required=True, track_visibility='onchange')
    description = fields.Char(string=u'描述')
    expectedRecDate = fields.Date(string=u'预计回收时间')
    performanceBond_is = fields.Selection([
        (u'Y', u'是'),
        (u'N', u'否')
    ], string=u'履约金保证金', default='N')
    # 关联删除
    # set null: 删除主记录[one表数据]时候，从记录到主记录的引用置为null。
    # set default: 删除主记录时候，从记录到主记录的引用置为缺省值。
    # cascade: 删除主记录时候，级联删除从记录。
    # restrict: 如果有从记录，不允许删除主记录。
    # no action: 不采取任何动作，即删除主记录，但保留从记录不变。测试没用
    project_id = fields.Many2one('demo.project', ondelete='set null', string=u'所属项目')


class CacheTest(models.Model):
    _name = "demo.cache"

    active = fields.Boolean('Active', default=True)
    no = fields.Char(string=u'项目编号')
    name = fields.Char(string=u'项目名称')
    startDate = fields.Date(string=u'开始时间')

    @api.multi
    def save(self):
        ids = []
        for index in range(1, 4):
            create_id = self.env['demo.many.test'].create({'name': str(index)})
            ids.append(create_id.id)
        print(ids)
        return {
            'name': _('Select Project'),
            'domain': False,
            'res_model': 'demo.wizard',
            'type': 'ir.actions.act_window',
            'view_id': self.env.ref('demo.wizard_form_view').id,
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': {
                'record_id': self.id,
                'default_project_id': 1,
                'default_test_ids': ids
            },
        }


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    @api.model
    def create(self, vals):
        # if vals.get('res_id', 0) != 0 and not (vals.get('res_id', False) and vals.get('res_model', False)):
        #     vals['res_id'] = vals['res_id']
        #     vals['res_model'] = 'demo.project'
        #     vals['res_field'] = 'demo.project.ir_attachment_ids'
        return super(IrAttachment, self).create(vals)

    @api.multi
    def write(self, vals):

        return super(IrAttachment, self).write(vals)
