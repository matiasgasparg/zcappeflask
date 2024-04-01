from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, storage
from ..models.pro_model import Pro
from flask_cors import CORS
from ..models.exceptions import userNotFound,CustomException,InvalidDataError,duplicateError
from werkzeug.utils import secure_filename

class proController:
    @classmethod
    def get(cls, idproducto):
        try:
            producto = Pro.get(idproducto)

            if producto:
                serialized_product = {
                    "idproducto": producto.idproducto,
                    "genero": producto.genero,
                    "descripcion": producto.descripcion,
                    "precio": producto.precio,
                    "imagenes": producto.urls_imagenes if hasattr(producto, 'urls_imagenes') else []
                }

                return jsonify(serialized_product), 200
            else:
                return jsonify({'message': 'Producto no encontrado'}), 404

        except Exception as e:
            print("Error al obtener el producto:", e)
            return jsonify({'message': 'Error en la solicitud'}), 500


    @classmethod
    def get_all(cls):
        try:
            productos = Pro.get_all()
            if productos is not None:
                serialized_products = [producto.serialize() for producto in productos]
                return jsonify(serialized_products), 200
            else:
                return jsonify({'message': 'No se pudieron obtener los productos'}), 500
        except Exception as e:
            print("Error al obtener todos los productos:", e)
            return jsonify({'message': 'Error en la solicitud'}), 500

    @classmethod
    def create(cls):
        try:
            # Obtener los datos del producto del cuerpo de la solicitud JSON
            data = request.json
            genero = data['genero']
            url = data['url']  # Cambiado el nombre del atributo
            descripcion = data['descripcion']
            precio = data['precio']

            # Crear una nueva instancia del modelo de imagen con los datos proporcionados
            new_producto = Pro(**data)
            print(new_producto)

            # Llamar al método de clase 'create' del modelo de imagen para crear la imagen en la base de datos
            if Pro.create(new_producto):
                return jsonify({'message': 'Imagen creada exitosamente'}), 201
            else:
                return jsonify({'message': 'Error al crear el Producto'}), 500

        except Exception as e:
            # Manejar cualquier error que ocurra durante el proceso de creación de la imagen
            return jsonify({'message': 'Error en la solicitud'}), 400
    @classmethod
    def update(cls, idproducto):
        data = request.json
        field_to_update = data.get('field')
        value = data.get('value')
        valid_fields = ['genero', 'url', 'descripcion', 'precio']

        if field_to_update in valid_fields:
            try:
                if field_to_update == 'url':
                    # No dividimos el valor para 'url', ya que se espera una lista de URLs
                    nuevo_valor = value
                    # Actualizamos los URLs y mantenemos la descripción
                    response = Pro.update(idproducto, field_to_update, nuevo_valor)
                    return jsonify({'message': response}), 200
                else:
                    response = Pro.update(idproducto, field_to_update, value)
                    return jsonify({'message': response}), 200
            except Exception as e:
                return jsonify({'message': str(e)}), 500
        else:
            return jsonify({'message': 'Campo no válido para actualización'}), 400


    @classmethod
    def delete(cls, idproducto):
        try:
            # Eliminar todas las imágenes con el nombre del álbum (descripción) proporcionado
            if Pro.delete(idproducto):
                return jsonify({'message': 'Producto eliminado exitosamente'}), 200
            else:
                raise userNotFound(idproducto)  # Si no se encuentran imágenes para eliminar, lanzar la excepción userNotFound
        except Exception as e:
            print("Error al eliminar el producto:", e)
            return jsonify ({'message': 'Error en la solicitud'}), 500   