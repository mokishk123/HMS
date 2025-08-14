from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one('hms.patient', string="Related Patient")

    @api.constrains('related_patient_id')
    def _check_patient_email_unique(self):
        for partner in self:
            if partner.related_patient_id and partner.related_patient_id.email:
                existing = self.search([
                    ('related_patient_id.email', '=', partner.related_patient_id.email),
                    ('id', '!=', partner.id)
                ])
                if existing:
                    raise ValidationError(_("This patient email is already linked to another customer."))

    @api.constrains('vat')
    def _check_vat_required_for_customers(self):
        for rec in self:
            if rec.customer_rank > 0 and not rec.vat:
                raise ValidationError(_('Tax ID (VAT) is mandatory for CRM customers.'))

    def unlink(self):
        for partner in self:
            if partner.related_patient_id:
                raise ValidationError(_("You cannot delete a customer linked to a patient."))
        return super().unlink()
