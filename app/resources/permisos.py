from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.permiso import Permiso
from ..extensions import db

permisos_ns = Namespace("permisos", description="Operaciones relacionadas con permisos")

permiso_model = permisos_ns.model(
    "Permiso",
    {
        "id": fields.Integer(readonly=True),
        "nombre": fields.String(required=True),
        "descripcion": fields.String,
        "estado": fields.String,
    },
)


@permisos_ns.route("/")
class PermisoList(Resource):
    @permisos_ns.marshal_list_with(permiso_model)
    def get(self):
        """Obtener todos los permisos"""
        return Permiso.get_all()

    @permisos_ns.expect(permiso_model)
    @permisos_ns.marshal_with(permiso_model, code=201)
    def post(self):
        """Crear un nuevo permiso"""
        data = request.json
        nuevo_permiso = Permiso(
            nombre=data["nombre"], descripcion=data.get("descripcion")
        )
        nuevo_permiso.save()
        return nuevo_permiso, 201


@permisos_ns.route("/<int:id>")
@permisos_ns.response(404, "Permiso no encontrado")
class PermisoResource(Resource):
    @permisos_ns.marshal_with(permiso_model)
    def get(self, id):
        """Obtener un permiso por ID"""
        permiso = Permiso.get_by_id(id)
        if not permiso:
            permisos_ns.abort(404, "Permiso no encontrado")
        return permiso

    @permisos_ns.expect(permiso_model)
    @permisos_ns.marshal_with(permiso_model)
    def put(self, id):
        """Actualizar un permiso"""
        permiso = Permiso.get_by_id(id)
        if not permiso:
            permisos_ns.abort(404, "Permiso no encontrado")

        data = request.json
        permiso.nombre = data.get("nombre", permiso.nombre)
        permiso.descripcion = data.get("descripcion", permiso.descripcion)
        permiso.save()
        return permiso

    def delete(self, id):
        """Eliminar un permiso (soft delete)"""
        permiso = Permiso.get_by_id(id)
        if not permiso:
            permisos_ns.abort(404, "Permiso no encontrado")
        permiso.estado = "inactivo"
        permiso.save()
        return "", 204
