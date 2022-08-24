from odoo import _, api, fields, models, tools 
from odoo.exceptions import UserError, ValidationError
import time
from werkzeug import urls

class PaymentTransaction(models.Model):

    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider != 'cashpay':
            return res

        return {
            'api_url': self._get_api_bill_data().get('bill_url'),
            'order_reference': self._get_api_bill_data().get('order_reference')
        }


    
    def _get_api_bill_data(self):
        base_url = self.acquirer_id.get_base_url()
        salt = str(time.time())
        data = {
            'amount': self.amount,
            'merchant_reference': self.reference + salt,
            'description': 'Test environnement Sandbox',
            'callback_url': base_url + 'callback',
            'redirect_url': base_url + 'callback',
            'client': {
                'lastname': self.partner_id.name,
                'firstname': self.partner_id.name,
                'phone': self.partner_id.phone if self.partner_id.phone else '+00000000000'
            },
            'direct_pay': 0,
            'gateway': 1,
            
        }
        response = self.acquirer_id._cashapy_make_request(salt, data)
        return {
            'bill_url': response.get('bill_url'),
            'order_reference': response.get('order_reference'),
        }
    @api.model
    def _get_tx_from_feedback_data(self, provider, data):
        """ Override of payment to find the transaction based on Ogone data.

        :param str provider: The provider of the acquirer that handled the transaction
        :param dict data: The feedback data sent by the provider
        :return: The transaction if found
        :rtype: recordset of `payment.transaction`
        :raise: ValidationError if the data match no transaction
        """
        raise ValidationError(_("gggggggggg " + str(data) + " gggggggggggggggggg"))
        tx = super()._get_tx_from_feedback_data(provider, data)
        if provider != 'cashpay':
            return tx

        reference = 'FAC/2022/00001'
        tx = self.search([('reference', '=', reference), ('provider', '=', 'cashpay')])
        if not tx:
            raise ValidationError(
                "cashpay: " + _("No transaction found matching reference %s.", reference)
            )
        return tx