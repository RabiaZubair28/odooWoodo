# from odoo import models, fields, api
# from odoo.exceptions import UserError

# class ApprovalRequest(models.Model):
#     _name = "approval.request"
#     _description = "Approval Request"
#     _inherit = ['mail.thread', 'mail.activity.mixin'] 



#     name = fields.Char(string="Request Name", required=True, copy=False, readonly=True, default=lambda self: "New")
#     email = fields.Char('Email')
#     requester_id = fields.Many2one('res.users', string='Requester', default=lambda self: self.env.user, readonly=True)
#     approver_id = fields.Many2one('res.users', string='Approver')
#     approval_type_id = fields.Many2one('approval.type', string="Approval Type", required=True)

#     date = fields.Datetime(string='Request Date', default=fields.Datetime.now)
#     state = fields.Selection([
#         ('draft', 'Draft'),
#         ('submitted', 'Submitted'),
#         ('approved', 'Approved'),
#         ('rejected', 'Rejected'),
#         ('cancel', 'Cancelled'),
#     ], string='Status', default='draft', tracking=True)
#     description = fields.Text(string='Description')
#     note = fields.Text(string='Manager Note')

#     def action_submit(self):
#         for rec in self:
#             if not rec.approver_id:
#                 raise UserError("Please set an approver before submitting.")
#             rec.state = 'submitted'
#             rec.message_post(body=f"Request submitted by {rec.requester_id.name} to {rec.approver_id.name}")

#     # def action_approve(self):
#         for rec in self:
#             # only approver or manager group
#             if self.env.user != rec.approver_id and not self.env.user.has_group('custom_approvals.group_approvals_manager'):
#                 raise UserError("Only the designated approver or users in Approvals Manager group can approve.")
#             rec.state = 'approved'
#             rec.message_post(body=f"Request approved by {self.env.user.name}")

#     def action_reject(self):
#         for rec in self:
#             if self.env.user != rec.approver_id and not self.env.user.has_group('custom_approvals.group_approvals_manager'):
#                 raise UserError("Only the designated approver or users in Approvals Manager group can reject.")
#             rec.state = 'rejected'
#             rec.message_post(body=f"Request rejected by {self.env.user.name}")

#     def action_set_to_draft(self):
#         for rec in self:
#             rec.state = 'draft'

#     @api.model
#     def create(self, vals):
#         if vals.get('name', "New") == "New":
#             seq = self.env['ir.sequence'].next_by_code('approval.request') or '/'
#             vals['name'] = seq
#         return super().create(vals)

from odoo import models, fields, api
from datetime import datetime

class ApprovalRequest(models.Model):
    _name = "approval.request"
    _description = "Approval Request"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string="Title", required=True, tracking=True)
    request_date = fields.Datetime(
        string="Request Date",
        default=lambda self: fields.Datetime.now(),
        tracking=True
    )
    requester_id = fields.Many2one(
        'res.users', string="Requested By",
        default=lambda self: self.env.user,
        tracking=True
    )

    approval_type_id = fields.Many2one(
        'approval.type', string="Approval Type", required=True, tracking=True
    )

    description = fields.Text(string="Description")

    # Status Flow: draft → pending → approved / rejected
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], default='draft', tracking=True)

    action_ids = fields.One2many(
        'approval.action', 'request_id',
        string="Actions"
    )

    approved_by = fields.Many2one('res.users', string="Approved By", tracking=True)
    approved_date = fields.Datetime(string="Approval Date")

    def set_pending(self):
        for rec in self:
            rec.state = 'pending'
            rec.action_ids.create({
                'request_id': rec.id,
                'action': 'submit',
                'user_id': self.env.user.id,
                'note': 'Submitted for approval',
            })

    def action_approve(self):
        for rec in self:
            rec.state = 'approved'
            rec.approved_by = self.env.user.id
            rec.approved_date = fields.Datetime.now()
            rec.action_ids.create({
                'request_id': rec.id,
                'action': 'approve',
                'user_id': self.env.user.id,
                'note': 'Approved',
            })

    def action_reject(self):
        for rec in self:
            rec.state = 'rejected'
            rec.action_ids.create({
                'request_id': rec.id,
                'action': 'reject',
                'user_id': self.env.user.id,
                'note': 'Rejected',
            })