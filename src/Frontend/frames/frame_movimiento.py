"""
frame_movimiento.py
Pantalla de movimiento: lista los destinos disponibles desde la
ubicación actual y permite al jugador desplazarse a uno de ellos.
"""

import tkinter as tk
from tkinter import messagebox
import estilos as estilos
import logica_interfaz as logica_interfaz


# Variables de estado de esta pantalla
_seleccion_destino_var = None
_origen_movimiento_var = None
_lista_destinos_frame  = None


def construir(ventana, on_volver):
    """
    Construye el frame de movimiento.

    :param ventana:   Ventana raíz (necesaria para crear StringVars).
    :param on_volver: Callback para regresar a la pantalla de juego.
    :returns: frame construido.
    """
    global _seleccion_destino_var, _origen_movimiento_var, _lista_destinos_frame

    frame = tk.Frame(ventana, bg=estilos.COLOR_FONDO)
    frame.config(width=900, height=550)
    frame.pack_propagate(False)

    _seleccion_destino_var = tk.StringVar(value="")
    _origen_movimiento_var = tk.StringVar(value="")

    contenedor = tk.Frame(frame, bg=estilos.COLOR_FONDO)
    contenedor.pack(fill="both", expand=True, padx=18, pady=16)

    # Panel izquierdo: lista de destinos
    panel_destinos = tk.Frame(contenedor, bg=estilos.COLOR_FONDO, width=430)
    panel_destinos.pack(side="left", fill="both", expand=True, padx=(0, 14))
    panel_destinos.pack_propagate(False)

    tk.Label(
        panel_destinos, text="DESTINOS DISPONIBLES",
        **estilos.estilo_label(fg=estilos.COLOR_BOTON_TEXTO, font=("Courier", 18, "bold")),
    ).pack(anchor="w", pady=(0, 10))

    tk.Label(
        panel_destinos,
        textvariable=_origen_movimiento_var,
        **estilos.estilo_label(fg=estilos.COLOR_TEXTO_OSCURO, font=("Courier", 11, "bold")),
    ).pack(anchor="w", pady=(0, 10))

    _lista_destinos_frame = tk.Frame(panel_destinos, bg=estilos.COLOR_FONDO)
    _lista_destinos_frame.pack(fill="both", expand=True)

    # Panel derecho: confirmacion y accion
    panel_confirmacion = tk.Frame(contenedor, bg=estilos.COLOR_FONDO, width=300)
    panel_confirmacion.pack(side="left", fill="y")
    panel_confirmacion.pack_propagate(False)

    tk.Label(
        panel_confirmacion, text="SELECCION",
        **estilos.estilo_label(fg=estilos.COLOR_AMARILLO, font=("Courier", 15, "bold")),
    ).pack(anchor="w", pady=(0, 12))

    tk.Entry(
        panel_confirmacion,
        textvariable=_seleccion_destino_var,
        state="readonly", width=26,
        font=("Courier", 13),
        bg=estilos.COLOR_BOTON_FONDO, fg=estilos.COLOR_TEXTO,
        relief="flat", readonlybackground=estilos.COLOR_BOTON_FONDO,
        justify="center",
    ).pack(anchor="w", pady=(0, 16))

    tk.Button(
        panel_confirmacion, text="IR", pady=12,
        command=_ejecutar_movimiento,
        **estilos.estilo_boton(color_fg=estilos.COLOR_VERDE),
    ).pack(anchor="w", pady=(0, 12))

    tk.Button(
        panel_confirmacion, text="VOLVER AL JUEGO", pady=12,
        command=on_volver,
        **estilos.estilo_boton(color_fg=estilos.COLOR_TEXTO_OSCURO),
    ).pack(anchor="w")

    return frame


def actualizar(on_volver_callback=None):
    """Recarga la lista de destinos disponibles desde la posición actual del jugador."""
    global _on_volver
    if on_volver_callback:
        _on_volver = on_volver_callback

    for widget in _lista_destinos_frame.winfo_children():
        widget.destroy()
    _seleccion_destino_var.set("")

    estado = logica_interfaz.obtener_estado_jugador()
    _origen_movimiento_var.set(f"Desde: {estado['ubicacion']}")

    destinos = logica_interfaz.obtener_destinos_disponibles()
    if not destinos:
        tk.Label(
            _lista_destinos_frame,
            text="No hay destinos disponibles.",
            **estilos.estilo_label(fg=estilos.COLOR_TEXTO_OSCURO, font=("Courier", 11, "italic")),
        ).pack(anchor="w", pady=6)
        return

    for destino in destinos:
        tk.Button(
            _lista_destinos_frame,
            text=destino, pady=10,
            command=lambda d=destino: _seleccion_destino_var.set(d),
            **estilos.estilo_boton(color_fg=estilos.COLOR_AZUL),
        ).pack(anchor="w", pady=6)


_on_volver = None


def _ejecutar_movimiento():
    destino = _seleccion_destino_var.get().strip()
    if not destino:
        messagebox.showwarning("Movimiento", "Primero selecciona un destino.")
        return

    if not logica_interfaz.puedo_ir(destino):
        messagebox.showerror("Movimiento", f"No puedes ir a {destino} desde la ubicacion actual.")
        actualizar()
        return

    if logica_interfaz.mover(destino):
        messagebox.showinfo("Movimiento", f"Te moviste a {destino}.")
        if _on_volver:
            _on_volver()
    else:
        messagebox.showerror("Movimiento", f"No se pudo mover a {destino}.")
