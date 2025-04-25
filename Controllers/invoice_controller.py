from Models.invoice_model import Invoice
from Models.user_model import User
from flask import jsonify, request
from Utils.CommonExceptions import CommonException
import logging


class InvoiceController():
    def getInvoice():
        try:
            invoices = Invoice.objects()
            if invoices:
                return jsonify([invoice.to_json() for invoice in invoices]), 200
            else:
                return jsonify([]), 200
        except Exception as e:
            logging.error(f"Error in getInvoice: {str(e)}")
            return CommonException.handleException(e)
    
    def getInvoiceByCategory():
        try:
            category = request.args.get('category')
            if not category:
                return CommonException.IdRequiredException()
            invoices = Invoice.objects(category=category)
            if invoices:
                return jsonify([invoice.to_json() for invoice in invoices]), 200
            else:
                return jsonify([]), 200
        except Exception as e:
            logging.error(f"Error in getInvoiceByCategory: {str(e)}")
            return CommonException.handleException(e)

    def getInvoicesByUser():
        try:
            token = request.headers.get('Authorization')
            user = User.objects(auth_token=token).first()
            invoices = Invoice.objects(user=user.id)
            if invoices:
                return jsonify([invoice.to_json() for invoice in invoices]), 200
            else:
                return jsonify([]), 200
        except Exception as e:
            logging.error(f"Error in getInvoicesByUser: {str(e)}")
            return CommonException.handleException(e)

    def createInvoice():
        try:
            data = request.get_json()
            if not data:
                return CommonException.DataRequiredException()
            
            token = request.headers.get('Authorization')
            user = User.objects(auth_token=token).first()
            if not user:
                return CommonException.InvalidIdException()
            
            invoice = Invoice(user=user.id, **data)
            invoice.validate()
            invoice.save()
            return jsonify({"Message": "Invoice Created Successfully"}), 200
        except Exception as e:
            logging.error(f"Error in createInvoice: {str(e)}")
            return CommonException.handleException(e)

    def updateInvoice():
        try:
            id = request.args.get('id')
            if not id:
                return CommonException.IdRequiredException()
            data = request.get_json()
            if not data:
                return CommonException.DataRequiredException()
            invoice = Invoice.objects(id=id).first()
            if invoice:
                invoice.update(**data)
                return jsonify({"Message": "Invoice Updated Successfully"}), 200
            else:
                return CommonException.InvalidIdException()
        except Exception as e:
            logging.error(f"Error in updateInvoice: {str(e)}")
            return CommonException.handleException(e)
    
    def deleteInvoice():
        try:
            token = request.headers.get('Authorization')
            user = User.objects(auth_token=token).first()
            id = request.args.get('id')
            if not id:
                return CommonException.IdRequiredException()
            invoice = Invoice.objects(user=user.id, id=id).first()
            if invoice:
                invoice.delete()
                return jsonify({"Message": "Invoice Deleted Successfully"}), 200
            else:
                return CommonException.InvalidIdException()
        except Exception as e:
            logging.error(f"Error in deleteInvoice: {str(e)}")
            return CommonException.handleException(e)
