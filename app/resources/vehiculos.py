from flask import request
from flask_restx import Namespace, Resource, fields
from ..models.vehiculo import Vehiculo
from ..extensions import db

vehiculos_ns = Namespace(
    "vehiculos", description="Operaciones relacionadas con vehículos"
)

vehiculo_model = vehiculos_ns.model(
    "Vehiculo",
    {
        "id": fields.Integer(readOnly=True, description="ID del vehículo"),
        "placa": fields.String(required=True, description="Placa del vehículo"),
        "capacidad_max": fields.Integer(required=True, description="Capacidad máxima"),
        "fecha_alta": fields.String(description="Fecha de alta"),
        "modelo": fields.String(description="Modelo del vehículo"),
        "anio_fabricacion": fields.Integer(description="Año de fabricación"),
        "id_tipo_transporte": fields.Integer(
            required=True, description="ID del tipo de transporte"
        ),
        "id_operador": fields.Integer(required=True, description="ID del operador"),
        "estado": fields.String(description="Estado del vehículo"),
    },
)


@vehiculos_ns.route("/")
class VehiculoList(Resource):
    @vehiculos_ns.marshal_list_with(vehiculo_model)
    def get(self):
        """Listar todos los vehículos activos"""
        return Vehiculo.get_all()

    @vehiculos_ns.expect(vehiculo_model)
    @vehiculos_ns.marshal_with(vehiculo_model, code=201)
    def post(self):
        """Crear un nuevo vehículo"""
        data = request.get_json()

        # Validar placa única
        if Vehiculo.query.filter_by(placa=data["placa"]).first():
            vehiculos_ns.abort(
                400, f"Ya existe un vehículo con la placa: {data['placa']}"
            )

        vehiculo = Vehiculo(
            placa=data["placa"],
            capacidad_max=data["capacidad_max"],
            fecha_alta=data.get("fecha_alta"),
            modelo=data.get("modelo"),
            anio_fabricacion=data.get("anio_fabricacion"),
            id_tipo_transporte=data["id_tipo_transporte"],
            id_operador=data["id_operador"],
        )

        db.session.add(vehiculo)
        db.session.commit()

        return vehiculo, 201


@vehiculos_ns.route("/<int:id>")
@vehiculos_ns.response(404, "Vehículo no encontrado")
@vehiculos_ns.param("id", "ID del vehículo")
class VehiculoDetail(Resource):
    @vehiculos_ns.marshal_with(vehiculo_model)
    def get(self, id):
        """Obtener un vehículo por ID"""
        vehiculo = Vehiculo.get_by_id(id)
        if not vehiculo:
            vehiculos_ns.abort(404, f"Vehículo con ID {id} no encontrado")
        return vehiculo

    @vehiculos_ns.expect(vehiculo_model)
    @vehiculos_ns.marshal_with(vehiculo_model)
    def put(self, id):
        """Actualizar un vehículo"""
        vehiculo = Vehiculo.get_by_id(id)
        if not vehiculo:
            vehiculos_ns.abort(404, f"Vehículo con ID {id} no encontrado")

        data = request.get_json()

        # Validar placa única si se está cambiando
        if "placa" in data and data["placa"] != vehiculo.placa:
            if Vehiculo.query.filter_by(placa=data["placa"]).first():
                vehiculos_ns.abort(
                    400, f"Ya existe un vehículo con la placa: {data['placa']}"
                )

        vehiculo.placa = data.get("placa", vehiculo.placa)
        vehiculo.capacidad_max = data.get("capacidad_max", vehiculo.capacidad_max)
        vehiculo.fecha_alta = data.get("fecha_alta", vehiculo.fecha_alta)
        vehiculo.modelo = data.get("modelo", vehiculo.modelo)
        vehiculo.anio_fabricacion = data.get(
            "anio_fabricacion", vehiculo.anio_fabricacion
        )
        vehiculo.id_tipo_transporte = data.get(
            "id_tipo_transporte", vehiculo.id_tipo_transporte
        )
        vehiculo.id_operador = data.get("id_operador", vehiculo.id_operador)

        db.session.commit()
        return vehiculo

    @vehiculos_ns.response(204, "Vehículo eliminado")
    def delete(self, id):
        """Eliminar (desactivar) un vehículo"""
        vehiculo = Vehiculo.get_by_id(id)
        if not vehiculo:
            vehiculos_ns.abort(404, f"Vehículo con ID {id} no encontrado")

        vehiculo.estado = "inactivo"
        db.session.commit()

        return "", 204
