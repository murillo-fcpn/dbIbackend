from flask import request
from flask_restx import Namespace, Resource, fields
from ..models.tipo_reclamo import TipoReclamo
from ..extensions import db

tipos_reclamo_ns = Namespace(
    "tipos-reclamo", description="Operaciones relacionadas con tipos de reclamo"
)

tipo_reclamo_model = tipos_reclamo_ns.model(
    "TipoReclamo",
    {
        "id": fields.Integer(readOnly=True, description="ID del tipo de reclamo"),
        "nombre": fields.String(
            required=True, description="Nombre del tipo de reclamo"
        ),
        "descripcion": fields.String(description="Descripción del tipo de reclamo"),
        "id_servicio": fields.Integer(
            required=True, description="ID del servicio asociado"
        ),
        "estado": fields.String(description="Estado del tipo de reclamo"),
    },
)


@tipos_reclamo_ns.route("/")
class TipoReclamoList(Resource):
    @tipos_reclamo_ns.marshal_list_with(tipo_reclamo_model)
    def get(self):
        """Listar todos los tipos de reclamo activos"""
        return TipoReclamo.get_all()

    @tipos_reclamo_ns.expect(tipo_reclamo_model)
    @tipos_reclamo_ns.marshal_with(tipo_reclamo_model, code=201)
    def post(self):
        """Crear un nuevo tipo de reclamo"""
        data = request.get_json()

        tipo_reclamo = TipoReclamo(
            nombre=data["nombre"],
            descripcion=data.get("descripcion"),
            id_servicio=data["id_servicio"],
        )

        db.session.add(tipo_reclamo)
        db.session.commit()

        return tipo_reclamo, 201


@tipos_reclamo_ns.route("/<int:id>")
@tipos_reclamo_ns.response(404, "Tipo de reclamo no encontrado")
@tipos_reclamo_ns.param("id", "ID del tipo de reclamo")
class TipoReclamoDetail(Resource):
    @tipos_reclamo_ns.marshal_with(tipo_reclamo_model)
    def get(self, id):
        """Obtener un tipo de reclamo por ID"""
        tipo_reclamo = TipoReclamo.get_by_id(id)
        if not tipo_reclamo:
            tipos_reclamo_ns.abort(404, f"Tipo de reclamo con ID {id} no encontrado")
        return tipo_reclamo

    @tipos_reclamo_ns.expect(tipo_reclamo_model)
    @tipos_reclamo_ns.marshal_with(tipo_reclamo_model)
    def put(self, id):
        """Actualizar un tipo de reclamo"""
        tipo_reclamo = TipoReclamo.get_by_id(id)
        if not tipo_reclamo:
            tipos_reclamo_ns.abort(404, f"Tipo de reclamo con ID {id} no encontrado")

        data = request.get_json()

        tipo_reclamo.nombre = data.get("nombre", tipo_reclamo.nombre)
        tipo_reclamo.descripcion = data.get("descripcion", tipo_reclamo.descripcion)
        tipo_reclamo.id_servicio = data.get("id_servicio", tipo_reclamo.id_servicio)

        db.session.commit()
        return tipo_reclamo

    @tipos_reclamo_ns.response(204, "Tipo de reclamo eliminado")
    def delete(self, id):
        """Eliminar (desactivar) un tipo de reclamo"""
        tipo_reclamo = TipoReclamo.get_by_id(id)
        if not tipo_reclamo:
            tipos_reclamo_ns.abort(404, f"Tipo de reclamo con ID {id} no encontrado")

        tipo_reclamo.estado = "inactivo"
        db.session.commit()

        return "", 204
