from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HmsPatient(models.Model):
    _name = 'hms.patient'
    _inherit = ['mail.thread']
    _description = 'Hms Patient'

    first_name = fields.Char(string="First Name", required=True, tracking=True)
    last_name = fields.Char(string="Last Name", required=True, tracking=True)
    age = fields.Integer(string="Age", required=True, tracking=True)
    birth_date = fields.Date(string="Birth Day", required=True, tracking=True)
    address = fields.Text(string="Address", required=True, tracking=True)
    history = fields.Html(string="History")
    cr_ratio = fields.Float(string="CR Ratio")
    blood_type = fields.Selection(
        [('a+', 'A+'),
         ('a-', 'A-'),
         ('b+', 'B+'),
         ('b-', 'B-'),
         ('ab+', 'AB+'),
         ('ab-', 'AB-'),
         ('o+', 'O+'),
         ('o-', 'O-'),
         ],
        string="Blood Type", required=True, tracking=True)
    states = fields.Selection(
        [('undetermined', 'Undetermined'),
         ('good', 'Good'),
         ('fair', 'Fair'),
         ('serious', 'Serious'),
         ],
        string="States", default='undetermined')
    pcr = fields.Boolean(string="PCR", required=True, tracking=True)
    image = fields.Image(string="Image")
    email = fields.Char(string='Email', index=True, required=True)
    department_id = fields.Many2one('hms.department', string="Department")

    # SQL constraints
    _sql_constraints = [
        ('unique_email', 'unique("email")', 'This email is exist!')
    ]

    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if record.email and '@' not in record.email:
                raise ValidationError("Invalid email format")

    # for undetermined

    def action_undetermined(self):
        for rec in self:
            rec.states = 'undetermined'

            # rec.write({
            #     'states':'undetermined'
            # })

    # for good

    def action_good(self):
        for rec in self:
            rec.states = 'good'
            # rec.write({
            #     'states':'good'
            # })

    # for fair

    def action_fair(self):
        for rec in self:
            rec.states = 'fair'
            # rec.write({
            #     'states':'fair'
            # })

    # for serious

    def action_serious(self):
        for rec in self:
            rec.states = 'serious'
            # rec.write({
            #     'states':'serious'
            # })
