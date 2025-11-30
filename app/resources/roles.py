from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.rol import Rol
from ..models.permiso import Permiso
from ..extensions import db

roles_ns = Namespace("roles", description="Operaciones relacionadas con roles")

rol_model = roles_ns.model(
    "Rol",
    {
        "id": fields.Integer(readonly=True),
        "nombre": fields.String(required=True),
        "descripcion": fields.String,
        "permisos": fields.List(fields.String),
        "estado": fields.String,
    },
)

rol_input_model = roles_ns.model(
    "RolInput",
    {
        "nombre": fields.String(required=True),
        "descripcion": fields.String,
        "permiso_ids": fields.List(fields.Integer),
    },
)


@roles_ns.route("/")
class RolList(Resource):
    @roles_ns.marshal_list_with(rol_model)
    def get(self):
        """Obtener todos los roles"""
        return Rol.get_all()

    @roles_ns.expect(rol_input_model)
    @roles_ns.marshal_with(rol_model, code=201)
    def post(self):
        """Crear un nuevo rol"""
        data = request.json
        nuevo_rol = Rol(nombre=data["nombre"], descripcion=data.get("descripcion"))

        # Asignar permisos si se proporcionan
        if data.get("permiso_ids"):
            permisos = Permiso.query.filter(
                Permiso.id.in_(data["permiso_ids"])
            ).all()
            nuevo_rol.permisos = permisos

        nuevo_rol.save()
        return nuevo_rol, 201


@roles_ns.route("/<int:id>")
@roles_ns.response(404, "Rol no encontrado")
class RolResource(Resource):
    @roles_ns.marshal_with(rol_model)
    def get(self, id):
        """Obtener un rol por ID"""
        rol = Rol.get_by_id(id)
        if not rol:
            roles_ns.abort(404, "Rol no encontrado")
        return rol

    @roles_ns.expect(rol_input_model)
    @roles_ns.marshal_with(rol_model)
    def put(self, id):
        """Actualizar un rol"""
        rol = Rol.get_by_id(id)
        if not rol:
            roles_ns.abort(404, "Rol no encontrado")

        data = request.json
        rol.nombre = data.get("nombre", rol.nombre)
        rol.descripcion = data.get("descripcion", rol.descripcion)

        # Actualizar permisos si se proporcionan
        if "permiso_ids" in data:
            permisos = Permiso.query.filter(
                Permiso.id.in_(data["permiso_ids"])
            ).all()
            rol.permisos = permisos

        rol.save()
        return rol

    def delete(self, id):
        """Eliminar un rol (soft delete)"""
        rol = Rol.get_by_id(id)
        if not rol:
            roles_ns.abort(404, "Rol no encontrado")
        rol.estado = "inactivo"
        rol.save()
        return "", 204
