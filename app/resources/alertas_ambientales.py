from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.alerta_ambiental import AlertaAmbiental
from ..extensions import db
from datetime import datetime

alertas_ambientales_ns = Namespace(
    "alertas-ambientales", description="Operaciones relacionadas con alertas ambientales"
)

alerta_ambiental_model = alertas_ambientales_ns.model(
    "AlertaAmbiental",
    {
        "id": fields.Integer(readonly=True),
        "fecha": fields.Date(required=True),
        "hora": fields.String(required=True),  # Time as string
        "tipo_alerta": fields.String(required=True),
        "descripcion": fields.String,
        "sensor_id": fields.Integer(required=True),
        "estado": fields.String,
    },
)


@alertas_ambientales_ns.route("/")
class AlertaAmbientalList(Resource):
    @alertas_ambientales_ns.marshal_list_with(alerta_ambiental_model)
    def get(self):
        """Obtener todas las alertas"""
        return AlertaAmbiental.get_all()

    @alertas_ambientales_ns.expect(alerta_ambiental_model)
    @alertas_ambientales_ns.marshal_with(alerta_ambiental_model, code=201)
    def post(self):
        """Crear una nueva alerta"""
        data = request.json
        fecha = datetime.strptime(data["fecha"], "%Y-%m-%d").date()
        hora = datetime.strptime(data["hora"], "%H:%M:%S").time()

        nueva_alerta = AlertaAmbiental(
            fecha=fecha,
            hora=hora,
            tipo_alerta=data["tipo_alerta"],
            descripcion=data.get("descripcion"),
            sensor_id=data["sensor_id"],
        )
        nueva_alerta.save()
        return nueva_alerta, 201


@alertas_ambientales_ns.route("/<int:id>")
@alertas_ambientales_ns.response(404, "Alerta no encontrada")
class AlertaAmbientalResource(Resource):
    @alertas_ambientales_ns.marshal_with(alerta_ambiental_model)
    def get(self, id):
        """Obtener una alerta por ID"""
        alerta = AlertaAmbiental.get_by_id(id)
        if not alerta:
            alertas_ambientales_ns.abort(404, "Alerta no encontrada")
        return alerta

    @alertas_ambientales_ns.expect(alerta_ambiental_model)
    @alertas_ambientales_ns.marshal_with(alerta_ambiental_model)
    def put(self, id):
        """Actualizar una alerta"""
        alerta = AlertaAmbiental.get_by_id(id)
        if not alerta:
            alertas_ambientales_ns.abort(404, "Alerta no encontrada")

        data = request.json
        alerta.tipo_alerta = data.get("tipo_alerta", alerta.tipo_alerta)
        alerta.descripcion = data.get("descripcion", alerta.descripcion)
        alerta.sensor_id = data.get("sensor_id", alerta.sensor_id)

        if data.get("fecha"):
            alerta.fecha = datetime.strptime(data["fecha"], "%Y-%m-%d").date()
        if data.get("hora"):
            alerta.hora = datetime.strptime(data["hora"], "%H:%M:%S").time()

        alerta.save()
        return alerta

    def delete(self, id):
        """Eliminar una alerta (soft delete)"""
        alerta = AlertaAmbiental.get_by_id(id)
        if not alerta:
            alertas_ambientales_ns.abort(404, "Alerta no encontrada")
        alerta.estado = "inactivo"
        alerta.save()
        return "", 204
