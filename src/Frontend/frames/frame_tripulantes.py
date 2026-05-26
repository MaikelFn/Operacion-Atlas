"""
frame_tripulantes.py
Pantalla de rescate de tripulantes:
lista los tripulantes atrapados en el módulo actual,
muestra los sistemas necesarios para liberarlos
y permite ejecutar el rescate.
"""

import tkinter as tk
from tkinter import messagebox
import estilos as estilos
import logica_interfaz as logica_interfaz


_seleccion_tripulante_var  = None
_lista_tripulantes_frame   = None
_lista_sistemas_req_frame  = None


def construir(ventana, on_volver):
    """
    Construye el frame de rescate de tripulantes.

    :param ventana:   Ventana raíz de Tkinter.
    :param on_volver: Callback para regresar a la pantalla de juego.
    :returns: frame construido.
    """
    global _seleccion_tripulante_var, _lista_tripulantes_frame, _lista_sistemas_req_frame

    frame = tk.Frame(ventana, bg=estilos.COLOR_FONDO)
    frame.config(width=900, height=550)
    frame.pack_propagate(False)

    _seleccion_tripulante_var = tk.StringVar(value="")

    contenedor = tk.Frame(frame, bg=estilos.COLOR_FONDO)
    contenedor.pack(fill="both", expand=True, padx=18, pady=16)

    # Panel izquierdo: tripulantes atrapados en el modulo
    panel = tk.Frame(contenedor, bg=estilos.COLOR_FONDO, width=430)
    panel.pack(side="left", fill="both", expand=True, padx=(0, 14))
    panel.pack_propagate(False)

    tk.Label(
        panel, text="TRIPULANTES ATRAPADOS (MODULO ACTUAL)",
        **estilos.estilo_label(fg=estilos.COLOR_BOTON_TEXTO, font=("Courier", 18, "bold")),
    ).pack(anchor="w", pady=(0, 10))

    _lista_tripulantes_frame = tk.Frame(panel, bg=estilos.COLOR_FONDO)
    _lista_tripulantes_frame.pack(fill="both", expand=True)

    # Panel derecho: detalle y accion
    panel_det = tk.Frame(contenedor, bg=estilos.COLOR_FONDO, width=300)
    panel_det.pack(side="left", fill="y")
    panel_det.pack_propagate(False)

    tk.Label(
        panel_det, text="SELECCION",
        **estilos.estilo_label(fg=estilos.COLOR_AMARILLO, font=("Courier", 15, "bold")),
    ).pack(anchor="w", pady=(0, 12))

    tk.Entry(
        panel_det, textvariable=_seleccion_tripulante_var,
        state="readonly", width=26, font=("Courier", 13),
        bg=estilos.COLOR_BOTON_FONDO, fg=estilos.COLOR_TEXTO,
        relief="flat", readonlybackground=estilos.COLOR_BOTON_FONDO, justify="center",
    ).pack(anchor="w", pady=(0, 8))

    tk.Label(
        panel_det, text="Sistemas requeridos:",
        **estilos.estilo_label(fg=estilos.COLOR_TEXTO_OSCURO, font=("Courier", 11, "bold")),
    ).pack(anchor="w", pady=(8, 4))

    _lista_sistemas_req_frame = tk.Frame(panel_det, bg=estilos.COLOR_FONDO)
    _lista_sistemas_req_frame.pack(fill="both", expand=True)

    tk.Button(
        panel_det, text="RESCATAR", pady=12,
        command=lambda: _ejecutar_rescate(on_volver),
        **estilos.estilo_boton(color_fg=estilos.COLOR_VERDE),
    ).pack(anchor="w", pady=(0, 12))

    tk.Button(
        panel_det, text="VOLVER AL JUEGO", pady=12,
        command=on_volver,
        **estilos.estilo_boton(color_fg=estilos.COLOR_TEXTO_OSCURO),
    ).pack(anchor="w")

    return frame


def actualizar():
    """Recarga la lista de tripulantes atrapados en el módulo actual."""
    for w in _lista_tripulantes_frame.winfo_children():
        w.destroy()
    for w in _lista_sistemas_req_frame.winfo_children():
        w.destroy()
    _seleccion_tripulante_var.set("")

    tripulantes = logica_interfaz.obtener_tripulantes_atrapados_modulo_actual()
    if not tripulantes:
        tk.Label(
            _lista_tripulantes_frame,
            text="No hay tripulantes atrapados en este modulo.",
            **estilos.estilo_label(fg=estilos.COLOR_TEXTO_OSCURO, font=("Courier", 11, "italic")),
        ).pack(anchor="w", pady=6)
        return

    for tripulante in tripulantes:
        tk.Button(
            _lista_tripulantes_frame, text=tripulante, pady=10,
            command=lambda t=tripulante: _seleccionar_tripulante(t),
            **estilos.estilo_boton(color_fg=estilos.COLOR_AMARILLO),
        ).pack(anchor="w", pady=6)


def _seleccionar_tripulante(tripulante):
    _seleccion_tripulante_var.set(tripulante)

    for w in _lista_sistemas_req_frame.winfo_children():
        w.destroy()

    sistemas = logica_interfaz.obtener_sistemas_requeridos_tripulante(tripulante)
    if not sistemas:
        tk.Label(
            _lista_sistemas_req_frame,
            text="No hay sistemas listados para este tripulante.",
            **estilos.estilo_label(fg=estilos.COLOR_TEXTO_OSCURO, font=("Courier", 11, "italic")),
        ).pack(anchor="w", pady=6)
        return

    for sistema in sistemas:
        tk.Label(
            _lista_sistemas_req_frame, text=sistema,
            **estilos.estilo_label(fg=estilos.COLOR_VERDE, font=("Courier", 12, "bold")),
        ).pack(anchor="w", pady=6)


def _ejecutar_rescate(on_volver):
    tripulante = _seleccion_tripulante_var.get().strip()
    if not tripulante:
        messagebox.showwarning("Rescatar", "Selecciona primero un tripulante.")
        return

    if logica_interfaz.rescatar(tripulante):
        messagebox.showinfo("Rescatar", f"Tripulante {tripulante} rescatado con éxito.")
        on_volver()
    else:
        messagebox.showerror(
            "Rescatar",
            f"No se pudo rescatar {tripulante}. Asegurate de cumplir los sistemas requeridos."
        )
