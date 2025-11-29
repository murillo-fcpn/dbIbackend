from flask import request
from flask_restx import Namespace, Resource, fields
from ..models.servicio import Servicio
from ..extensions import db

servicios_ns = Namespace(
    "servicios", description="Operaciones relacionadas con servicios"
)

# Modelos para la documentación de la API
servicio_model = servicios_ns.model(
    "Servicio",
    {
        "id": fields.Integer(readOnly=True, description="ID del servicio"),
        "nombre": fields.String(required=True, description="Nombre del servicio"),
        "tipo": fields.String(
            required=True, description="Tipo de servicio (agua, luz, gas)"
        ),
        "descripcion": fields.String(description="Descripción del servicio"),
        "estado": fields.String(description="Estado del servicio"),
    },
)


@servicios_ns.route("/")
class ServicioList(Resource):
    @servicios_ns.marshal_list_with(servicio_model)
    def get(self):
        """Listar todos los servicios activos"""
        return Servicio.get_all()

    @servicios_ns.expect(servicio_model)
    @servicios_ns.marshal_with(servicio_model, code=201)
    def post(self):
        """Crear un nuevo servicio"""
        data = request.get_json()

        # Validar que no exista un servicio con el mismo nombre
        if Servicio.query.filter_by(nombre=data["nombre"]).first():
            servicios_ns.abort(
                400, f"Ya existe un servicio con el nombre: {data['nombre']}"
            )

        servicio = Servicio(
            nombre=data["nombre"],
            tipo=data["tipo"],
            descripcion=data.get("descripcion"),
        )

        db.session.add(servicio)
        db.session.commit()

        return servicio, 201


@servicios_ns.route("/<int:id>")
@servicios_ns.response(404, "Servicio no encontrado")
@servicios_ns.param("id", "ID del servicio")
class ServicioDetail(Resource):
    @servicios_ns.marshal_with(servicio_model)
    def get(self, id):
        """Obtener un servicio por ID"""
        servicio = Servicio.get_by_id(id)
        if not servicio:
            servicios_ns.abort(404, f"Servicio con ID {id} no encontrado")
        return servicio

    @servicios_ns.expect(servicio_model)
    @servicios_ns.marshal_with(servicio_model)
    def put(self, id):
        """Actualizar un servicio"""
        servicio = Servicio.get_by_id(id)
        if not servicio:
            servicios_ns.abort(404, f"Servicio con ID {id} no encontrado")

        data = request.get_json()

        # Validar nombre único si se está cambiando
        if "nombre" in data and data["nombre"] != servicio.nombre:
            if Servicio.query.filter_by(nombre=data["nombre"]).first():
                servicios_ns.abort(
                    400, f"Ya existe un servicio con el nombre: {data['nombre']}"
                )

        servicio.nombre = data.get("nombre", servicio.nombre)
        servicio.tipo = data.get("tipo", servicio.tipo)
        servicio.descripcion = data.get("descripcion", servicio.descripcion)

        db.session.commit()
        return servicio

    @servicios_ns.response(204, "Servicio eliminado")
    def delete(self, id):
        """Eliminar (desactivar) un servicio"""
        servicio = Servicio.get_by_id(id)
        if not servicio:
            servicios_ns.abort(404, f"Servicio con ID {id} no encontrado")

        servicio.estado = "inactivo"
        db.session.commit()

        return "", 204
