from Controllers.product_controller import ProductController
from flask import Blueprint

product_bp = Blueprint('Product', __name__)

product_bp.add_url_rule('/getProduct', view_func=ProductController.getProduct, methods=['GET'])
product_bp.add_url_rule('/getProductByCategory', view_func=ProductController.getProductByCatogory, methods=['GET'])
product_bp.add_url_rule('/getProductsByUser', view_func=ProductController.getProductsByUser, methods=['GET'])
product_bp.add_url_rule('/createProduct', view_func=ProductController.createProduct, methods=['POST'])
product_bp.add_url_rule('/updateProduct', view_func=ProductController.updateProduct, methods=['PUT'])
product_bp.add_url_rule('/deleteProduct', view_func=ProductController.deleteProduct, methods=['DELETE'])
