from odoo import _, http
from odoo.exceptions import UserError, ValidationError
from odoo.http import request

class CashpayController(http.Controller):
    @http.route('/callback', methods=["get"], auth='public')
    def cashpay_return_from_redirect(self, **feedback_data):
        request.env['payment.transaction'].sudo()._handle_feedback_data('cashpay', feedback_data)
        return request.redirect('/payment/status')