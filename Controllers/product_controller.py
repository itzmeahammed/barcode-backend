from Models.product_models import Product
from Models.user_model import User
from flask import jsonify, request
from Utils.CommonExceptions import CommonException
import logging


class ProductController():
    def getProduct():
        try:
            products = Product.objects()
            if products:
                return jsonify([product.to_json() for product in products]), 200
            else:
                return jsonify([]), 200
        except Exception as e:
            logging.error(f"Error in getProduct: {str(e)}")
            return CommonException.handleException()
    
    def getProductByCatogory():
        try:
            catogory = request.args.get('catogory')
            if not catogory:
                return CommonException.IdRequiredException()
            products = Product.objects(catogory=catogory)
            if products:
                return jsonify([product.to_json() for product in products]), 200
            else:
                return jsonify([]), 200
        except Exception as e:
            logging.error(f"Error in getProductByCatogory: {str(e)}")
            return CommonException.handleException()

    def getProductsByUser():
        try:
            token = request.headers.get('Authorization')
            user = User.objects(auth_token=token).first()
            products = Product.objects(user=user.id)
            if products:
                return jsonify([product.to_json() for product in products]), 200
            else:
                return jsonify([]), 200
        except Exception as e:
            logging.error(f"Error in getProductsByUser: {str(e)}")
            return CommonException.handleException(e)

    def createProduct():
        try:
            data = request.get_json()
            if not data:
                return CommonException.DataRequiredException()
            
            token = request.headers.get('Authorization')
            user = User.objects(auth_token=token).first()
            if not user:
                return CommonException.InvalidIdException()
            
            product = Product(user=user.id,**data)
            product.validate()
            product.save()
            return jsonify({"Message": "Product Created Successfully"}), 200
        except Exception as e:
            logging.error(f"Error in createProduct: {str(e)}")
            return CommonException.handleException(e)

    def updateProduct():
        try:
            id = request.args.get('id')
            if not id:
                return CommonException.IdRequiredException()
            data = request.get_json()
            if not data:
                return CommonException.DataRequiredException()
            product = Product.objects(id=id).first()
            if product:
                product.update(**data)
                return jsonify({"Message": "Product Updated Successfully"}), 200
            else:
                return CommonException.InvalidIdException()
        except Exception as e:
            logging.error(f"Error in updateProduct: {str(e)}")
            return CommonException.handleException(e)
    
    def deleteProduct():
        try:
            token = request.headers.get('Authorization')
            user = User.objects(auth_token=token).first()
            id = request.args.get('id')
            if not id:
                return CommonException.IdRequiredException()
            product = Product.objects(user=user.id, id=id).first()
            if product:
                product.delete()
                return jsonify({"Message": "Product Deleted Successfully"}), 200
            else:
                return CommonException.InvalidIdException()
        except Exception as e:
            logging.error(f"Error in deleteProduct: {str(e)}")
            return CommonException.handleException(e)
