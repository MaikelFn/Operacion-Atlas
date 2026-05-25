
from pathlib import Path

from pyswip import Prolog


# Referencias a frames — se asignan desde main.py
frame_activo = None
frame_menu = None
frame_juego = None
frame_mover = None
frame_tomar = None
frame_usar = None
frame_donde = None
frame_inventario = None
frame_rescatar = None
frame_visitados = None


archivo_logica = Path(__file__).resolve().parent / "logica.pl"
_prolog = Prolog()
_prolog.consult(str(archivo_logica).replace("\\", "/"))


def obtener_prolog():
    return _prolog


def consultar_uno(query):
    return next(obtener_prolog().query(query), None)

def consultar_todos(query):
    return list(obtener_prolog().query(query))


def lista_a_texto(valor):
    if valor is None:
        return []
    if isinstance(valor, list):
        return [str(elemento) for elemento in valor]
    return [str(valor)]


def obtener_estado_jugador():
    """Consulta a Prolog el estado relevante del jugador para pintar la UI."""
    jugador = consultar_uno("jugador(Modulo)") or {}
    ubicacion = str(jugador.get("Modulo") or "") or "desconocido"

    descripcion = consultar_uno(f"modulo({ubicacion}, Descripcion)") or {}
    descripcion_modulo = str(descripcion.get("Descripcion") or "") or "Sin descripcion disponible."

    artefactos = consultar_uno("que_tengo(Lista)") or {}
    artefactos_tenidos = lista_a_texto(artefactos.get("Lista"))

    usados = consultar_uno("usados(Lista)") or {}
    artefactos_usados = lista_a_texto(usados.get("Lista"))

    sistemas_en_falla = []
    for resultado in consultar_todos("sistema(Modulo, Sistema, Artefactos, fallo)"):
        sistemas_en_falla.append({
            "modulo": str(resultado.get("Modulo") or ""),
            "sistema": str(resultado.get("Sistema") or ""),
            "artefactos": lista_a_texto(resultado.get("Artefactos")),
        })

    tripulantes_atrapados = []
    for resultado in consultar_todos("tripulante(Tripulante, Modulo, Sistemas, atrapado)"):
        tripulantes_atrapados.append({
            "nombre": str(resultado.get("Tripulante") or ""),
            "modulo": str(resultado.get("Modulo") or ""),
            "sistemas_necesarios": lista_a_texto(resultado.get("Sistemas")),
        })

    return {
        "ubicacion": ubicacion,
        "descripcion_modulo": descripcion_modulo,
        "artefactos": artefactos_tenidos,
        "artefactos_usados": artefactos_usados,
        "sistemas_en_falla": sistemas_en_falla,
        "tripulantes_atrapados": tripulantes_atrapados,
    }


def mostrar_frame(frame):
    global frame_activo
    if frame_activo:
        try:
            frame_activo.place_forget()
        except Exception:
            pass
    try:
        frame.place(relx=0.5, rely=0.5, anchor="center")
    except Exception:
        pass
    frame_activo = frame


def ir_a_menu():
    if frame_menu:
        mostrar_frame(frame_menu)


def ir_a_jugar():
    if frame_juego:
        mostrar_frame(frame_juego)


def ir_a_mover():
    if frame_mover:
        mostrar_frame(frame_mover)


def ir_a_tomar():
    if frame_tomar:
        mostrar_frame(frame_tomar)


def ir_a_usar():
    if frame_usar:
        mostrar_frame(frame_usar)


def ir_a_donde():
    if frame_donde:
        mostrar_frame(frame_donde)


def ir_a_inventario():
    if frame_inventario:
        mostrar_frame(frame_inventario)


def ir_a_rescatar():
    if frame_rescatar:
        mostrar_frame(frame_rescatar)


def ir_a_visitados():
    if frame_visitados:
        mostrar_frame(frame_visitados)


# ==========================
# Stubs de acciones (no implementadas)
# ==========================

def tomar(artefacto):
    return consultar_uno(f"tomar({artefacto})") is not None


def usar(artefacto):
    return consultar_uno(f"usar({artefacto})") is not None


def inicializar_juego():
    return consultar_uno("inicializar_juego") is not None


def reparar(sistema):
    return consultar_uno(f"reparar({sistema})") is not None


def obtener_tripulantes_atrapados_modulo_actual():
    jugador = consultar_uno("jugador(Modulo)") or {}
    ubicacion = str(jugador.get("Modulo") or "")

    tripulantes = []
    for resultado in consultar_todos(f"tripulante(Tripulante, {ubicacion}, Sistemas, atrapado)"):
        tripulante = str(resultado.get("Tripulante") or "")
        if tripulante:
            tripulantes.append(tripulante)
    return tripulantes


def obtener_sistemas_requeridos_tripulante(tripulante):
    jugador = consultar_uno("jugador(Modulo)") or {}
    ubicacion = str(jugador.get("Modulo") or "")

    resultado = consultar_uno(f"tripulante({tripulante}, {ubicacion}, Sistemas, atrapado)") or {}
    return lista_a_texto(resultado.get("Sistemas"))


def obtener_sistemas_en_fallo():
    jugador = consultar_uno("jugador(Modulo)") or {}
    ubicacion = str(jugador.get("Modulo") or "")

    sistemas = []
    for resultado in consultar_todos(f"sistema({ubicacion}, Sistema, Artefactos, fallo)"):
        sistema = str(resultado.get("Sistema") or "")
        if sistema:
            sistemas.append(sistema)
    return sistemas


def obtener_artefactos_requeridos_sistema(sistema):
    jugador = consultar_uno("jugador(Modulo)") or {}
    ubicacion = str(jugador.get("Modulo") or "")

    resultado = consultar_uno(f"sistema({ubicacion},{sistema},Artefactos, fallo)") or {}
    return lista_a_texto(resultado.get("Artefactos"))


def rescatar(tripulante):
    return consultar_uno(f"rescatar({tripulante})") is not None


def puedo_ir(destino):
    return consultar_uno(f"puedo_ir({destino})") is not None


def mover(modulo):
    return consultar_uno(f"mover({modulo})") is not None


def obtener_destinos_disponibles():
    destinos = []
    for resultado in consultar_todos("modulo(Destino, _)"):
        destino = str(resultado.get("Destino") or "")
        if destino and puedo_ir(destino):
            destinos.append(destino)
    return destinos


def donde_esta(artefacto):
    resultado = consultar_uno(f"donde_esta({artefacto}, Modulo)") or {}
    return str(resultado.get("Modulo") or "")


def que_tengo():
    resultado = consultar_uno("que_tengo(Lista)") or {}
    return lista_a_texto(resultado.get("Lista"))


def usados():
    resultado = consultar_uno("usados(Lista)") or {}
    return lista_a_texto(resultado.get("Lista"))


def obtener_artefactos_usables():
    inventario = que_tengo()
    usados_actuales = set(usados())
    return [artefacto for artefacto in inventario if artefacto not in usados_actuales]


def obtener_artefactos_disponibles():
    jugador = consultar_uno("jugador(Modulo)") or {}
    ubicacion = str(jugador.get("Modulo") or "")

    logrados = set(que_tengo())
    artefactos = []
    for resultado in consultar_todos(f"artefacto(Artefacto, {ubicacion})"):
        artefacto = str(resultado.get("Artefacto") or "")
        if artefacto and artefacto not in logrados:
            artefactos.append(artefacto)
    return artefactos


def obtener_artefactos_faltantes():
    inventario = set(que_tengo())
    artefactos = []
    for resultado in consultar_todos("artefacto(Artefacto, Modulo)"):
        artefacto = str(resultado.get("Artefacto") or "")
        if artefacto and artefacto not in inventario:
            artefactos.append(artefacto)
    return artefactos


def obtener_inventario_artefactos():
    inventario = que_tengo()
    usados_actuales = set(usados())
    artefactos = []

    for artefacto in inventario:
        artefactos.append({
            "artefacto": artefacto,
            "usado": artefacto in usados_actuales,
            "modulo": donde_esta(artefacto),
        })

    return artefactos


def modulos_visitados():
    resultado = consultar_uno("modulos_visitados(Lista)") or {}
    return lista_a_texto(resultado.get("Lista"))


def ruta(inicio, fin):
    if not inicio or not fin:
        return []
    resultado = consultar_uno(f"ruta({inicio},{fin},Ruta)") or {}
    ruta_prolog = resultado.get("Ruta") if resultado else None
    return lista_a_texto(ruta_prolog)


def obtener_modulos():
    modulos = []
    for resultado in consultar_todos("modulo(Modulo, _)"):
        modulo = str(resultado.get("Modulo") or "")
        if modulo:
            modulos.append(modulo)
    return modulos


def obtener_descripcion_modulo(modulo):
    resultado = consultar_uno(f"modulo({modulo}, Descripcion)") or {}
    return str(resultado.get("Descripcion") or "")


def como_gano():
    pass


__all__ = [
    "mostrar_frame",
    "ir_a_menu",
    "ir_a_jugar",
    "ir_a_mover",
    "ir_a_tomar",
    "ir_a_usar",
    "ir_a_donde",
    "ir_a_inventario",
    "obtener_estado_jugador",
    "obtener_destinos_disponibles",
    "obtener_artefactos_disponibles",
    "obtener_artefactos_faltantes",
    "obtener_inventario_artefactos",
    "obtener_artefactos_usables",
    "puedo_ir",
    "mover",
    "tomar",
    "usar",
    "ruta",
    "obtener_modulos",
]
