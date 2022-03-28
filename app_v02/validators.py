
from marshmallow import Schema, fields
from marshmallow import validate, ValidationError


class CreateRegisterSchema(Schema):

    nombres = fields.Str(required=True, validate=validate.Length(min=0, max=200))

    apellidos = fields.Str(required=True, validate=validate.Length(min=0, max=200))

    password = fields.Str(required=True, validate=validate.Length(min=8, max=12))

    correo = fields.Str(required=True, validate=validate.Email())

class CreateLoginSchema(Schema):

    password = fields.Str(required=True, validate=validate.Length(min=8, max=12))
    correo = fields.Str(required=True, validate=validate.Email())


class CreateCrearProducto(Schema):
    nombres = fields.Str(required=True, validate=validate.Length(min=0, max=200))
    
    precio = fields.Int(Required=True, validate=validate.Range(min=0, max=1000000))

