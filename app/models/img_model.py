from ..database import DatabaseConnection
from app.models.date_model import Img_date
class Img(Img_date):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    @classmethod
    def get(cls, idimagen):
 

        query = """SELECT idimagen, genero, url, descripcion,
        precio 
        FROM producto WHERE idimagen = %s"""
        params = idimagen,
        result = DatabaseConnection.fetch_one(query, params=params)

        if result is not None:
            return cls(**dict(zip(['idimagen', 'genero', 'url', 'descripcion', 'precio'], result)))
        return None
    @classmethod
    def get_all(cls):

        query = """SELECT idimagen, genero, url, descripcion,
        precio 
        FROM producto"""
        results = DatabaseConnection.fetch_all(query)

        imgs = []
        if results is not None:
            for result in results:
                imgs.append(cls(**dict(zip(['idimagen', 'genero', 'url', 'descripcion', 'precio'], result))))
        return imgs
    @classmethod
    def create(cls, img):
        try:
            query = """INSERT INTO producto (genero, url, descripcion, precio) 
                       VALUES (%s, %s, %s, %s)"""  # Corregir la consulta SQL
    
            params = (img.genero, img.url, img.descripcion, img.precio)  # Corregir la tupla de parámetros
            DatabaseConnection.execute_query(query, params=params)
            return True
        except Exception as e:
            print("Error al crear la IMAGEN:", e)
            return False
    @classmethod
    def delete(cls, idimagen):

        query = "DELETE FROM producto WHERE idimagen = %s"
        params = idimagen,
        DatabaseConnection.execute_query(query, params=params)
    @classmethod
    def update(cls,idimagen, campo, nuevo_valor):
  
        if campo == 'genero':
            query = "UPDATE producto SET genero = %s WHERE idimagen = %s"
        elif campo == 'url':
            query = "UPDATE producto SET url = %s WHERE idimagen = %s"
        elif campo == 'descripcion':
            query = "UPDATE producto SET descripcion = %s WHERE idimagen = %s"
        elif campo == 'precio':  # Cambiado 'contraseña' a 'password'
            query = "UPDATE producto SET precio = %s WHERE idimagen = %s"
    
        else:
            raise ValueError("Campo no válido para actualización")
        print(nuevo_valor, idimagen,query,campo)
        params = (nuevo_valor, idimagen)

        DatabaseConnection.execute_query(query,params=params)

        return True
    @classmethod
    def exists(cls, idimagen):
        query = "SELECT COUNT(*) FROM producto WHERE idimagen = %s"
        params = (idimagen,)

        result = DatabaseConnection.fetch_one(query, params=params)
        return result[0] > 0 
        