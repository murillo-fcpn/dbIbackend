from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.zona import Zona
from ..extensions import db

zonas_ns = Namespace("zonas", description="Operaciones relacionadas con zonas")

zona_model = zonas_ns.model(
    "Zona",
    {
        "id": fields.Integer(readonly=True),
        "nombre": fields.String(required=True),
        "poligono_geojson": fields.Raw(required=False),
        "descripcion": fields.String,
        "tipo": fields.String,
        "estado": fields.String,
    },
)


@zonas_ns.route("/")
class ZonaList(Resource):
    @zonas_ns.marshal_list_with(zona_model)
    def get(self):
        """Obtener todas las zonas"""
        return Zona.get_all()

    @zonas_ns.expect(zona_model)
    @zonas_ns.marshal_with(zona_model, code=201)
    def post(self):
        """Crear una nueva zona"""
        data = request.json
        nueva_zona = Zona(
            nombre=data["nombre"],
            poligono_geojson=data.get("poligono_geojson"),
            descripcion=data.get("descripcion"),
            tipo=data.get("tipo"),
        )
        nueva_zona.save()
        return nueva_zona, 201


@zonas_ns.route("/<int:id>")
@zonas_ns.response(404, "Zona no encontrada")
class ZonaResource(Resource):
    @zonas_ns.marshal_with(zona_model)
    def get(self, id):
        """Obtener una zona por ID"""
        zona = Zona.get_by_id(id)
        if not zona:
            zonas_ns.abort(404, "Zona no encontrada")
        return zona

    @zonas_ns.expect(zona_model)
    @zonas_ns.marshal_with(zona_model)
    def put(self, id):
        """Actualizar una zona"""
        zona = Zona.get_by_id(id)
        if not zona:
            zonas_ns.abort(404, "Zona no encontrada")

        data = request.json
        zona.nombre = data.get("nombre", zona.nombre)
        zona.poligono_geojson = data.get("poligono_geojson", zona.poligono_geojson)
        zona.descripcion = data.get("descripcion", zona.descripcion)
        zona.tipo = data.get("tipo", zona.tipo)
        zona.save()
        return zona

    def delete(self, id):
        """Eliminar una zona (soft delete)"""
        zona = Zona.get_by_id(id)
        if not zona:
            zonas_ns.abort(404, "Zona no encontrada")
        zona.estado = "inactivo"
        zona.save()
        return "", 204
