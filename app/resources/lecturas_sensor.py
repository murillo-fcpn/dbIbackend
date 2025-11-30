from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.lectura_sensor import LecturaSensor
from ..extensions import db
from datetime import datetime

lecturas_sensor_ns = Namespace(
    "lecturas-sensor", description="Operaciones relacionadas con lecturas de sensores"
)

lectura_sensor_model = lecturas_sensor_ns.model(
    "LecturaSensor",
    {
        "id": fields.Integer(readonly=True),
        "valor": fields.Float(required=True),
        "unidad_medida": fields.String(required=True),
        "fecha": fields.Date(required=True),
        "hora": fields.String(required=True),  # Time as string
        "tipo_lectura": fields.String(required=True),
        "sensor_id": fields.Integer(required=True),
        "estado": fields.String,
    },
)


@lecturas_sensor_ns.route("/")
class LecturaSensorList(Resource):
    @lecturas_sensor_ns.marshal_list_with(lectura_sensor_model)
    def get(self):
        """Obtener todas las lecturas"""
        return LecturaSensor.get_all()

    @lecturas_sensor_ns.expect(lectura_sensor_model)
    @lecturas_sensor_ns.marshal_with(lectura_sensor_model, code=201)
    def post(self):
        """Crear una nueva lectura"""
        data = request.json
        fecha = datetime.strptime(data["fecha"], "%Y-%m-%d").date()
        hora = datetime.strptime(data["hora"], "%H:%M:%S").time()

        nueva_lectura = LecturaSensor(
            valor=data["valor"],
            unidad_medida=data["unidad_medida"],
            fecha=fecha,
            hora=hora,
            tipo_lectura=data["tipo_lectura"],
            sensor_id=data["sensor_id"],
        )
        nueva_lectura.save()
        return nueva_lectura, 201


@lecturas_sensor_ns.route("/<int:id>")
@lecturas_sensor_ns.response(404, "Lectura no encontrada")
class LecturaSensorResource(Resource):
    @lecturas_sensor_ns.marshal_with(lectura_sensor_model)
    def get(self, id):
        """Obtener una lectura por ID"""
        lectura = LecturaSensor.get_by_id(id)
        if not lectura:
            lecturas_sensor_ns.abort(404, "Lectura no encontrada")
        return lectura

    @lecturas_sensor_ns.expect(lectura_sensor_model)
    @lecturas_sensor_ns.marshal_with(lectura_sensor_model)
    def put(self, id):
        """Actualizar una lectura"""
        lectura = LecturaSensor.get_by_id(id)
        if not lectura:
            lecturas_sensor_ns.abort(404, "Lectura no encontrada")

        data = request.json
        lectura.valor = data.get("valor", lectura.valor)
        lectura.unidad_medida = data.get("unidad_medida", lectura.unidad_medida)
        lectura.tipo_lectura = data.get("tipo_lectura", lectura.tipo_lectura)
        lectura.sensor_id = data.get("sensor_id", lectura.sensor_id)

        if data.get("fecha"):
            lectura.fecha = datetime.strptime(data["fecha"], "%Y-%m-%d").date()
        if data.get("hora"):
            lectura.hora = datetime.strptime(data["hora"], "%H:%M:%S").time()

        lectura.save()
        return lectura

    def delete(self, id):
        """Eliminar una lectura (soft delete)"""
        lectura = LecturaSensor.get_by_id(id)
        if not lectura:
            lecturas_sensor_ns.abort(404, "Lectura no encontrada")
        lectura.estado = "inactivo"
        lectura.save()
        return "", 204
