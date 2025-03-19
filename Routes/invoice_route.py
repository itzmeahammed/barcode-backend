from Controllers.invoice_controller import InvoiceController
from flask import Blueprint

invoice_bp = Blueprint('Invoice', __name__)

invoice_bp.add_url_rule('/getInvoice', view_func=InvoiceController.getInvoice, methods=['GET'])
invoice_bp.add_url_rule('/getInvoiceByCategory', view_func=InvoiceController.getInvoiceByCategory, methods=['GET'])
invoice_bp.add_url_rule('/getInvoicesByUser', view_func=InvoiceController.getInvoicesByUser, methods=['GET'])
invoice_bp.add_url_rule('/createInvoice', view_func=InvoiceController.createInvoice, methods=['POST'])
invoice_bp.add_url_rule('/updateInvoice', view_func=InvoiceController.updateInvoice, methods=['PUT'])
invoice_bp.add_url_rule('/deleteInvoice', view_func=InvoiceController.deleteInvoice, methods=['DELETE'])
