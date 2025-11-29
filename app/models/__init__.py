# Importar todos los modelos para que Flask-Migrate los detecte
from .servicio import Servicio
from .proveedor_servicio import ProveedorServicio
from .medidor import Medidor
from .lectura_servicio import LecturaServicio
from .tipo_reclamo import TipoReclamo
from .estado_reclamo import EstadoReclamo
from .reclamo import Reclamo
from .corte_programado import CorteProgramado


from .tipo_transporte import TipoTransporte
from .tipo_incidente import TipoIncidente
from .operador import Operador
from .conductor import Conductor
from .vehiculo import Vehiculo
from .ruta import Ruta
from .parada import Parada
from .horario import Horario
from .trayecto import Trayecto
from .incidente_transito import IncidenteTransito
