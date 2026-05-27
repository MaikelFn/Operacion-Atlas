

import tkinter as tk
import estilos as estilos


_frame_contenedor = None
_boton_volver = None
_callback_volver = None


def construir(ventana, on_volver=None):


    global _frame_contenedor
    global _callback_volver
    global _boton_volver

    _callback_volver = on_volver

    # Frame principal
    _frame_contenedor = tk.Frame(
        ventana,
        bg=estilos.COLOR_FONDO
    )
    _frame_contenedor.config(width=900, height=550)
    _frame_contenedor.pack_propagate(False)

    # Panel central
    panel = tk.Frame(_frame_contenedor, bg=estilos.COLOR_FONDO)
    panel.pack(fill="both", expand=True, padx=50, pady=50)

    # Título
    tk.Label(
        panel,
        text="CÓMO GANO",
        bg=estilos.COLOR_FONDO,
        fg=estilos.COLOR_BOTON_TEXTO,
        font=("Courier", 24, "bold")
    ).pack(pady=(0, 30))

    # Mensaje
    tk.Label(
        panel,
        text="Funcionalidad en desarrollo",
        bg=estilos.COLOR_FONDO,
        fg=estilos.COLOR_TEXTO,
        font=("Courier", 14)
    ).pack(pady=20)

    # Botón de volver
    _boton_volver = tk.Button(
        panel,
        text="Volver al Juego",
        pady=12,
        command=lambda: _volver(),
        **estilos.estilo_boton(
            color_fg=estilos.COLOR_TEXTO_OSCURO
        )
    )
    _boton_volver.pack(pady=(50, 0))

    return _frame_contenedor


def _volver():
    """Ejecuta el callback de volver."""
    if _callback_volver:
        _callback_volver()
