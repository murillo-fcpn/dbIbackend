from flask import request
from flask_restx import Namespace, Resource, fields
from ..models.tipo_incidente import TipoIncidente
from ..extensions import db

tipos_incidente_ns = Namespace(
    "tipos-incidente", description="Operaciones relacionadas con tipos de incidente"
)

tipo_incidente_model = tipos_incidente_ns.model(
    "TipoIncidente",
    {
        "id": fields.Integer(readOnly=True, description="ID del tipo de incidente"),
        "nombre": fields.String(
            required=True, description="Nombre del tipo de incidente"
        ),
        "descripcion": fields.String(description="Descripción del tipo de incidente"),
        "categoria": fields.String(
            required=True, description="Categoría (transito, mecanico, seguridad)"
        ),
        "estado": fields.String(description="Estado del tipo de incidente"),
    },
)


@tipos_incidente_ns.route("/")
class TipoIncidenteList(Resource):
    @tipos_incidente_ns.marshal_list_with(tipo_incidente_model)
    def get(self):
        """Listar todos los tipos de incidente activos"""
        return TipoIncidente.get_all()

    @tipos_incidente_ns.expect(tipo_incidente_model)
    @tipos_incidente_ns.marshal_with(tipo_incidente_model, code=201)
    def post(self):
        """Crear un nuevo tipo de incidente"""
        data = request.get_json()

        # Validar nombre único
        if TipoIncidente.query.filter_by(nombre=data["nombre"]).first():
            tipos_incidente_ns.abort(
                400, f"Ya existe un tipo de incidente con el nombre: {data['nombre']}"
            )

        tipo_incidente = TipoIncidente(
            nombre=data["nombre"],
            descripcion=data.get("descripcion"),
            categoria=data["categoria"],
        )

        db.session.add(tipo_incidente)
        db.session.commit()

        return tipo_incidente, 201


@tipos_incidente_ns.route("/<int:id>")
@tipos_incidente_ns.response(404, "Tipo de incidente no encontrado")
@tipos_incidente_ns.param("id", "ID del tipo de incidente")
class TipoIncidenteDetail(Resource):
    @tipos_incidente_ns.marshal_with(tipo_incidente_model)
    def get(self, id):
        """Obtener un tipo de incidente por ID"""
        tipo_incidente = TipoIncidente.get_by_id(id)
        if not tipo_incidente:
            tipos_incidente_ns.abort(
                404, f"Tipo de incidente con ID {id} no encontrado"
            )
        return tipo_incidente

    @tipos_incidente_ns.expect(tipo_incidente_model)
    @tipos_incidente_ns.marshal_with(tipo_incidente_model)
    def put(self, id):
        """Actualizar un tipo de incidente"""
        tipo_incidente = TipoIncidente.get_by_id(id)
        if not tipo_incidente:
            tipos_incidente_ns.abort(
                404, f"Tipo de incidente con ID {id} no encontrado"
            )

        data = request.get_json()

        # Validar nombre único si se está cambiando
        if "nombre" in data and data["nombre"] != tipo_incidente.nombre:
            if TipoIncidente.query.filter_by(nombre=data["nombre"]).first():
                tipos_incidente_ns.abort(
                    400,
                    f"Ya existe un tipo de incidente con el nombre: {data['nombre']}",
                )

        tipo_incidente.nombre = data.get("nombre", tipo_incidente.nombre)
        tipo_incidente.descripcion = data.get("descripcion", tipo_incidente.descripcion)
        tipo_incidente.categoria = data.get("categoria", tipo_incidente.categoria)

        db.session.commit()
        return tipo_incidente

    @tipos_incidente_ns.response(204, "Tipo de incidente eliminado")
    def delete(self, id):
        """Eliminar (desactivar) un tipo de incidente"""
        tipo_incidente = TipoIncidente.get_by_id(id)
        if not tipo_incidente:
            tipos_incidente_ns.abort(
                404, f"Tipo de incidente con ID {id} no encontrado"
            )

        tipo_incidente.estado = "inactivo"
        db.session.commit()

        return "", 204
