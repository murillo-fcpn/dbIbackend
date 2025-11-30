from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.sensor import Sensor
from ..extensions import db
from datetime import datetime

sensores_ns = Namespace("sensores", description="Operaciones relacionadas con sensores")

sensor_model = sensores_ns.model(
    "Sensor",
    {
        "id": fields.Integer(readonly=True),
        "codigo": fields.String(required=True),
        "tipo": fields.String(required=True),
        "ubicacion": fields.String,
        "latitud": fields.Float,
        "longitud": fields.Float,
        "fecha_instalacion": fields.Date,
        "zona_id": fields.Integer(required=True),
        "estado": fields.String,
    },
)


@sensores_ns.route("/")
class SensorList(Resource):
    @sensores_ns.marshal_list_with(sensor_model)
    def get(self):
        """Obtener todos los sensores"""
        return Sensor.get_all()

    @sensores_ns.expect(sensor_model)
    @sensores_ns.marshal_with(sensor_model, code=201)
    def post(self):
        """Crear un nuevo sensor"""
        data = request.json
        fecha_instalacion = None
        if data.get("fecha_instalacion"):
            fecha_instalacion = datetime.strptime(
                data["fecha_instalacion"], "%Y-%m-%d"
            ).date()

        nuevo_sensor = Sensor(
            codigo=data["codigo"],
            tipo=data["tipo"],
            ubicacion=data.get("ubicacion"),
            latitud=data.get("latitud"),
            longitud=data.get("longitud"),
            fecha_instalacion=fecha_instalacion,
            zona_id=data["zona_id"],
        )
        nuevo_sensor.save()
        return nuevo_sensor, 201


@sensores_ns.route("/<int:id>")
@sensores_ns.response(404, "Sensor no encontrado")
class SensorResource(Resource):
    @sensores_ns.marshal_with(sensor_model)
    def get(self, id):
        """Obtener un sensor por ID"""
        sensor = Sensor.get_by_id(id)
        if not sensor:
            sensores_ns.abort(404, "Sensor no encontrado")
        return sensor

    @sensores_ns.expect(sensor_model)
    @sensores_ns.marshal_with(sensor_model)
    def put(self, id):
        """Actualizar un sensor"""
        sensor = Sensor.get_by_id(id)
        if not sensor:
            sensores_ns.abort(404, "Sensor no encontrado")

        data = request.json
        sensor.codigo = data.get("codigo", sensor.codigo)
        sensor.tipo = data.get("tipo", sensor.tipo)
        sensor.ubicacion = data.get("ubicacion", sensor.ubicacion)
        sensor.latitud = data.get("latitud", sensor.latitud)
        sensor.longitud = data.get("longitud", sensor.longitud)
        sensor.zona_id = data.get("zona_id", sensor.zona_id)

        if data.get("fecha_instalacion"):
            sensor.fecha_instalacion = datetime.strptime(
                data["fecha_instalacion"], "%Y-%m-%d"
            ).date()

        sensor.save()
        return sensor

    def delete(self, id):
        """Eliminar un sensor (soft delete)"""
        sensor = Sensor.get_by_id(id)
        if not sensor:
            sensores_ns.abort(404, "Sensor no encontrado")
        sensor.estado = "inactivo"
        sensor.save()
        return "", 204
