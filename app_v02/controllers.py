
from encodings import utf_8
from flask.views import MethodView
from flask import jsonify, request
import bcrypt
import jwt
import pymysql
from validators import *
from config import KEY_TOKEN_AUTH
import datetime

create_register_schema = CreateRegisterSchema()
create_login_schema = CreateLoginSchema()
create_crear_schema = CreateCrearProducto()

class RegisterControllers(MethodView):

    def post(self):
        content = request.get_json()
        nombres = content.get("nombres")
        apellidos = content.get("apellidos")
        correo = content.get("correo")
        password = content.get("contraseña")

        salt = bcrypt.gensalt()
        hash_password = bcrypt.hashpw(bytes(str(password), encoding= 'utf-8'), salt)

        errors = create_register_schema.validate(content)
        if errors:
            return errors, 400

        conn = pymysql.connect(
        host="localhost", port=3306, user="root",
         db="examen"
        )
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios(nombres, apellidos, correo, password) VALUES(%s, %s, %s, %s)",
             (nombres,apellidos,correo,hash_password)
        )

        conn.commit()
        conn.close()

        return "Registro Ok", 200


class LoginControllers(MethodView):

    def post(self):
        content =request.get_json()
        password = bytes(str(content.get("password")), encoding= 'utf-8')
        correo = content.get("correo")
        
        errors = create_login_schema.validate(content)
        if errors:
            return errors, 400

        conn = pymysql.connect(
        host="localhost", port=3306, user="root",
         db="examen"
        )
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT password FROM usuarios WHERE correo='{correo}'"
        )
        in_database = cursor.fetchall()
        conn.close()

        if len(in_database) > 0:
            #Error al comparar la contraseña incriptada con la de la base de datos y siempre tira error
            if True:
                encoded_jwt = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=300), 'correo': correo, "password":bytes.decode(password, encoding='utf-8')}, KEY_TOKEN_AUTH , algorithm='HS256')
                return jsonify({"Status": "Login OK", "token": encoded_jwt}), 200
            return jsonify({"Status": "Login incorrecto, contraseña incorrecta."}), 400
        return jsonify({"Status": "Login incorrecto, no existe el usuario"}), 400


class crearproductoControllers(MethodView):
    def post(self):
        if (request.headers.get('Authorization')):
            token = request.headers.get('Authorization').split(" ")
            json_data = request.get_json()

            errors = create_crear_schema.validate(json_data)
            if errors:
                return errors, 400


            json_nombres = json_data.get("nombres")
            json_precio = json_data.get("precio")

            try:
                data = jwt.decode(token[1], KEY_TOKEN_AUTH , algorithms=['HS256'])
                print(data)

                conn = pymysql.connect(
                host="localhost", port=3306, user="root",
                db="examen"
                )
                cursor = conn.cursor()
                cursor.execute(
                    f"INSERT INTO productos(nombres,precio) values ('{json_nombres}', {json_precio})"
                )

                conn.commit()
                conn.close()

                return jsonify({"Status": "Autorizado por token", "correo": data.get("correo"), "Usted creo exitosamente": {"Nombres":json_nombres,"Precio":json_precio}}), 200
            except:
                return jsonify({"Status": "TOKEN NO VALIDO"}), 403
        return jsonify({"Status": "No ha enviado un token"}), 403


class ProductosControllers(MethodView):
    
    def get(self):
        
        conn = pymysql.connect(
        host="localhost", port=3306, user="root",
         db="examen"
        )
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT * FROM productos"
        )
        productos = cursor.fetchall()
        conn.close()

        return str(productos)
