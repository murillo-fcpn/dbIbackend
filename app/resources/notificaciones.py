from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.notificacion import Notificacion
from ..extensions import db
from datetime import datetime

notificaciones_ns = Namespace(
    "notificaciones", description="Operaciones relacionadas con notificaciones"
)

notificacion_model = notificaciones_ns.model(
    "Notificacion",
    {
        "id": fields.Integer(readonly=True),
        "titulo": fields.String(required=True),
        "mensaje": fields.String(required=True),
        "fecha_hora": fields.DateTime,
        "tipo": fields.String,
        "ciudadano_id": fields.Integer(required=True),
        "estado": fields.String,
    },
)


@notificaciones_ns.route("/")
class NotificacionList(Resource):
    @notificaciones_ns.marshal_list_with(notificacion_model)
    def get(self):
        """Obtener todas las notificaciones"""
        return Notificacion.get_all()

    @notificaciones_ns.expect(notificacion_model)
    @notificaciones_ns.marshal_with(notificacion_model, code=201)
    def post(self):
        """Crear una nueva notificación"""
        data = request.json
        nueva_notificacion = Notificacion(
            titulo=data["titulo"],
            mensaje=data["mensaje"],
            tipo=data.get("tipo"),
            ciudadano_id=data["ciudadano_id"],
        )
        nueva_notificacion.save()
        return nueva_notificacion, 201


@notificaciones_ns.route("/<int:id>")
@notificaciones_ns.response(404, "Notificación no encontrada")
class NotificacionResource(Resource):
    @notificaciones_ns.marshal_with(notificacion_model)
    def get(self, id):
        """Obtener una notificación por ID"""
        notificacion = Notificacion.get_by_id(id)
        if not notificacion:
            notificaciones_ns.abort(404, "Notificación no encontrada")
        return notificacion

    @notificaciones_ns.expect(notificacion_model)
    @notificaciones_ns.marshal_with(notificacion_model)
    def put(self, id):
        """Actualizar una notificación"""
        notificacion = Notificacion.get_by_id(id)
        if not notificacion:
            notificaciones_ns.abort(404, "Notificación no encontrada")

        data = request.json
        notificacion.titulo = data.get("titulo", notificacion.titulo)
        notificacion.mensaje = data.get("mensaje", notificacion.mensaje)
        notificacion.tipo = data.get("tipo", notificacion.tipo)
        notificacion.ciudadano_id = data.get(
            "ciudadano_id", notificacion.ciudadano_id
        )

        notificacion.save()
        return notificacion

    def delete(self, id):
        """Eliminar una notificación (soft delete)"""
        notificacion = Notificacion.get_by_id(id)
        if not notificacion:
            notificaciones_ns.abort(404, "Notificación no encontrada")
        notificacion.estado = "inactivo"
        notificacion.save()
        return "", 204
