from flask import request
from flask_restx import Namespace, Resource, fields
from ..models.conductor import Conductor
from ..extensions import db

conductores_ns = Namespace(
    "conductores", description="Operaciones relacionadas con conductores"
)

conductor_model = conductores_ns.model(
    "Conductor",
    {
        "id": fields.Integer(readOnly=True, description="ID del conductor"),
        "nombre": fields.String(required=True, description="Nombre del conductor"),
        "apellido": fields.String(required=True, description="Apellido del conductor"),
        "ci": fields.String(required=True, description="Cédula de identidad"),
        "licencia": fields.String(required=True, description="Número de licencia"),
        "vencimiento_licencia": fields.String(
            required=True, description="Fecha de vencimiento de licencia"
        ),
        "telefono": fields.String(description="Teléfono del conductor"),
        "estado": fields.String(description="Estado del conductor"),
    },
)


@conductores_ns.route("/")
class ConductorList(Resource):
    @conductores_ns.marshal_list_with(conductor_model)
    def get(self):
        """Listar todos los conductores activos"""
        return Conductor.get_all()

    @conductores_ns.expect(conductor_model)
    @conductores_ns.marshal_with(conductor_model, code=201)
    def post(self):
        """Crear un nuevo conductor"""
        data = request.get_json()

        # Validar CI único
        if Conductor.query.filter_by(ci=data["ci"]).first():
            conductores_ns.abort(400, f"Ya existe un conductor con la CI: {data['ci']}")

        conductor = Conductor(
            nombre=data["nombre"],
            apellido=data["apellido"],
            ci=data["ci"],
            licencia=data["licencia"],
            vencimiento_licencia=data["vencimiento_licencia"],
            telefono=data.get("telefono"),
        )

        db.session.add(conductor)
        db.session.commit()

        return conductor, 201


@conductores_ns.route("/<int:id>")
@conductores_ns.response(404, "Conductor no encontrado")
@conductores_ns.param("id", "ID del conductor")
class ConductorDetail(Resource):
    @conductores_ns.marshal_with(conductor_model)
    def get(self, id):
        """Obtener un conductor por ID"""
        conductor = Conductor.get_by_id(id)
        if not conductor:
            conductores_ns.abort(404, f"Conductor con ID {id} no encontrado")
        return conductor

    @conductores_ns.expect(conductor_model)
    @conductores_ns.marshal_with(conductor_model)
    def put(self, id):
        """Actualizar un conductor"""
        conductor = Conductor.get_by_id(id)
        if not conductor:
            conductores_ns.abort(404, f"Conductor con ID {id} no encontrado")

        data = request.get_json()

        # Validar CI único si se está cambiando
        if "ci" in data and data["ci"] != conductor.ci:
            if Conductor.query.filter_by(ci=data["ci"]).first():
                conductores_ns.abort(
                    400, f"Ya existe un conductor con la CI: {data['ci']}"
                )

        conductor.nombre = data.get("nombre", conductor.nombre)
        conductor.apellido = data.get("apellido", conductor.apellido)
        conductor.ci = data.get("ci", conductor.ci)
        conductor.licencia = data.get("licencia", conductor.licencia)
        conductor.vencimiento_licencia = data.get(
            "vencimiento_licencia", conductor.vencimiento_licencia
        )
        conductor.telefono = data.get("telefono", conductor.telefono)

        db.session.commit()
        return conductor

    @conductores_ns.response(204, "Conductor eliminado")
    def delete(self, id):
        """Eliminar (desactivar) un conductor"""
        conductor = Conductor.get_by_id(id)
        if not conductor:
            conductores_ns.abort(404, f"Conductor con ID {id} no encontrado")

        conductor.estado = "inactivo"
        db.session.commit()

        return "", 204
