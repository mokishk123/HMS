from odoo import api, fields, models


class HmsDoctors(models.Model):
    _name = 'hms.doctor'
    _inherit = ['mail.thread']
    _description = 'Hms Doctor'

    name = fields.Char(compute="_compute_name")
    first_name = fields.Char(string="First Name", required=True, tracking=True)
    last_name = fields.Char(string="Last Name", required=True, tracking=True)
    image = fields.Image(string="Image")

    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        for rec in self:
            rec.name = f'{rec.first_name} {rec.last_name}'
