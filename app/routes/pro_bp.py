from flask import Blueprint

from ..controllers.producto_controller import proController

pro_bp = Blueprint('pro_bp', __name__)

pro_bp.route('/', methods=['GET'])(proController.get_all) 
pro_bp.route('/<int:idproducto>', methods=['GET'])(proController.get) 
pro_bp.route('/crear', methods=['POST'])(proController.create) 
pro_bp.route('/<int:idproducto>', methods=['PUT'])(proController.update)
pro_bp.route('/<int:idproducto>', methods=['DELETE'])(proController.delete) 


