from flask import request
from flask_restx import Namespace, Resource, fields
from ..models.proveedor_servicio import ProveedorServicio
from ..extensions import db

proveedores_ns = Namespace(
    "proveedores", description="Operaciones relacionadas con proveedores de servicio"
)

proveedor_model = proveedores_ns.model(
    "ProveedorServicio",
    {
        "id": fields.Integer(readOnly=True, description="ID del proveedor"),
        "nombre": fields.String(required=True, description="Nombre del proveedor"),
        "telefono": fields.String(description="Teléfono del proveedor"),
        "email": fields.String(description="Email del proveedor"),
        "direccion": fields.String(description="Dirección del proveedor"),
        "estado": fields.String(description="Estado del proveedor"),
    },
)


@proveedores_ns.route("/")
class ProveedorList(Resource):
    @proveedores_ns.marshal_list_with(proveedor_model)
    def get(self):
        """Listar todos los proveedores activos"""
        return ProveedorServicio.get_all()

    @proveedores_ns.expect(proveedor_model)
    @proveedores_ns.marshal_with(proveedor_model, code=201)
    def post(self):
        """Crear un nuevo proveedor"""
        data = request.get_json()

        proveedor = ProveedorServicio(
            nombre=data["nombre"],
            telefono=data.get("telefono"),
            email=data.get("email"),
            direccion=data.get("direccion"),
        )

        db.session.add(proveedor)
        db.session.commit()

        return proveedor, 201


@proveedores_ns.route("/<int:id>")
@proveedores_ns.response(404, "Proveedor no encontrado")
@proveedores_ns.param("id", "ID del proveedor")
class ProveedorDetail(Resource):
    @proveedores_ns.marshal_with(proveedor_model)
    def get(self, id):
        """Obtener un proveedor por ID"""
        proveedor = ProveedorServicio.get_by_id(id)
        if not proveedor:
            proveedores_ns.abort(404, f"Proveedor con ID {id} no encontrado")
        return proveedor

    @proveedores_ns.expect(proveedor_model)
    @proveedores_ns.marshal_with(proveedor_model)
    def put(self, id):
        """Actualizar un proveedor"""
        proveedor = ProveedorServicio.get_by_id(id)
        if not proveedor:
            proveedores_ns.abort(404, f"Proveedor con ID {id} no encontrado")

        data = request.get_json()

        proveedor.nombre = data.get("nombre", proveedor.nombre)
        proveedor.telefono = data.get("telefono", proveedor.telefono)
        proveedor.email = data.get("email", proveedor.email)
        proveedor.direccion = data.get("direccion", proveedor.direccion)

        db.session.commit()
        return proveedor

    @proveedores_ns.response(204, "Proveedor eliminado")
    def delete(self, id):
        """Eliminar (desactivar) un proveedor"""
        proveedor = ProveedorServicio.get_by_id(id)
        if not proveedor:
            proveedores_ns.abort(404, f"Proveedor con ID {id} no encontrado")

        proveedor.estado = "inactivo"
        db.session.commit()

        return "", 204
