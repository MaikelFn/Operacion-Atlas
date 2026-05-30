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
    Entrada: ventana (tk.Tk), on_volver (callable).
    Salida: frame (tk.Frame).
    Funcionamiento: Construye y retorna la interfaz de módulos visitados.
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
    """
    Entrada: Ninguna (usa variables globales y logica_interfaz).
    Salida: Ninguna.
    Funcionamiento: Recarga la lista de módulos visitados desde logica_interfaz.
    """
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
    """
    Entrada: modulo (str).
    Salida: Ninguna.
    Funcionamiento: Muestra el nombre y la descripción del módulo visitado seleccionado.
    """
    _vis_seleccion_var.set(modulo)
    _vis_descripcion_var.set(logica_interfaz.obtener_descripcion_modulo(modulo))


# ──────────────────────────────────────────────
# BUSCAR RUTA ENTRE MÓDULOS
# ──────────────────────────────────────────────

_cb_inicio      = None
_cb_destino     = None
_lista_frame    = None   # frame interior del canvas donde se colocan los labels
_canvas_ruta    = None
_scroll_ruta    = None

# Colores de los nodos
_COLOR_ORIGEN    = "#4A90D9"   # Azul  — módulo de inicio
_COLOR_ACCESIBLE = "#2ECC71"   # Verde — puede acceder
_COLOR_BLOQUEADO = "#E74C3C"   # Rojo  — no puede acceder
_COLOR_NODO_TXT  = "#0D0D0D"   # Texto oscuro sobre los nodos


def _puede_acceder_modulo(modulo):
    """
    Entrada: modulo (str).
    Salida: bool.
    Funcionamiento: Consulta a Prolog si el jugador cumple los tres requisitos
                    de acceso al módulo (artefacto, paso previo y estado).
    """
    prolog = logica_interfaz.obtener_prolog()
    try:
        arte_ok  = next(prolog.query(f"cumple_requisito_artefacto({modulo})"), None) is not None
        paso_ok  = next(prolog.query(f"cumple_paso_previo({modulo})"),         None) is not None
        est_ok   = next(prolog.query(f"cumple_requisito_estado({modulo})"),    None) is not None
        return arte_ok and paso_ok and est_ok
    except Exception:
        return True


def _poblar_lista_ruta(ruta, inicio):
    """
    Entrada: ruta (list[str]), inicio (str).
    Salida: Ninguna.
    Funcionamiento: Limpia el frame interior y crea un Label por cada nodo
                    más un Label de flecha entre ellos. Sin cálculos de posición.
    """
    for w in _lista_frame.winfo_children():
        w.destroy()

    if not ruta:
        tk.Label(
            _lista_frame,
            text="No existe ruta entre los módulos seleccionados.",
            bg=estilos.COLOR_FONDO, fg=estilos.COLOR_TEXTO_OSCURO,
            font=("Courier", 11, "italic"),
        ).pack(pady=8)
        _canvas_ruta.update_idletasks()
        _canvas_ruta.config(scrollregion=_canvas_ruta.bbox("all"))
        return

    for i, modulo in enumerate(ruta):
        es_inicio = (i == 0)

        if es_inicio:
            bg = _COLOR_ORIGEN
            etiqueta = "ORIGEN"
        elif _puede_acceder_modulo(modulo):
            bg = _COLOR_ACCESIBLE
            etiqueta = "✓ accesible"
        else:
            bg = _COLOR_BLOQUEADO
            etiqueta = "✗ bloqueado"

        # Contenedor del nodo para darle padding interno con el color de fondo
        nodo = tk.Frame(_lista_frame, bg=bg, padx=14, pady=6)
        nodo.pack(pady=(0, 0))

        tk.Label(
            nodo,
            text=etiqueta,
            bg=bg, fg=_COLOR_NODO_TXT,
            font=("Courier", 8, "bold"),
        ).pack()

        tk.Label(
            nodo,
            text=modulo,
            bg=bg, fg=_COLOR_NODO_TXT,
            font=("Courier", 12, "bold"),
        ).pack()

        # Flecha entre nodos (excepto después del último)
        if i < len(ruta) - 1:
            tk.Label(
                _lista_frame,
                text="↓",
                bg=estilos.COLOR_FONDO, fg=estilos.COLOR_TEXTO_OSCURO,
                font=("Courier", 14, "bold"),
            ).pack(pady=2)

    # Actualizar la región de scroll
    _canvas_ruta.update_idletasks()
    _canvas_ruta.config(scrollregion=_canvas_ruta.bbox("all"))


def construir_ruta(ventana, on_volver):
    """
    Entrada: ventana (tk.Tk), on_volver (callable).
    Salida: frame (tk.Frame).
    Funcionamiento: Construye y retorna la interfaz para calcular ruta entre módulos.
    """
    global _cb_inicio, _cb_destino, _lista_frame, _canvas_ruta, _scroll_ruta

    frame = tk.Frame(ventana, bg=estilos.COLOR_FONDO)
    frame.config(width=900, height=550)
    frame.pack_propagate(False)

    contenedor = tk.Frame(frame, bg=estilos.COLOR_FONDO)
    contenedor.pack(fill="both", expand=True, padx=18, pady=16)

    # ── Panel izquierdo: título + lista de nodos con scroll ──
    panel_left = tk.Frame(contenedor, bg=estilos.COLOR_FONDO)
    panel_left.pack(side="left", fill="both", expand=True, padx=(0, 14))

    tk.Label(
        panel_left, text="VER RUTA",
        **estilos.estilo_label(fg=estilos.COLOR_BOTON_TEXTO, font=("Courier", 18, "bold")),
    ).pack(anchor="w", pady=(0, 10))

    # Canvas + scrollbar que contiene el frame de nodos
    wrap = tk.Frame(panel_left, bg=estilos.COLOR_FONDO)
    wrap.pack(fill="both", expand=True)

    _scroll_ruta = tk.Scrollbar(wrap, orient="vertical")
    _scroll_ruta.pack(side="right", fill="y")

    _canvas_ruta = tk.Canvas(
        wrap,
        bg=estilos.COLOR_FONDO,
        highlightthickness=0,
        yscrollcommand=_scroll_ruta.set,
    )
    _canvas_ruta.pack(side="left", fill="both", expand=True)
    _scroll_ruta.config(command=_canvas_ruta.yview)

    # Frame interior donde viven los labels — anclado al canvas
    _lista_frame = tk.Frame(_canvas_ruta, bg=estilos.COLOR_FONDO)
    _canvas_ruta.create_window((0, 0), window=_lista_frame, anchor="nw")

    # Mensaje inicial
    tk.Label(
        _lista_frame,
        text="Selecciona origen y destino para calcular la ruta.",
        bg=estilos.COLOR_FONDO, fg=estilos.COLOR_TEXTO_OSCURO,
        font=("Courier", 11, "italic"),
    ).pack(pady=8)

    # ── Panel derecho: controles ──
    panel_right = tk.Frame(contenedor, bg=estilos.COLOR_FONDO, width=220)
    panel_right.pack(side="left", fill="y")
    panel_right.pack_propagate(False)

    tk.Label(panel_right, text="Inicio",
             **estilos.estilo_label(fg=estilos.COLOR_TEXTO_OSCURO,
                                    font=("Courier", 11, "bold"))).pack(anchor="w", pady=(6, 2))
    _cb_inicio = ttk.Combobox(panel_right, values=logica_interfaz.obtener_modulos(),
                               state="readonly", width=24)
    _cb_inicio.pack(anchor="w", pady=(0, 10))

    tk.Label(panel_right, text="Destino",
             **estilos.estilo_label(fg=estilos.COLOR_TEXTO_OSCURO,
                                    font=("Courier", 11, "bold"))).pack(anchor="w", pady=(0, 2))
    _cb_destino = ttk.Combobox(panel_right, values=logica_interfaz.obtener_modulos(),
                                state="readonly", width=24)
    _cb_destino.pack(anchor="w", pady=(0, 14))

    tk.Button(
        panel_right, text="Mostrar ruta", pady=10,
        command=_mostrar_ruta,
        **estilos.estilo_boton(),
    ).pack(anchor="w", pady=(0, 8), fill="x")

    tk.Button(
        panel_right, text="VOLVER", pady=10,
        command=on_volver,
        **estilos.estilo_boton(color_fg=estilos.COLOR_TEXTO_OSCURO),
    ).pack(anchor="w", fill="x")

    return frame


def refrescar_ruta():
    """
    Entrada: Ninguna (usa variables globales y logica_interfaz).
    Salida: Ninguna.
    Funcionamiento: Actualiza los combobox y limpia la lista de nodos.
    """
    modulos = logica_interfaz.obtener_modulos() or []
    try:
        _cb_inicio["values"]  = modulos
        _cb_destino["values"] = modulos
        _cb_inicio.set("")
        _cb_destino.set("")
        for w in _lista_frame.winfo_children():
            w.destroy()
        tk.Label(
            _lista_frame,
            text="Selecciona origen y destino para calcular la ruta.",
            bg=estilos.COLOR_FONDO, fg=estilos.COLOR_TEXTO_OSCURO,
            font=("Courier", 11, "italic"),
        ).pack(pady=8)
        _canvas_ruta.update_idletasks()
        _canvas_ruta.config(scrollregion=_canvas_ruta.bbox("all"))
    except Exception:
        pass


def _mostrar_ruta():
    """
    Entrada: Ninguna (usa variables globales y logica_interfaz).
    Salida: Ninguna.
    Funcionamiento: Obtiene la ruta de logica_interfaz y la pasa a _poblar_lista_ruta().
    """
    inicio  = _cb_inicio.get().strip()
    destino = _cb_destino.get().strip()
    if not inicio or not destino:
        messagebox.showwarning("Ruta", "Selecciona inicio y destino.")
        return
    if inicio == destino:
        messagebox.showwarning("Ruta", "El origen y el destino son el mismo módulo.")
        return

    ruta = logica_interfaz.ruta(inicio, destino)
    _poblar_lista_ruta(ruta, inicio)