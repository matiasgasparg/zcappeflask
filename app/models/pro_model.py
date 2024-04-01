from ..database import DatabaseConnection
from app.models.date_model import Pro_date
from flask import Flask, request, jsonify

class Pro(Pro_date):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def get(cls, idproducto):
        try:
            query = """
                SELECT p.idproducto, p.genero, p.descripcion, p.precio, GROUP_CONCAT(pi.url) AS urls
                FROM producto p
                LEFT JOIN producto_has_imagen phi ON p.idproducto = phi.producto_idproducto
                LEFT JOIN imagen pi ON phi.imagen_idimagen = pi.idimagen
                WHERE p.idproducto = %s
                GROUP BY p.idproducto
            """
            result = DatabaseConnection.fetch_one(query, params=(idproducto,))

            if result:
                idproducto, genero, descripcion, precio, urls = result
                producto = cls(idproducto=idproducto, genero=genero, descripcion=descripcion, precio=precio)
                producto.urls_imagenes = urls.split(',')
                return producto
            else:
                return None
        except Exception as e:
            print("Error al obtener el producto:", e)
            return None
        finally:
            DatabaseConnection.close_connection()  # Cerrar la conexión después de realizar la consulta
    @classmethod
    def get_all(cls):
        try:
           query = """
               SELECT p.idproducto, p.genero, p.descripcion, p.precio, GROUP_CONCAT(pi.url) AS urls
               FROM producto p
               LEFT JOIN producto_has_imagen phi ON p.idproducto = phi.producto_idproducto
               LEFT JOIN imagen pi ON phi.imagen_idimagen = pi.idimagen
               GROUP BY p.idproducto
           """
           results = DatabaseConnection.fetch_all(query)

           productos = []
           for result in results:
               idproducto, genero, descripcion, precio, urls = result
               producto = Pro(idproducto=idproducto, genero=genero, descripcion=descripcion, precio=precio, url=urls.split(','))
               productos.append(producto)

           return productos
        except Exception as e:
           print("Error al obtener todos los productos:", e)
           return None
        finally:
            DatabaseConnection.close_connection()  # Cerrar la conexión después de realizar la consulta


    @classmethod
    def create(cls, pro):
        try:
            # Insertar el producto en la base de datos
            query = """
                INSERT INTO producto (genero, descripcion, precio) 
                VALUES (%s, %s, %s)
            """
            params = (pro.genero, pro.descripcion, pro.precio)
            DatabaseConnection.execute_query(query, params=params)

            # Obtener el ID del producto recién insertado
            query_get_last_insert_id = "SELECT LAST_INSERT_ID()"
            result = DatabaseConnection.fetch_one(query_get_last_insert_id)
            idproducto = result[0]

            # Insertar las URLs asociadas a las imágenes en la tabla de imágenes
            for url in pro.url:
                query_insert_url = """
                    INSERT INTO imagen (url, descripcion) 
                    VALUES (%s, %s)
                """
                params_url = (url, pro.descripcion)  # Asociar la misma descripción a todas las imágenes
                DatabaseConnection.execute_query(query_insert_url, params=params_url)

                # Obtener el ID de la imagen recién insertada
                query_get_last_insert_id = "SELECT LAST_INSERT_ID()"
                result = DatabaseConnection.fetch_one(query_get_last_insert_id)
                idimagen = result[0]

                # Establecer la relación entre el producto y la imagen en la tabla de relación
                query_insert_relation = """
                    INSERT INTO producto_has_imagen (producto_idproducto, imagen_idimagen) 
                    VALUES (%s, %s)
                """
                params_relation = (idproducto, idimagen)
                DatabaseConnection.execute_query(query_insert_relation, params=params_relation)

            return True
        except Exception as e:
            print("Error al crear el producto:", e)
            return False
        finally:
            DatabaseConnection.close_connection()  # Cerrar la conexión después de realizar la consulta
    @classmethod
    def delete(cls, idproducto):
        try:
            # Eliminar registros asociados en la tabla producto_has_imagen
            query_delete_relational = "DELETE FROM producto_has_imagen WHERE producto_idproducto = %s"
            params = (idproducto,)
            DatabaseConnection.execute_query(query_delete_relational, params=params)

            # Luego eliminar el producto
            query_delete_producto = "DELETE FROM producto WHERE idproducto = %s"
            DatabaseConnection.execute_query(query_delete_producto, params=params)

            return {'message': 'Producto eliminado exitosamente'}, 204
        except Exception as e:
            print("Error al eliminar el producto:", e)
            return {'message': 'Error en la solicitud'}, 500
        finally:
            DatabaseConnection.close_connection()  # Cerrar la conexión después de realizar la consulta
    @classmethod
    def update(cls, idproducto, campo, nuevo_valor):
        try:
            if campo == 'genero':
                query = "UPDATE producto SET genero = %s WHERE idproducto = %s"
            elif campo == 'descripcion':
                # Para la descripción, actualizamos solo si el valor no es None
                if nuevo_valor is not None:
                    query = "UPDATE producto SET descripcion = %s WHERE idproducto = %s"
                else:
                    return "La descripción no puede ser None"
            elif campo == 'precio':
                query = "UPDATE producto SET precio = %s WHERE idproducto = %s"
            elif campo == 'url':
                # Si el campo a actualizar es 'url', primero eliminamos todas las entradas asociadas al producto en la tabla de relación
                delete_query = "DELETE FROM producto_has_imagen WHERE producto_idproducto = %s"
                DatabaseConnection.execute_query(delete_query, params=(idproducto,))
    
                # Luego, insertamos las nuevas entradas en la tabla de relación
                for url in nuevo_valor:
                    # Aquí ejecutamos una consulta para obtener el ID de la imagen correspondiente al URL
                    query_obtener_id_imagen = "SELECT idimagen FROM imagen WHERE url = %s"
                    imagen_id = DatabaseConnection.fetch_one(query_obtener_id_imagen, params=(url,))
                    if imagen_id:
                        # Si la imagen ya existe en la base de datos, usamos su ID
                        imagen_id = imagen_id[0]
                    else:
                        # Si la imagen no existe, la insertamos en la tabla de imágenes y obtenemos su ID
                        insert_query = "INSERT INTO imagen (url) VALUES (%s)"
                        DatabaseConnection.execute_query(insert_query, params=(url,))
                        imagen_id = DatabaseConnection.fetch_one("SELECT LAST_INSERT_ID()")[0]
    
                    # Insertamos la entrada en la tabla de relación
                    insert_query_relacion = "INSERT INTO producto_has_imagen (producto_idproducto, imagen_idimagen) VALUES (%s, %s)"
                    DatabaseConnection.execute_query(insert_query_relacion, params=(idproducto, imagen_id))
    
                return 'URLs actualizados exitosamente'
            else:
                raise ValueError("Campo no válido para actualización")
    
            params = (nuevo_valor, idproducto)
            DatabaseConnection.execute_query(query, params=params)
    
            return f'{campo.capitalize()} actualizado exitosamente'
        except Exception as e:
            print(f"Error al actualizar el campo '{campo}':", e)
            return 'Error en la solicitud'
        finally:
            DatabaseConnection.close_connection()  # Cerrar la conexión después de realizar la consulta

    @classmethod
    def exists(cls, idproducto):
        query = "SELECT COUNT(*) FROM producto WHERE idproducto = %s"
        params = (idproducto,)
        result = DatabaseConnection.fetch_one(query, params=params)
        return result[0] > 0