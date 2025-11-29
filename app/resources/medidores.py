from flask import request
from flask_restx import Namespace, Resource, fields
from ..models.medidor import Medidor
from ..extensions import db

medidores_ns = Namespace(
    "medidores", description="Operaciones relacionadas con medidores"
)

medidor_model = medidores_ns.model(
    "Medidor",
    {
        "id": fields.Integer(readOnly=True, description="ID del medidor"),
        "numero_serie": fields.String(
            required=True, description="Número de serie del medidor"
        ),
        "tipo": fields.String(required=True, description="Tipo de medidor"),
        "ubicacion": fields.String(description="Ubicación del medidor"),
        "fecha_instalacion": fields.String(description="Fecha de instalación"),
        "id_servicio": fields.Integer(required=True, description="ID del servicio"),
        "id_ciudadano": fields.Integer(description="ID del ciudadano"),
        "estado": fields.String(description="Estado del medidor"),
    },
)


@medidores_ns.route("/")
class MedidorList(Resource):
    @medidores_ns.marshal_list_with(medidor_model)
    def get(self):
        """Listar todos los medidores activos"""
        return Medidor.get_all()

    @medidores_ns.expect(medidor_model)
    @medidores_ns.marshal_with(medidor_model, code=201)
    def post(self):
        """Crear un nuevo medidor"""
        data = request.get_json()

        # Validar número de serie único
        if Medidor.query.filter_by(numero_serie=data["numero_serie"]).first():
            medidores_ns.abort(
                400,
                f"Ya existe un medidor con el número de serie: {data['numero_serie']}",
            )

        medidor = Medidor(
            numero_serie=data["numero_serie"],
            tipo=data["tipo"],
            ubicacion=data.get("ubicacion"),
            fecha_instalacion=data.get("fecha_instalacion"),
            id_servicio=data["id_servicio"],
            id_ciudadano=data.get("id_ciudadano"),
        )

        db.session.add(medidor)
        db.session.commit()

        return medidor, 201


@medidores_ns.route("/<int:id>")
@medidores_ns.response(404, "Medidor no encontrado")
@medidores_ns.param("id", "ID del medidor")
class MedidorDetail(Resource):
    @medidores_ns.marshal_with(medidor_model)
    def get(self, id):
        """Obtener un medidor por ID"""
        medidor = Medidor.get_by_id(id)
        if not medidor:
            medidores_ns.abort(404, f"Medidor con ID {id} no encontrado")
        return medidor

    @medidores_ns.expect(medidor_model)
    @medidores_ns.marshal_with(medidor_model)
    def put(self, id):
        """Actualizar un medidor"""
        medidor = Medidor.get_by_id(id)
        if not medidor:
            medidores_ns.abort(404, f"Medidor con ID {id} no encontrado")

        data = request.get_json()

        # Validar número de serie único si se está cambiando
        if "numero_serie" in data and data["numero_serie"] != medidor.numero_serie:
            if Medidor.query.filter_by(numero_serie=data["numero_serie"]).first():
                medidores_ns.abort(
                    400,
                    f"Ya existe un medidor con el número de serie: {data['numero_serie']}",
                )

        medidor.numero_serie = data.get("numero_serie", medidor.numero_serie)
        medidor.tipo = data.get("tipo", medidor.tipo)
        medidor.ubicacion = data.get("ubicacion", medidor.ubicacion)
        medidor.fecha_instalacion = data.get(
            "fecha_instalacion", medidor.fecha_instalacion
        )
        medidor.id_servicio = data.get("id_servicio", medidor.id_servicio)
        medidor.id_ciudadano = data.get("id_ciudadano", medidor.id_ciudadano)

        db.session.commit()
        return medidor

    @medidores_ns.response(204, "Medidor eliminado")
    def delete(self, id):
        """Eliminar (desactivar) un medidor"""
        medidor = Medidor.get_by_id(id)
        if not medidor:
            medidores_ns.abort(404, f"Medidor con ID {id} no encontrado")

        medidor.estado = "inactivo"
        db.session.commit()

        return "", 204
