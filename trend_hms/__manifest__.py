# noinspection PyStatementEffect
{
    "name": "Hospital Management System",
    "author": "Mohamed Mostafa Kishk",
    "version": "17.0",
    "depends": [
        'base',
        'mail',
        'contacts',
        'crm',
    ],
    "data": [
        "security/hms_security.xml",
        "security/ir.model.access.csv",
        "reports/reports.xml",
        "reports/patient_report.xml",
        "views/hms_patients_view.xml",
        "views/hms_doctors_view.xml",
        "views/hms_department_view.xml",
        "views/res_partner_views.xml",
        "views/menu.xml",
    ]
}
