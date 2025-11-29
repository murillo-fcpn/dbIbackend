from flask import request
from flask_restx import Namespace, Resource, fields
from ..models.operador import Operador
from ..extensions import db

operadores_ns = Namespace(
    "operadores", description="Operaciones relacionadas con operadores"
)

operador_model = operadores_ns.model(
    "Operador",
    {
        "id": fields.Integer(readOnly=True, description="ID del operador"),
        "nombre": fields.String(required=True, description="Nombre del operador"),
        "telefono": fields.String(description="Teléfono del operador"),
        "email": fields.String(description="Email del operador"),
        "certificado_vigente": fields.Boolean(description="Certificado vigente"),
        "fecha_vencimiento_certificado": fields.String(
            description="Fecha de vencimiento del certificado"
        ),
        "estado": fields.String(description="Estado del operador"),
    },
)


@operadores_ns.route("/")
class OperadorList(Resource):
    @operadores_ns.marshal_list_with(operador_model)
    def get(self):
        """Listar todos los operadores activos"""
        return Operador.get_all()

    @operadores_ns.expect(operador_model)
    @operadores_ns.marshal_with(operador_model, code=201)
    def post(self):
        """Crear un nuevo operador"""
        data = request.get_json()

        operador = Operador(
            nombre=data["nombre"],
            telefono=data.get("telefono"),
            email=data.get("email"),
            certificado_vigente=data.get("certificado_vigente", True),
            fecha_vencimiento_certificado=data.get("fecha_vencimiento_certificado"),
        )

        db.session.add(operador)
        db.session.commit()

        return operador, 201


@operadores_ns.route("/<int:id>")
@operadores_ns.response(404, "Operador no encontrado")
@operadores_ns.param("id", "ID del operador")
class OperadorDetail(Resource):
    @operadores_ns.marshal_with(operador_model)
    def get(self, id):
        """Obtener un operador por ID"""
        operador = Operador.get_by_id(id)
        if not operador:
            operadores_ns.abort(404, f"Operador con ID {id} no encontrado")
        return operador

    @operadores_ns.expect(operador_model)
    @operadores_ns.marshal_with(operador_model)
    def put(self, id):
        """Actualizar un operador"""
        operador = Operador.get_by_id(id)
        if not operador:
            operadores_ns.abort(404, f"Operador con ID {id} no encontrado")

        data = request.get_json()

        operador.nombre = data.get("nombre", operador.nombre)
        operador.telefono = data.get("telefono", operador.telefono)
        operador.email = data.get("email", operador.email)
        operador.certificado_vigente = data.get(
            "certificado_vigente", operador.certificado_vigente
        )
        operador.fecha_vencimiento_certificado = data.get(
            "fecha_vencimiento_certificado", operador.fecha_vencimiento_certificado
        )

        db.session.commit()
        return operador

    @operadores_ns.response(204, "Operador eliminado")
    def delete(self, id):
        """Eliminar (desactivar) un operador"""
        operador = Operador.get_by_id(id)
        if not operador:
            operadores_ns.abort(404, f"Operador con ID {id} no encontrado")

        operador.estado = "inactivo"
        db.session.commit()

        return "", 204
