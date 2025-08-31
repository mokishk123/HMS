from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HmsPatient(models.Model):
    _name = 'hms.patient'
    _inherit = ['mail.thread']
    _description = 'Hms Patient'
    _rec_name = 'first_name'

    first_name = fields.Char(string="First Name", required=True, tracking=True)
    last_name = fields.Char(string="Last Name", required=True, tracking=True)
    age = fields.Integer(string="Age", required=True, tracking=True, compute="_compute_age")
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
    email = fields.Char(string='Email', required=True)
    department_id = fields.Many2one('hms.department', string="Department")
    capacity = fields.Integer(related='department_id.capacity')
    doctor_ids = fields.Many2many('hms.doctor')
    user_id = fields.Many2one("res.users", string="Owner", default=lambda self: self.env.user, index=True)

    # SQL constraints
    _sql_constraints = [
        ('unique_email', 'unique("email")', 'This email is exist!')
    ]

    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if record.email and '@' not in record.email:
                raise ValidationError("Invalid email format")

    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                today = date.today()
                born = record.birth_date
                age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
                record.age = age
            else:
                record.age = 0

    @api.onchange('pcr')
    def _check_cr_ratio(self):
        for record in self:
            if record.pcr and record.cr_ratio <= 0.0:
                return {
                    'warning': {
                        'title': ('CR Ratio'),
                        'message': 'CR Ratio is Required'
                    }
                }

    @api.onchange('age')
    def _check_cr_ratio(self):
        for record in self:
            if record.age <= 30:
                record.pcr = True
                return {
                    'warning': {
                        'title': ('PCR'),
                        'message': 'PCR was Checked'
                    }
                }

    @api.constrains('birth_date')
    def _check_birth_date(self):
        for record in self:
            if record.birth_date and record.birth_date > date.today():
                raise ValidationError("The age must be positive")

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

    log_history_ids = fields.One2many(
        'log.history',
        'patient_id',
        string='Log History',
        readonly=True
    )

    @api.model
    def create(self, vals):

        patient = super(HmsPatient, self).create(vals)

        self.env['log.history'].create({
            'patient_id': patient.id,
            'description': _('Patient record created.'),
        })
        return patient

    def write(self, vals):
        for patient in self:
            old_states = patient.states
            result = super(HmsPatient, patient).write(vals)

            if 'states' in vals and patient.states != old_states:
                self.env['log.history'].create({
                    'patient_id': patient.id,
                    'description': _('State changed from %s to %s.') % (old_states, patient.states),
                })
            return result


class LogHistory(models.Model):
    _name = 'log.history'
    _description = 'Patient Log History'
    _order = 'create_date desc'

    create_uid = fields.Many2one(
        'res.users',
        string='Created By',
        readonly=True
    )

    create_date = fields.Datetime(
        string='Creation Date',
        readonly=True
    )

    description = fields.Text(
        string='Description',
        readonly=True
    )

    patient_id = fields.Many2one(
        'hms.patient',
        string='Patient',
        required=True,
        ondelete='cascade',
        readonly=True
    )
