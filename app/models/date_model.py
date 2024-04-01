class User_date:
    def __init__(self, **kwargs):
        self.id_usuario = kwargs.get('id_usuario')
        self.name = kwargs.get('name')
        self.username = kwargs.get('username')
        self.email = kwargs.get('email')
        self.password = kwargs.get('password')
        self.admin = kwargs.get('admin')  


    def serialize(self):
        return {
            "id_usuario": self.id_usuario,
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "admin":self.admin
        }
class Img_date:
    def __init__(self, **kwargs):
        self.idimagen = kwargs.get('idimagen')
        self.url = kwargs.get('url')
        self.descripcion = kwargs.get('descripcion') 



    def serialize(self):
        return {
            "idimagen": self.idimagen,
            "url": self.url,
            "descripcion": self.descripcion,
        }
       
class Pro_date:
    def __init__(self, **kwargs):
        self.idproducto = kwargs.get('idproducto')
        self.genero = kwargs.get('genero')
        self.url = kwargs.get('url')
        self.descripcion = kwargs.get('descripcion') 
        self.precio = kwargs.get('precio')



    def serialize(self):
        return {
            "idproducto": self.idproducto,
            "genero": self.genero,
            "url": self.url,
            "descripcion": self.descripcion,
            "precio": self.precio
        }
