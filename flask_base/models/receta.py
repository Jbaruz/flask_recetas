import os

from flask_base.config.mysqlconnection import connectToMySQL
from flask_base.models.modelo_base import ModeloBase
from flask import flash

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
    
    @classmethod
    def update(cls,data):
        query = """UPDATE receta SET
                        nombre = %(nombre)s,
                        descripcion = %(descripcion)s,
                        instrucciones = %(instrucciones)s,
                        fecha_elaboracion = %(fecha_elaboracion)s,
                        menos_30 = %(menos_30)s,
                        updated_at=NOW() 
                    WHERE id = %(id)s"""
        resultado = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query, data)
        print("RESULTADO: ", resultado)
        return resultado
    
    @staticmethod
    def validar_largo(data, campo, largo):
        is_valid = True
        if len(data[campo]) <= largo:
            flash(f'El largo del {campo} no puede ser menor o igual {largo}', 'error')
            is_valid = False
        return is_valid

    @classmethod
    def validar(cls, data):

        is_valid = True

        is_valid = cls.validar_largo(data, 'nombre', 3)
        if not is_valid:
            is_valid = cls.validar_largo(data, 'descripcion', 3)
            is_valid = False
        if not is_valid:
            is_valid = cls.validar_largo(data, 'instrucciones', 3)
            is_valid = False
        if not is_valid:
            is_valid = cls.validar_largo(data, 'fecha_elaboracion', 9)
            is_valid = False


        return is_valid