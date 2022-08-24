from odoo import _, api, fields, models, tools 
from odoo.exceptions import UserError, ValidationError
import time
import requests
from hashlib import sha256

class PaymentAcquirer(models.Model):

    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('cashpay', "Cashpay")], ondelete={'cashpay': 'set default'})
    cashpay_api_login = fields.Char(string='Api login')
    cashpay_api_key = fields.Char(string='Api key')
    cashpay_api_refenrence = fields.Char(string='Api reference')

    

    def _cashapy_make_request(self, salt, data = None, method="post"):
        endpoint_url = "https://sandbox.semoa-payments.com/api"
        login = self.cashpay_api_login
        apireference = self.cashpay_api_refenrence
        api_key = self.cashpay_api_key
        token = login + api_key + salt
        api_secure = sha256(token.encode('utf-8')).hexdigest()

        headers = {
            'login': login,
            'apisecure': api_secure,
            'apireference': apireference,
            'salt': salt,
            'Content-Type': 'application/json',
        }


        try:
            if method == 'post':
                response = requests.post(endpoint_url + '/orders',  headers=headers, json=data)
            else:
                response = requests.post(endpoint_url + '/orders',  headers=headers)
        except ConnectionError as e:
            raise UserError(_(e , "Erreur lors de la connexon à l'API : Vérifiez votre connexion Internet"))
        
        return response.json()

