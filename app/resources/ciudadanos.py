from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.ciudadano import Ciudadano
from ..extensions import db
from datetime import datetime

ciudadanos_ns = Namespace(
    "ciudadanos", description="Operaciones relacionadas con ciudadanos"
)

ciudadano_model = ciudadanos_ns.model(
    "Ciudadano",
    {
        "id": fields.Integer(readonly=True),
        "nombre": fields.String(required=True),
        "apellido": fields.String(required=True),
        "ci": fields.String(required=True),
        "telefono": fields.String,
        "email": fields.String,
        "direccion": fields.String,
        "latitud": fields.Float,
        "longitud": fields.Float,
        "fecha_nacimiento": fields.Date,
        "estado": fields.String,
    },
)


@ciudadanos_ns.route("/")
class CiudadanoList(Resource):
    @ciudadanos_ns.marshal_list_with(ciudadano_model)
    def get(self):
        """Obtener todos los ciudadanos"""
        return Ciudadano.get_all()

    @ciudadanos_ns.expect(ciudadano_model)
    @ciudadanos_ns.marshal_with(ciudadano_model, code=201)
    def post(self):
        """Crear un nuevo ciudadano"""
        data = request.json
        fecha_nacimiento = None
        if data.get("fecha_nacimiento"):
            fecha_nacimiento = datetime.strptime(
                data["fecha_nacimiento"], "%Y-%m-%d"
            ).date()

        nuevo_ciudadano = Ciudadano(
            nombre=data["nombre"],
            apellido=data["apellido"],
            ci=data["ci"],
            telefono=data.get("telefono"),
            email=data.get("email"),
            direccion=data.get("direccion"),
            latitud=data.get("latitud"),
            longitud=data.get("longitud"),
            fecha_nacimiento=fecha_nacimiento,
        )
        nuevo_ciudadano.save()
        return nuevo_ciudadano, 201


@ciudadanos_ns.route("/<int:id>")
@ciudadanos_ns.response(404, "Ciudadano no encontrado")
class CiudadanoResource(Resource):
    @ciudadanos_ns.marshal_with(ciudadano_model)
    def get(self, id):
        """Obtener un ciudadano por ID"""
        ciudadano = Ciudadano.get_by_id(id)
        if not ciudadano:
            ciudadanos_ns.abort(404, "Ciudadano no encontrado")
        return ciudadano

    @ciudadanos_ns.expect(ciudadano_model)
    @ciudadanos_ns.marshal_with(ciudadano_model)
    def put(self, id):
        """Actualizar un ciudadano"""
        ciudadano = Ciudadano.get_by_id(id)
        if not ciudadano:
            ciudadanos_ns.abort(404, "Ciudadano no encontrado")

        data = request.json
        ciudadano.nombre = data.get("nombre", ciudadano.nombre)
        ciudadano.apellido = data.get("apellido", ciudadano.apellido)
        ciudadano.ci = data.get("ci", ciudadano.ci)
        ciudadano.telefono = data.get("telefono", ciudadano.telefono)
        ciudadano.email = data.get("email", ciudadano.email)
        ciudadano.direccion = data.get("direccion", ciudadano.direccion)
        ciudadano.latitud = data.get("latitud", ciudadano.latitud)
        ciudadano.longitud = data.get("longitud", ciudadano.longitud)

        if data.get("fecha_nacimiento"):
            ciudadano.fecha_nacimiento = datetime.strptime(
                data["fecha_nacimiento"], "%Y-%m-%d"
            ).date()

        ciudadano.save()
        return ciudadano

    def delete(self, id):
        """Eliminar un ciudadano (soft delete)"""
        ciudadano = Ciudadano.get_by_id(id)
        if not ciudadano:
            ciudadanos_ns.abort(404, "Ciudadano no encontrado")
        ciudadano.estado = "inactivo"
        ciudadano.save()
        return "", 204
