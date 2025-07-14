from odoo import api, fields, models


class HmsDepartment(models.Model):
    _name = 'hms.department'
    _inherit = ['mail.thread']
    _description = 'Hms Department'

    name = fields.Char(string="Name", required=True, tracking=True)
    capacity = fields.Integer(string="Capacity", required=True)
    is_opened = fields.Boolean(string="Open", required=True, tracking=True)
    patient_ids = fields.One2many('hms.patient', 'department_id', string="Patients")
