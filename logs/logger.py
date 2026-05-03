# Importación de módulos necesarios
import logging  # Para registrar eventos del sistema
from datetime import datetime  # Para manejar fechas y horas
import os  # Para crear carpetas y manejar archivos


def configurar_logger():
    """Configura el sistema de logging"""
    # Crea la carpeta logs si no existe
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # Nombre del archivo con fecha actual: sistema_20260101.log
    log_filename = f"logs/sistema_{datetime.now().strftime('%Y%m%d')}.log"

    # Configuración principal del logging
    logging.basicConfig(
        level=logging.INFO,  # Solo guarda mensajes INFO o más importantes
        format="%(asctime)s - %(levelname)s - %(message)s",  # Formato: fecha - nivel - mensaje
        handlers=[
            # Guarda los logs en archivo
            logging.FileHandler(log_filename, encoding="utf-8"),
            # Muestra los logs en consola
            logging.StreamHandler(),
        ],
    )
    return logging.getLogger(__name__)


def registrar_log(mensaje, nivel="info"):
    """Registra un mensaje en el log"""
    logger = logging.getLogger(__name__)

    # Según el nivel, usa el método correspondiente
    if nivel == "error":
        logger.error(mensaje)  # Para errores graves
    elif nivel == "warning":
        logger.warning(mensaje)  # Para advertencias
    else:
        logger.info(mensaje)  # Para información general
