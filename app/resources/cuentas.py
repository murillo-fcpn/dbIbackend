from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.cuenta import Cuenta
from ..extensions import db
from datetime import datetime

cuentas_ns = Namespace("cuentas", description="Operaciones relacionadas con cuentas")

cuenta_model = cuentas_ns.model(
    "Cuenta",
    {
        "id": fields.Integer(readonly=True),
        "usuario": fields.String(required=True),
        "email": fields.String(required=True),
        "rol_id": fields.Integer(required=True),
        "fecha_creacion": fields.DateTime,
        "estado": fields.String,
    },
)

cuenta_input_model = cuentas_ns.model(
    "CuentaInput",
    {
        "usuario": fields.String(required=True),
        "email": fields.String(required=True),
        "contrasena": fields.String(required=True),
        "rol_id": fields.Integer(required=True),
    },
)


@cuentas_ns.route("/")
class CuentaList(Resource):
    @cuentas_ns.marshal_list_with(cuenta_model)
    def get(self):
        """Obtener todas las cuentas"""
        return Cuenta.get_all()

    @cuentas_ns.expect(cuenta_input_model)
    @cuentas_ns.marshal_with(cuenta_model, code=201)
    def post(self):
        """Crear una nueva cuenta"""
        data = request.json
        nueva_cuenta = Cuenta(
            usuario=data["usuario"], email=data["email"], rol_id=data["rol_id"]
        )
        nueva_cuenta.set_password(data["contrasena"])
        nueva_cuenta.save()
        return nueva_cuenta, 201


@cuentas_ns.route("/<int:id>")
@cuentas_ns.response(404, "Cuenta no encontrada")
class CuentaResource(Resource):
    @cuentas_ns.marshal_with(cuenta_model)
    def get(self, id):
        """Obtener una cuenta por ID"""
        cuenta = Cuenta.get_by_id(id)
        if not cuenta:
            cuentas_ns.abort(404, "Cuenta no encontrada")
        return cuenta

    @cuentas_ns.expect(cuenta_input_model)
    @cuentas_ns.marshal_with(cuenta_model)
    def put(self, id):
        """Actualizar una cuenta"""
        cuenta = Cuenta.get_by_id(id)
        if not cuenta:
            cuentas_ns.abort(404, "Cuenta no encontrada")

        data = request.json
        cuenta.usuario = data.get("usuario", cuenta.usuario)
        cuenta.email = data.get("email", cuenta.email)
        cuenta.rol_id = data.get("rol_id", cuenta.rol_id)

        if data.get("contrasena"):
            cuenta.set_password(data["contrasena"])

        cuenta.save()
        return cuenta

    def delete(self, id):
        """Eliminar una cuenta (soft delete)"""
        cuenta = Cuenta.get_by_id(id)
        if not cuenta:
            cuentas_ns.abort(404, "Cuenta no encontrada")
        cuenta.estado = "inactivo"
        cuenta.save()
        return "", 204
