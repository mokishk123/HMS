from odoo import api, fields, models


class HmsDoctors(models.Model):
    _name = 'hms.doctor'
    _inherit = ['mail.thread']
    _description = 'Hms Doctor'

    first_name = fields.Char(string="First Name", required=True, tracking=True)
    last_name = fields.Char(string="Last Name", required=True, tracking=True)
    image = fields.Image(string="Image")
