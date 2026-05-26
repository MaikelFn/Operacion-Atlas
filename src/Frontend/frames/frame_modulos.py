"""
frame_modulos.py
Agrupa las dos pantallas relacionadas con módulos y navegación:
  - Visitados: historial de módulos recorridos con descripción.
  - Ruta:      cálculo de camino entre dos módulos cualesquiera.
"""

import tkinter as tk
from tkinter import messagebox, ttk
import estilos as estilos
import logica_interfaz as logica_interfaz


# ──────────────────────────────────────────────
# MÓDULOS VISITADOS
# ──────────────────────────────────────────────

_vis_seleccion_var   = None
_vis_descripcion_var = None
_vis_lista_frame     = None


def construir_visitados(ventana, on_volver):
    """
    Construye el frame de módulos visitados.

    :param ventana:   Ventana raíz de Tkinter.
    :param on_volver: Callback para regresar a la pantalla de juego.
    :returns: frame construido.
    """
    global _vis_seleccion_var, _vis_descripcion_var, _vis_lista_frame

    frame = tk.Frame(ventana, bg=estilos.COLOR_FONDO)
    frame.config(width=900, height=550)
    frame.pack_propagate(False)

    _vis_seleccion_var   = tk.StringVar(value="")
    _vis_descripcion_var = tk.StringVar(value="")

    contenedor = tk.Frame(frame, bg=estilos.COLOR_FONDO)
    contenedor.pack(fill="both", expand=True, padx=18, pady=16)

    # Panel izquierdo: lista de modulos visitados
    panel = tk.Frame(contenedor, bg=estilos.COLOR_FONDO, width=430)
    panel.pack(side="left", fill="both", expand=True, padx=(0, 14))
    panel.pack_propagate(False)

    tk.Label(
        panel, text="MODULOS VISITADOS",
        **estilos.estilo_label(fg=estilos.COLOR_BOTON_TEXTO, font=("Courier", 18, "bold")),
    ).pack(anchor="w", pady=(0, 10))

    _vis_lista_frame = tk.Frame(panel, bg=estilos.COLOR_FONDO)
    _vis_lista_frame.pack(fill="both", expand=True)

    # Panel derecho: detalle del modulo seleccionado
    panel_det = tk.Frame(contenedor, bg=estilos.COLOR_FONDO, width=300)
    panel_det.pack(side="left", fill="y")
    panel_det.pack_propagate(False)

    tk.Label(
        panel_det, textvariable=_vis_seleccion_var,
        wraplength=260, justify="left",
        **estilos.estilo_label(fg=estilos.COLOR_AMARILLO, font=("Courier", 15, "bold")),
    ).pack(anchor="w", pady=(0, 10))

    tk.Label(
        panel_det, text="Descripcion del modulo:",
        **estilos.estilo_label(fg=estilos.COLOR_TEXTO_OSCURO, font=("Courier", 11, "bold")),
    ).pack(anchor="w", pady=(0, 4))

    tk.Label(
        panel_det, textvariable=_vis_descripcion_var,
        wraplength=260, justify="left",
        **estilos.estilo_label(fg=estilos.COLOR_TEXTO, font=("Courier", 12, "bold")),
    ).pack(anchor="w", pady=(0, 16))

    tk.Button(
        panel_det, text="VOLVER AL JUEGO", pady=12,
        command=on_volver,
        **estilos.estilo_boton(color_fg=estilos.COLOR_TEXTO_OSCURO),
    ).pack(anchor="w")

    return frame


def actualizar_visitados():
    """Recarga la lista de módulos visitados."""
    for w in _vis_lista_frame.winfo_children():
        w.destroy()
    _vis_seleccion_var.set("")
    _vis_descripcion_var.set("")

    visitados = logica_interfaz.modulos_visitados()
    if not visitados:
        tk.Label(
            _vis_lista_frame,
            text="No hay modulos visitados registrados.",
            **estilos.estilo_label(fg=estilos.COLOR_TEXTO_OSCURO, font=("Courier", 11, "italic")),
        ).pack(anchor="w", pady=6)
        return

    for modulo in visitados:
        tk.Button(
            _vis_lista_frame, text=modulo, pady=10,
            command=lambda m=modulo: _seleccionar_visitado(m),
            **estilos.estilo_boton(color_fg=estilos.COLOR_AZUL),
        ).pack(anchor="w", pady=6)


def _seleccionar_visitado(modulo):
    _vis_seleccion_var.set(modulo)
    _vis_descripcion_var.set(logica_interfaz.obtener_descripcion_modulo(modulo))


# ──────────────────────────────────────────────
# BUSCAR RUTA ENTRE MÓDULOS
# ──────────────────────────────────────────────

_cb_inicio    = None
_cb_destino   = None
_resultado_txt = None


def construir_ruta(ventana, on_volver):
    """
    Construye el frame de cálculo de ruta entre módulos.

    :param ventana:   Ventana raíz de Tkinter.
    :param on_volver: Callback para regresar a la pantalla de juego.
    :returns: frame construido.
    """
    global _cb_inicio, _cb_destino, _resultado_txt

    frame = tk.Frame(ventana, bg=estilos.COLOR_FONDO)
    frame.config(width=900, height=550)
    frame.pack_propagate(False)

    contenedor = tk.Frame(frame, bg=estilos.COLOR_FONDO)
    contenedor.pack(fill="both", expand=True, padx=18, pady=16)

    # Panel izquierdo: titulo
    panel_left = tk.Frame(contenedor, bg=estilos.COLOR_FONDO, width=430)
    panel_left.pack(side="left", fill="both", expand=True, padx=(0, 14))
    panel_left.pack_propagate(False)

    tk.Label(
        panel_left, text="VER RUTA",
        **estilos.estilo_label(fg=estilos.COLOR_BOTON_TEXTO, font=("Courier", 18, "bold")),
    ).pack(anchor="w", pady=(0, 10))

    # Panel derecho: controles y resultado
    panel_right = tk.Frame(contenedor, bg=estilos.COLOR_FONDO, width=300)
    panel_right.pack(side="left", fill="y")
    panel_right.pack_propagate(False)

    tk.Label(panel_right, text="Inicio",
             **estilos.estilo_label(fg=estilos.COLOR_TEXTO_OSCURO)).pack(anchor="w", pady=(6, 2))
    _cb_inicio = ttk.Combobox(panel_right, values=logica_interfaz.obtener_modulos(), state="readonly")
    _cb_inicio.pack(anchor="w", pady=(0, 8))

    tk.Label(panel_right, text="Destino",
             **estilos.estilo_label(fg=estilos.COLOR_TEXTO_OSCURO)).pack(anchor="w", pady=(6, 2))
    _cb_destino = ttk.Combobox(panel_right, values=logica_interfaz.obtener_modulos(), state="readonly")
    _cb_destino.pack(anchor="w", pady=(0, 8))

    _resultado_txt = tk.Text(panel_right, height=10, width=30,
                              bg=estilos.COLOR_FONDO, fg=estilos.COLOR_TEXTO, relief="flat")
    _resultado_txt.pack(anchor="w", pady=(10, 8))
    _resultado_txt.config(state="disabled")

    tk.Button(panel_right, text="Mostrar ruta", pady=10,
              command=_mostrar_ruta,
              **estilos.estilo_boton()).pack(anchor="w", pady=(6, 6))
    tk.Button(panel_right, text="VOLVER", pady=10,
              command=on_volver,
              **estilos.estilo_boton(color_fg=estilos.COLOR_TEXTO_OSCURO)).pack(anchor="w")

    return frame


def refrescar_ruta():
    """Actualiza los valores de los combobox y limpia el resultado."""
    modulos = logica_interfaz.obtener_modulos() or []
    try:
        _cb_inicio["values"]  = modulos
        _cb_destino["values"] = modulos
        _cb_inicio.set("")
        _cb_destino.set("")
        _resultado_txt.config(state="normal")
        _resultado_txt.delete("1.0", "end")
        _resultado_txt.config(state="disabled")
    except Exception:
        pass


def _mostrar_ruta():
    inicio  = _cb_inicio.get().strip()
    destino = _cb_destino.get().strip()
    if not inicio or not destino:
        messagebox.showwarning("Ruta", "Selecciona inicio y destino.")
        return
    ruta = logica_interfaz.ruta(inicio, destino)
    _resultado_txt.config(state="normal")
    _resultado_txt.delete("1.0", "end")
    if ruta:
        _resultado_txt.insert("end", " → ".join(ruta))
    else:
        _resultado_txt.insert("end", "No existe ruta entre los módulos seleccionados.")
    _resultado_txt.config(state="disabled")
