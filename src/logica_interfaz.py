
# Referencias a frames — se asignan desde main.py
frame_activo = None
frame_menu = None
frame_juego = None


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
    "tomar",
    "usar",
    "reparar",
    "rescatar",
    "puedo_ir",
    "mover",
    "donde_esta",
    "que_tengo",
    "modulos_visitados",
    "ruta",
    "como_gano",
]
