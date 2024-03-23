from flask import Blueprint

from ..controllers.img_controller import imgController

img_bp = Blueprint('img_bp', __name__)

img_bp.route('/', methods=['POST'])(imgController.upload_image) #'/img'
img_bp.route('/', methods=['GET'])(imgController.get_all) 
img_bp.route('/<int:idimagen>', methods=['GET'])(imgController.get) 
img_bp.route('/crear', methods=['POST'])(imgController.create) 
img_bp.route('/<int:idimagen>', methods=['PUT'])(imgController.update)
img_bp.route('/<int:idimagen>', methods=['DELETE'])(imgController.delete) 


