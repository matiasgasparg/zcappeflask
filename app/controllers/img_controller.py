from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, storage
from ..models.img_model import Img
from flask_cors import CORS
from ..models.exceptions import userNotFound,CustomException,InvalidDataError,duplicateError
from werkzeug.utils import secure_filename

class imgController:
    @classmethod
    def upload_image(cls):
        if 'image' in request.files:
            image = request.files['image']
            # Sube la imagen a Firebase Storage
            bucket = storage.bucket()
            blob = bucket.blob(image.filename)
            
            # Establece el tipo de contenido como 'image/png' (o el tipo de imagen adecuado)
            blob.upload_from_file(image, content_type='image/png')

            # Obtiene el nombre del archivo
            file_name = blob.name

            # Devuelve el nombre del archivo en la respuesta
            return jsonify({"fileName": file_name})
        else:
            return 'No se encontró ninguna imagen en la solicitud'
    @classmethod
    def get(cls, idimagen):
            img = Img.get(idimagen)  # Aquí se espera un ID de imagen
            if img is not None:
                return img.serialize(), 200
            else:
                # Si no se encuentra el user, lanza la excepción userNotFound
                raise userNotFound(idimagen)
    @classmethod
    def get_all(cls):
        """Get all imgs"""
        img_objects = Img.get_all()
        imgs = []
        for img in img_objects:
            imgs.append(img.serialize())
        return imgs, 200
    @classmethod
    def create(cls):
        try:
            # Obtener los datos de la imagen del cuerpo de la solicitud JSON
            data = request.json
            genero = data['genero']
            url = data['url']
            descripcion = data['descripcion']
            precio = data['precio']
    
            # Crear una nueva instancia del modelo de imagen con los datos proporcionados
            new_img = Img(**data)
            print(new_img)
            # Llamar al método de clase 'create' del modelo de imagen para crear la imagen en la base de datos
            if Img.create(new_img):
                return jsonify({'message': 'Imagen creada exitosamente'}), 201
            else:
                return jsonify({'message': 'Error al crear imagen'}), 500

        except Exception as e:
            # Manejar cualquier error que ocurra durante el proceso de creación de la imagen
            return jsonify({'message': 'Error en la solicitud'}), 400
    @classmethod
    def update(cls, idimagen):
        """Update a Img"""
        data = request.json
        field_to_update = data.get('field')  # Campo que se desea actualizar
        value = data.get('value')  # Nuevo valor para el campo
        valid_fields = ['genero', 'url', 'descripcion', 'precio']  # Lista de campos válidos

        if field_to_update in valid_fields:
            if Img.update(idimagen, field_to_update, value):
                return jsonify({'message': f'{field_to_update.capitalize()} actualizado exitosamente'}), 200
            else:
                raise userNotFound(idimagen)
        else:
            return jsonify({'message': 'Campo no válido para actualización'}), 400
    @classmethod
    def delete(cls,idimagen):
        """Delete a Img"""
        if not Img.exists(idimagen):
            raise userNotFound(idimagen)

        Img.delete(idimagen)
        return {'message': 'Img deleted successfully'}, 204