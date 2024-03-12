from odoo import api, models
from odoo.exceptions import ValidationError, UserError


class User(models.Model):
     _inherit = "res.users"

     @api.model
     def create(self, values):
        group_create_user_ext_id = 'ehcs_create_user.group_create_user'
        group_create_user_id = self.env.ref('ehcs_create_user.group_create_user').id

         # Check if user has creation group
        if not self.env.user.has_group(group_create_user_ext_id):

            raise UserError("You do not have access to create a user. Please contact ERP Harbor.")
             # If no access, then show error
        return super(User, self).create(values)


