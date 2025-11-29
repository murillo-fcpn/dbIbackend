from flask import request
from flask_restx import Namespace, Resource, fields
from ..models.tipo_transporte import TipoTransporte
from ..extensions import db

tipos_transporte_ns = Namespace(
    "tipos-transporte", description="Operaciones relacionadas con tipos de transporte"
)

tipo_transporte_model = tipos_transporte_ns.model(
    "TipoTransporte",
    {
        "id": fields.Integer(readOnly=True, description="ID del tipo de transporte"),
        "nombre": fields.String(
            required=True, description="Nombre del tipo de transporte"
        ),
        "descripcion": fields.String(description="Descripción del tipo de transporte"),
        "empresa_operadora": fields.String(description="Empresa operadora"),
        "estado": fields.String(description="Estado del tipo de transporte"),
    },
)


@tipos_transporte_ns.route("/")
class TipoTransporteList(Resource):
    @tipos_transporte_ns.marshal_list_with(tipo_transporte_model)
    def get(self):
        """Listar todos los tipos de transporte activos"""
        return TipoTransporte.get_all()

    @tipos_transporte_ns.expect(tipo_transporte_model)
    @tipos_transporte_ns.marshal_with(tipo_transporte_model, code=201)
    def post(self):
        """Crear un nuevo tipo de transporte"""
        data = request.get_json()

        # Validar nombre único
        if TipoTransporte.query.filter_by(nombre=data["nombre"]).first():
            tipos_transporte_ns.abort(
                400, f"Ya existe un tipo de transporte con el nombre: {data['nombre']}"
            )

        tipo_transporte = TipoTransporte(
            nombre=data["nombre"],
            descripcion=data.get("descripcion"),
            empresa_operadora=data.get("empresa_operadora"),
        )

        db.session.add(tipo_transporte)
        db.session.commit()

        return tipo_transporte, 201


@tipos_transporte_ns.route("/<int:id>")
@tipos_transporte_ns.response(404, "Tipo de transporte no encontrado")
@tipos_transporte_ns.param("id", "ID del tipo de transporte")
class TipoTransporteDetail(Resource):
    @tipos_transporte_ns.marshal_with(tipo_transporte_model)
    def get(self, id):
        """Obtener un tipo de transporte por ID"""
        tipo_transporte = TipoTransporte.get_by_id(id)
        if not tipo_transporte:
            tipos_transporte_ns.abort(
                404, f"Tipo de transporte con ID {id} no encontrado"
            )
        return tipo_transporte

    @tipos_transporte_ns.expect(tipo_transporte_model)
    @tipos_transporte_ns.marshal_with(tipo_transporte_model)
    def put(self, id):
        """Actualizar un tipo de transporte"""
        tipo_transporte = TipoTransporte.get_by_id(id)
        if not tipo_transporte:
            tipos_transporte_ns.abort(
                404, f"Tipo de transporte con ID {id} no encontrado"
            )

        data = request.get_json()

        # Validar nombre único si se está cambiando
        if "nombre" in data and data["nombre"] != tipo_transporte.nombre:
            if TipoTransporte.query.filter_by(nombre=data["nombre"]).first():
                tipos_transporte_ns.abort(
                    400,
                    f"Ya existe un tipo de transporte con el nombre: {data['nombre']}",
                )

        tipo_transporte.nombre = data.get("nombre", tipo_transporte.nombre)
        tipo_transporte.descripcion = data.get(
            "descripcion", tipo_transporte.descripcion
        )
        tipo_transporte.empresa_operadora = data.get(
            "empresa_operadora", tipo_transporte.empresa_operadora
        )

        db.session.commit()
        return tipo_transporte

    @tipos_transporte_ns.response(204, "Tipo de transporte eliminado")
    def delete(self, id):
        """Eliminar (desactivar) un tipo de transporte"""
        tipo_transporte = TipoTransporte.get_by_id(id)
        if not tipo_transporte:
            tipos_transporte_ns.abort(
                404, f"Tipo de transporte con ID {id} no encontrado"
            )

        tipo_transporte.estado = "inactivo"
        db.session.commit()

        return "", 204
