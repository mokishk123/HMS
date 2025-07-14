from odoo import api, fields, models


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
    department_id = fields.Many2one('hms.department', string="Department")


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
