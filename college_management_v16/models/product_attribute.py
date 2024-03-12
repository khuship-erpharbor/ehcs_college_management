from odoo import models,fields

class ProductAttribute(models.Model):
	_inherit = "product.attribute"


	is_product_attribute = fields.Boolean(string="is_product_attribute")

	country = fields.Selection([
		('india','India'),
		('china','China'),
		('usa','USA'),
		('uk','UK')
		],string="Country")


class ProductAttributeValue(models.Model):
	_inherit = "product.attribute.value"


	is_product_attribute_value = fields.Boolean(string="product?")


	