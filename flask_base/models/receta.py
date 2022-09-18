import os

from flask_base.config.mysqlconnection import connectToMySQL
from flask_base.models.modelo_base import ModeloBase

class Receta(ModeloBase):
    
    modelo = 'receta'
    campos = ['nombre','descripcion','instrucciones','fecha_elaboracion','menos_30','usuarios_id']

    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.descripcion = data['descripcion']
        self.instrucciones = data['instrucciones']
        self.fecha_elaboracion = data['fecha_elaboracion']
        self.menos_30 = data['menos_30']
        self.usuario_id = data['usuarios_id']
        self.usuario_nombre = data['usuarios.nombre']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all_width_user(cls):
        query = f"SELECT * FROM {cls.modelo} JOIN usuarios ON usuarios.id = {cls.modelo}.usuarios_id;"
        results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query)
        print("AQUI QUIERO VER -->",results)
        all_data = []
        for data in results:
            all_data.append(cls(data))
        return all_data