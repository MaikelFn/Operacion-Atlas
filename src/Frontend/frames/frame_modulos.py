"""
frame_modulos.py
Agrupa las dos pantallas relacionadas con módulos y navegación:
  - Visitados: historial de módulos recorridos con descripción.
  - Ruta:      cálculo de camino entre dos módulos cualesquiera.
"""

import tkinter as tk
from tkinter import messagebox
import estilos as estilos
import logica_interfaz as logica_interfaz


# MÓDULOS VISITADOS

vis_seleccion_var   = None
vis_descripcion_var = None
vis_lista_frame     = None


def construir_visitados(ventana, on_volver):
    """
    Entrada: ventana (tk.Tk), on_volver (callable).
    Salida: frame (tk.Frame).
    Funcionamiento: Construye y retorna la interfaz de módulos visitados.
    """
    global vis_seleccion_var, vis_descripcion_var, vis_lista_frame

    frame = tk.Frame(ventana, bg=estilos.COLOR_FONDO)
    frame.config(width=900, height=550)
    frame.pack_propagate(False)

    vis_seleccion_var   = tk.StringVar(value="")
    vis_descripcion_var = tk.StringVar(value="")

    contenedor = tk.Frame(frame, bg=estilos.COLOR_FONDO)
    contenedor.pack(fill="both", expand=True, padx=18, pady=16)

    panel = tk.Frame(contenedor, bg=estilos.COLOR_FONDO, width=430)
    panel.pack(side="left", fill="both", expand=True, padx=(0, 14))
    panel.pack_propagate(False)

    tk.Label(
        panel, text="MODULOS VISITADOS",
        **estilos.estilo_label(fg=estilos.COLOR_BOTON_TEXTO, font=("Courier", 18, "bold")),
    ).pack(anchor="w", pady=(0, 10))

    vis_lista_frame = tk.Frame(panel, bg=estilos.COLOR_FONDO)
    vis_lista_frame.pack(fill="both", expand=True)

    # Panel derecho: detalle del modulo seleccionado
    panel_det = tk.Frame(contenedor, bg=estilos.COLOR_FONDO, width=300)
    panel_det.pack(side="left", fill="y")
    panel_det.pack_propagate(False)

    tk.Label(
        panel_det, textvariable=vis_seleccion_var,
        wraplength=260, justify="left",
        **estilos.estilo_label(fg=estilos.COLOR_AMARILLO, font=("Courier", 15, "bold")),
    ).pack(anchor="w", pady=(0, 10))

    tk.Label(
        panel_det, text="Descripcion del modulo:",
        **estilos.estilo_label(fg=estilos.COLOR_TEXTO_OSCURO, font=("Courier", 11, "bold")),
    ).pack(anchor="w", pady=(0, 4))

    tk.Label(
        panel_det, textvariable=vis_descripcion_var,
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
    for widget in vis_lista_frame.winfo_children():
        widget.destroy()
    vis_seleccion_var.set("")
    vis_descripcion_var.set("")

    visitados = logica_interfaz.modulos_visitados()
    if not visitados:
        tk.Label(
            vis_lista_frame,
            text="No hay modulos visitados registrados.",
            **estilos.estilo_label(fg=estilos.COLOR_TEXTO_OSCURO, font=("Courier", 11, "italic")),
        ).pack(anchor="w", pady=6)
        return

    for modulo in visitados:
        tk.Button(
            vis_lista_frame, text=modulo, pady=10,
            command=lambda m=modulo: seleccionar_visitado(m),
            **estilos.estilo_boton(color_fg=estilos.COLOR_AZUL),
        ).pack(anchor="w", pady=6)


def seleccionar_visitado(modulo):
    """
    Entrada: modulo (str).
    Salida: Ninguna.
    Funcionamiento: Muestra el nombre y la descripción del módulo visitado seleccionado.
    """
    vis_seleccion_var.set(modulo)
    vis_descripcion_var.set(logica_interfaz.obtener_descripcion_modulo(modulo))


# ──────────────────────────────────────────────
# BUSCAR RUTA ENTRE MÓDULOS
# ──────────────────────────────────────────────

listbox_inicio      = None   # Listbox de origen
listbox_destino     = None   # Listbox de destino
sel_inicio     = None   # Módulo de origen seleccionado (str)
sel_destino    = None   # Módulo de destino seleccionado (str)
idx_inicio     = None   # Índice del item marcado en lb_inicio
idx_destino    = None   # Índice del item marcado en lb_destino
lista_frame    = None   # frame interior del canvas donde se colocan los labels
canvas_ruta    = None
scroll_ruta    = None
lista_frame_id = None  # ID del create_window para reposicionar

# Colores de los nodos
COLOR_ORIGEN    = "#4A90D9"   # Azul  — módulo de inicio
COLOR_ACCESIBLE = "#2ECC71"   # Verde — puede acceder
COLOR_BLOQUEADO = "#E74C3C"   # Rojo  — no puede acceder
COLOR_NODO_TXT  = "#0D0D0D"   # Texto oscuro sobre los nodos


def puede_acceder_modulo(modulo):
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


def poblar_lista_ruta(ruta, inicio):
    """
    Entrada: ruta (list[str]), inicio (str).
    Salida: Ninguna.
    Funcionamiento: Limpia el frame interior y crea un Label por cada nodo
                    más un Label de flecha entre ellos, centrados en el canvas.
    """
    for widget in lista_frame.winfo_children():
        widget.destroy()

    if not ruta:
        tk.Label(
            lista_frame,
            text="No existe ruta entre los módulos seleccionados.",
            bg=estilos.COLOR_FONDO, fg=estilos.COLOR_TEXTO_OSCURO,
            font=("Courier", 11, "italic"),
        ).pack(pady=8)
        canvas_ruta.update_idletasks()
        canvas_ruta.config(scrollregion=canvas_ruta.bbox("all"))
        return

    for indice, modulo in enumerate(ruta):
        es_inicio = (indice == 0)

        if es_inicio:
            bg = COLOR_ORIGEN
            etiqueta = "ORIGEN"
        elif puede_acceder_modulo(modulo):
            bg = COLOR_ACCESIBLE
            etiqueta = "✓ accesible"
        else:
            bg = COLOR_BLOQUEADO
            etiqueta = "✗ bloqueado"

        # Nodo: ancho fijo grande, centrado
        nodo = tk.Frame(lista_frame, bg=bg, padx=0, pady=10, width=260, height=64)
        nodo.pack(pady=(0, 0))
        nodo.pack_propagate(False)

        tk.Label(
            nodo,
            text=etiqueta,
            bg=bg, fg=COLOR_NODO_TXT,
            font=("Courier", 9, "bold"),
        ).pack(expand=True)

        tk.Label(
            nodo,
            text=modulo,
            bg=bg, fg=COLOR_NODO_TXT,
            font=("Courier", 14, "bold"),
        ).pack(expand=True)

        # Flecha entre nodos (excepto después del último)
        if indice < len(ruta) - 1:
            tk.Label(
                lista_frame,
                text="↓",
                bg=estilos.COLOR_FONDO, fg=estilos.COLOR_TEXTO_OSCURO,
                font=("Courier", 16, "bold"),
            ).pack(pady=3)

    # Centrar el frame interior en el canvas
    canvas_ruta.update_idletasks()
    canvas_w = canvas_ruta.winfo_width()
    frame_w  = lista_frame.winfo_reqwidth()
    x_offset = max(0, (canvas_w - frame_w) // 2)
    canvas_ruta.coords(lista_frame_id, x_offset, 10)
    canvas_ruta.config(scrollregion=canvas_ruta.bbox("all"))


def construir_ruta(ventana, on_volver):
    """
    Entrada: ventana (tk.Tk), on_volver (callable).
    Salida: frame (tk.Frame).
    Funcionamiento: Construye y retorna la interfaz para calcular ruta entre módulos.
    """
    global listbox_inicio, listbox_destino, sel_inicio, sel_destino, idx_inicio, idx_destino, lista_frame, canvas_ruta, scroll_ruta, lista_frame_id
    sel_inicio  = None
    sel_destino = None
    idx_inicio  = None
    idx_destino = None

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

    wrap = tk.Frame(panel_left, bg=estilos.COLOR_FONDO)
    wrap.pack(fill="both", expand=True)

    scroll_ruta = tk.Scrollbar(wrap, orient="vertical")
    scroll_ruta.pack(side="right", fill="y")

    canvas_ruta = tk.Canvas(
        wrap,
        bg=estilos.COLOR_FONDO,
        highlightthickness=0,
        yscrollcommand=scroll_ruta.set,
    )
    canvas_ruta.pack(side="left", fill="both", expand=True)
    scroll_ruta.config(command=canvas_ruta.yview)

    lista_frame = tk.Frame(canvas_ruta, bg=estilos.COLOR_FONDO)
    lista_frame_id = canvas_ruta.create_window((0, 10), window=lista_frame, anchor="n")

    def centrar_lista(event=None):
        canvas_w = canvas_ruta.winfo_width()
        frame_w  = lista_frame.winfo_reqwidth()
        x_offset = max(frame_w // 2, canvas_w // 2)
        canvas_ruta.coords(lista_frame_id, x_offset, 10)
        canvas_ruta.config(scrollregion=canvas_ruta.bbox("all"))

    canvas_ruta.bind("<Configure>", centrar_lista)

    tk.Label(
        lista_frame,
        text="Selecciona origen y destino para calcular la ruta.",
        bg=estilos.COLOR_FONDO, fg=estilos.COLOR_TEXTO_OSCURO,
        font=("Courier", 11, "italic"),
    ).pack(pady=8)

    panel_right = tk.Frame(contenedor, bg=estilos.COLOR_FONDO, width=240)
    panel_right.pack(side="left", fill="both")
    panel_right.pack_propagate(False)

    tk.Label(panel_right, text="Origen", 
             **estilos.estilo_label(fg=estilos.COLOR_TEXTO_OSCURO,
                                    font=("Courier", 11, "bold"))).pack(anchor="w", pady=(6, 2))

    wrap_ini = tk.Frame(panel_right, bg=estilos.COLOR_FONDO)
    wrap_ini.pack(fill="both", expand=True, pady=(0, 8))

    sb_ini = tk.Scrollbar(wrap_ini, orient="vertical")
    sb_ini.pack(side="right", fill="y")

    listbox_inicio = tk.Listbox(
        wrap_ini,
        yscrollcommand=sb_ini.set,
        selectmode="single",
        bg="#1A1A2E", fg=estilos.COLOR_TEXTO,
        selectbackground=COLOR_ORIGEN, selectforeground=COLOR_NODO_TXT,
        font=("Courier", 11), borderwidth=0, highlightthickness=1,
        highlightcolor=estilos.COLOR_AZUL, activestyle="none",
    )
    listbox_inicio.pack(side="left", fill="both", expand=True)
    sb_ini.config(command=listbox_inicio.yview)

    def _onsel_inicio(event=None):
        global sel_inicio, idx_inicio
        sel = listbox_inicio.curselection()
        if sel:
            if idx_inicio is not None:
                listbox_inicio.itemconfig(idx_inicio, bg="#1A1A2E", fg=estilos.COLOR_TEXTO)
            idx_inicio = sel[0]
            sel_inicio = listbox_inicio.get(idx_inicio)
            listbox_inicio.itemconfig(idx_inicio, bg=COLOR_ORIGEN, fg=COLOR_NODO_TXT)
    listbox_inicio.bind("<<ListboxSelect>>", _onsel_inicio)

    for modulo in (logica_interfaz.obtener_modulos() or []):
        listbox_inicio.insert("end", modulo)

    tk.Label(panel_right, text="Destino",
             **estilos.estilo_label(fg=estilos.COLOR_TEXTO_OSCURO,
                                    font=("Courier", 11, "bold"))).pack(anchor="w", pady=(0, 2))

    wrap_dst = tk.Frame(panel_right, bg=estilos.COLOR_FONDO)
    wrap_dst.pack(fill="both", expand=True, pady=(0, 10))

    sb_dst = tk.Scrollbar(wrap_dst, orient="vertical")
    sb_dst.pack(side="right", fill="y")

    listbox_destino = tk.Listbox(
        wrap_dst,
        yscrollcommand=sb_dst.set,
        selectmode="single",
        bg="#1A1A2E", fg=estilos.COLOR_TEXTO,
        selectbackground=COLOR_BLOQUEADO, selectforeground=COLOR_NODO_TXT,
        font=("Courier", 11), borderwidth=0, highlightthickness=1,
        highlightcolor=estilos.COLOR_AZUL, activestyle="none",
    )
    listbox_destino.pack(side="left", fill="both", expand=True)
    sb_dst.config(command=listbox_destino.yview)

    def _onsel_destino(event=None):
        global sel_destino, idx_destino
        sel = listbox_destino.curselection()
        if sel:
            if idx_destino is not None:
                listbox_destino.itemconfig(idx_destino, bg="#1A1A2E", fg=estilos.COLOR_TEXTO)
            idx_destino = sel[0]
            sel_destino = listbox_destino.get(idx_destino)
            listbox_destino.itemconfig(idx_destino, bg=COLOR_BLOQUEADO, fg=COLOR_NODO_TXT)
    listbox_destino.bind("<<ListboxSelect>>", _onsel_destino)

    for modulo in (logica_interfaz.obtener_modulos() or []):
        listbox_destino.insert("end", modulo)

    tk.Button(
        panel_right, text="Mostrar ruta", pady=10,
        command=mostrar_ruta,
        **estilos.estilo_boton(),
    ).pack(fill="x", pady=(0, 6))

    tk.Button(
        panel_right, text="VOLVER", pady=10,
        command=on_volver,
        **estilos.estilo_boton(color_fg=estilos.COLOR_TEXTO_OSCURO),
    ).pack(fill="x")

    return frame


def refrescar_ruta():
    """
    Entrada: Ninguna (usa variables globales y logica_interfaz).
    Salida: Ninguna.
    Funcionamiento: Actualiza los listbox y limpia la lista de nodos.
    """
    global sel_inicio, sel_destino, idx_inicio, idx_destino
    modulos = logica_interfaz.obtener_modulos() or []
    try:
        sel_inicio  = None
        sel_destino = None
        idx_inicio  = None
        idx_destino = None
        for listbox in (listbox_inicio, listbox_destino):
            listbox.delete(0, "end")
            for modulo in modulos:
                listbox.insert("end", modulo)
        for widget in lista_frame.winfo_children():
            widget.destroy()
        tk.Label(
            lista_frame,
            text="Selecciona origen y destino para calcular la ruta.",
            bg=estilos.COLOR_FONDO, fg=estilos.COLOR_TEXTO_OSCURO,
            font=("Courier", 11, "italic"),
        ).pack(pady=8)
        canvas_ruta.update_idletasks()
        canvas_ruta.config(scrollregion=canvas_ruta.bbox("all"))
    except Exception:
        pass

def mostrar_ruta():
    """
    Entrada: Ninguna (usa variables globales y logica_interfaz).
    Salida: Ninguna.
    Funcionamiento: Obtiene la ruta de logica_interfaz y la pasa a poblar_lista_ruta().
    """
    inicio  = sel_inicio  or ""
    destino = sel_destino or ""
    if not inicio or not destino:
        messagebox.showwarning("Ruta", "Selecciona inicio y destino.")
        return
    if inicio == destino:
        messagebox.showwarning("Ruta", "El origen y el destino son el mismo módulo.")
        return

    ruta = logica_interfaz.ruta(inicio, destino)
    poblar_lista_ruta(ruta, inicio)