from flask import request
from flask_restx import Namespace, Resource, fields
from ..models.ruta import Ruta
from ..extensions import db

rutas_ns = Namespace("rutas", description="Operaciones relacionadas con rutas")

ruta_model = rutas_ns.model(
    "Ruta",
    {
        "id": fields.Integer(readOnly=True, description="ID de la ruta"),
        "nombre": fields.String(required=True, description="Nombre de la ruta"),
        "distancia_km": fields.Float(description="Distancia en kilómetros"),
        "tiempo_estimado_min": fields.Integer(description="Tiempo estimado en minutos"),
        "color_mapa": fields.String(description="Color en el mapa (hex)"),
        "id_tipo_transporte": fields.Integer(
            required=True, description="ID del tipo de transporte"
        ),
        "estado": fields.String(description="Estado de la ruta"),
    },
)


@rutas_ns.route("/")
class RutaList(Resource):
    @rutas_ns.marshal_list_with(ruta_model)
    def get(self):
        """Listar todas las rutas activas"""
        return Ruta.get_all()

    @rutas_ns.expect(ruta_model)
    @rutas_ns.marshal_with(ruta_model, code=201)
    def post(self):
        """Crear una nueva ruta"""
        data = request.get_json()

        # Validar nombre único
        if Ruta.query.filter_by(nombre=data["nombre"]).first():
            rutas_ns.abort(400, f"Ya existe una ruta con el nombre: {data['nombre']}")

        ruta = Ruta(
            nombre=data["nombre"],
            distancia_km=data.get("distancia_km"),
            tiempo_estimado_min=data.get("tiempo_estimado_min"),
            color_mapa=data.get("color_mapa"),
            id_tipo_transporte=data["id_tipo_transporte"],
        )

        db.session.add(ruta)
        db.session.commit()

        return ruta, 201


@rutas_ns.route("/<int:id>")
@rutas_ns.response(404, "Ruta no encontrada")
@rutas_ns.param("id", "ID de la ruta")
class RutaDetail(Resource):
    @rutas_ns.marshal_with(ruta_model)
    def get(self, id):
        """Obtener una ruta por ID"""
        ruta = Ruta.get_by_id(id)
        if not ruta:
            rutas_ns.abort(404, f"Ruta con ID {id} no encontrada")
        return ruta

    @rutas_ns.expect(ruta_model)
    @rutas_ns.marshal_with(ruta_model)
    def put(self, id):
        """Actualizar una ruta"""
        ruta = Ruta.get_by_id(id)
        if not ruta:
            rutas_ns.abort(404, f"Ruta con ID {id} no encontrada")

        data = request.get_json()

        # Validar nombre único si se está cambiando
        if "nombre" in data and data["nombre"] != ruta.nombre:
            if Ruta.query.filter_by(nombre=data["nombre"]).first():
                rutas_ns.abort(
                    400, f"Ya existe una ruta con el nombre: {data['nombre']}"
                )

        ruta.nombre = data.get("nombre", ruta.nombre)
        ruta.distancia_km = data.get("distancia_km", ruta.distancia_km)
        ruta.tiempo_estimado_min = data.get(
            "tiempo_estimado_min", ruta.tiempo_estimado_min
        )
        ruta.color_mapa = data.get("color_mapa", ruta.color_mapa)
        ruta.id_tipo_transporte = data.get(
            "id_tipo_transporte", ruta.id_tipo_transporte
        )

        db.session.commit()
        return ruta

    @rutas_ns.response(204, "Ruta eliminada")
    def delete(self, id):
        """Eliminar (desactivar) una ruta"""
        ruta = Ruta.get_by_id(id)
        if not ruta:
            rutas_ns.abort(404, f"Ruta con ID {id} no encontrada")

        ruta.estado = "inactivo"
        db.session.commit()

        return "", 204
