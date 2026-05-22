
from pathlib import Path

from pyswip import Prolog


# Referencias a frames — se asignan desde main.py
frame_activo = None
frame_menu = None
frame_juego = None


archivo_logica = Path(__file__).resolve().parent / "logica.pl"


def obtener_prolog():
    prolog = Prolog()
    prolog.consult(str(archivo_logica).replace("\\", "/"))
    return prolog


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


# ==========================
# Stubs de acciones (no implementadas)
# ==========================

def tomar(artefacto):
    pass


def usar(artefacto):
    pass


def reparar(sistema):
    pass


def rescatar(tripulante):
    pass


def puedo_ir(destino):
    pass


def mover(modulo):
    pass


def donde_esta(artefacto):
    pass


def que_tengo():
    pass


def modulos_visitados():
    pass


def ruta(inicio, fin):
    pass


def como_gano():
    pass


__all__ = [
    "mostrar_frame",
    "ir_a_menu",
    "ir_a_jugar",
    "obtener_estado_jugador",
]
