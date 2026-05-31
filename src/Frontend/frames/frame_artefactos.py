"""
frame_artefactos.py
Agrupa las cuatro pantallas relacionadas con artefactos:
  - Tomar:      recoger un artefacto disponible en el módulo actual.
  - Usar:       activar un artefacto del inventario.
  - Donde:      consultar en qué módulo se encuentra un artefacto.
  - Inventario: ver todos los artefactos obtenidos y su estado.
"""

import tkinter as tk
from tkinter import messagebox
import estilos as estilos
import logica_interfaz as logica_interfaz


# ==============================================
# TOMAR ARTEFACTO
# ==============================================

_tomar_seleccion_var  = None
_tomar_origen_var     = None
_tomar_lista_frame    = None


def construir_tomar(ventana, on_volver):
    """
    Entrada: ventana (tk.Tk), on_volver (callable).
    Salida: frame (tk.Frame).
    Funcionamiento: Construye y retorna la interfaz de toma de artefactos.
    """
    global _tomar_seleccion_var, _tomar_origen_var, _tomar_lista_frame

    frame = tk.Frame(ventana, bg=estilos.COLOR_FONDO)
    frame.config(width=900, height=550)
    frame.pack_propagate(False)

    _tomar_seleccion_var = tk.StringVar(value="")
    _tomar_origen_var    = tk.StringVar(value="")

    contenedor = tk.Frame(frame, bg=estilos.COLOR_FONDO)
    contenedor.pack(fill="both", expand=True, padx=18, pady=16)

    panel = tk.Frame(contenedor, bg=estilos.COLOR_FONDO, width=430)
    panel.pack(side="left", fill="both", expand=True, padx=(0, 14))
    panel.pack_propagate(False)

    tk.Label(panel, text="ARTEFACTOS DISPONIBLES",
             **estilos.estilo_label(fg=estilos.COLOR_BOTON_TEXTO, font=("Courier", 18, "bold"))
             ).pack(anchor="w", pady=(0, 10))
    tk.Label(panel, textvariable=_tomar_origen_var,
             **estilos.estilo_label(fg=estilos.COLOR_TEXTO_OSCURO, font=("Courier", 11, "bold"))
             ).pack(anchor="w", pady=(0, 10))

    _tomar_lista_frame = tk.Frame(panel, bg=estilos.COLOR_FONDO)
    _tomar_lista_frame.pack(fill="both", expand=True)

    panel_conf = tk.Frame(contenedor, bg=estilos.COLOR_FONDO, width=300)
    panel_conf.pack(side="left", fill="y")
    panel_conf.pack_propagate(False)

    tk.Label(panel_conf, text="SELECCION",
             **estilos.estilo_label(fg=estilos.COLOR_AMARILLO, font=("Courier", 15, "bold"))
             ).pack(anchor="w", pady=(0, 12))
    tk.Entry(panel_conf, textvariable=_tomar_seleccion_var,
             state="readonly", width=26, font=("Courier", 13),
             bg=estilos.COLOR_BOTON_FONDO, fg=estilos.COLOR_TEXTO, relief="flat",
             readonlybackground=estilos.COLOR_BOTON_FONDO, justify="center"
             ).pack(anchor="w", pady=(0, 16))
    tk.Button(panel_conf, text="TOMAR", pady=12,
              command=lambda: _ejecutar_tomar(on_volver),
              **estilos.estilo_boton(color_fg=estilos.COLOR_VERDE)
              ).pack(anchor="w", pady=(0, 12))
    tk.Button(panel_conf, text="VOLVER AL JUEGO", pady=12,
              command=on_volver,
              **estilos.estilo_boton(color_fg=estilos.COLOR_TEXTO_OSCURO)
              ).pack(anchor="w")

    return frame


def actualizar_tomar():
    """
    Entrada: Ninguna (usa variables globales y logica_interfaz).
    Salida: Ninguna.
    Funcionamiento: Refresca la lista de artefactos disponibles en el módulo actual.
    """
    for w in _tomar_lista_frame.winfo_children():
        w.destroy()
    _tomar_seleccion_var.set("")

    estado = logica_interfaz.obtener_estado_jugador()
    _tomar_origen_var.set(f"En: {estado['ubicacion']}")

    artefactos = logica_interfaz.obtener_artefactos_disponibles()
    if not artefactos:
        tk.Label(_tomar_lista_frame, text="No hay artefactos disponibles.",
                 **estilos.estilo_label(fg=estilos.COLOR_TEXTO_OSCURO, font=("Courier", 11, "italic"))
                 ).pack(anchor="w", pady=6)
        return
    for a in artefactos:
        tk.Button(_tomar_lista_frame, text=a, pady=10,
                  command=lambda x=a: _tomar_seleccion_var.set(x),
                  **estilos.estilo_boton(color_fg=estilos.COLOR_VERDE)
                  ).pack(anchor="w", pady=6)


def _ejecutar_tomar(on_volver):
    """
    Entrada: on_volver (callable).
    Salida: Ninguna.
    Funcionamiento: Intenta tomar el artefacto seleccionado y muestra el resultado.
    """
    artefacto = _tomar_seleccion_var.get().strip()
    if not artefacto:
        messagebox.showwarning("Tomar", "Primero selecciona un artefacto.")
        return
    if logica_interfaz.tomar(artefacto):
        messagebox.showinfo("Tomar", f"Tomaste {artefacto} y se agregó al inventario.")
        on_volver()
    else:
        messagebox.showerror("Tomar", f"No se pudo tomar {artefacto}.")


# ==============================================
# USAR ARTEFACTO
# ==============================================

_usar_seleccion_var = None
_usar_origen_var    = None
_usar_lista_frame   = None


def construir_usar(ventana, on_volver):
    """
    Entrada: ventana (tk.Tk), on_volver (callable).
    Salida: frame (tk.Frame).
    Funcionamiento: Construye y retorna la interfaz para usar artefactos.
    """
    global _usar_seleccion_var, _usar_origen_var, _usar_lista_frame

    frame = tk.Frame(ventana, bg=estilos.COLOR_FONDO)
    frame.config(width=900, height=550)
    frame.pack_propagate(False)

    _usar_seleccion_var = tk.StringVar(value="")
    _usar_origen_var    = tk.StringVar(value="")

    contenedor = tk.Frame(frame, bg=estilos.COLOR_FONDO)
    contenedor.pack(fill="both", expand=True, padx=18, pady=16)

    panel = tk.Frame(contenedor, bg=estilos.COLOR_FONDO, width=430)
    panel.pack(side="left", fill="both", expand=True, padx=(0, 14))
    panel.pack_propagate(False)

    tk.Label(panel, text="ARTEFACTOS DEL INVENTARIO",
             **estilos.estilo_label(fg=estilos.COLOR_BOTON_TEXTO, font=("Courier", 18, "bold"))
             ).pack(anchor="w", pady=(0, 10))
    tk.Label(panel, textvariable=_usar_origen_var,
             **estilos.estilo_label(fg=estilos.COLOR_TEXTO_OSCURO, font=("Courier", 11, "bold"))
             ).pack(anchor="w", pady=(0, 10))

    _usar_lista_frame = tk.Frame(panel, bg=estilos.COLOR_FONDO)
    _usar_lista_frame.pack(fill="both", expand=True)

    panel_conf = tk.Frame(contenedor, bg=estilos.COLOR_FONDO, width=300)
    panel_conf.pack(side="left", fill="y")
    panel_conf.pack_propagate(False)

    tk.Label(panel_conf, text="SELECCION",
             **estilos.estilo_label(fg=estilos.COLOR_AMARILLO, font=("Courier", 15, "bold"))
             ).pack(anchor="w", pady=(0, 12))
    tk.Entry(panel_conf, textvariable=_usar_seleccion_var,
             state="readonly", width=26, font=("Courier", 13),
             bg=estilos.COLOR_BOTON_FONDO, fg=estilos.COLOR_TEXTO, relief="flat",
             readonlybackground=estilos.COLOR_BOTON_FONDO, justify="center"
             ).pack(anchor="w", pady=(0, 16))
    tk.Button(panel_conf, text="USAR", pady=12,
              command=lambda: _ejecutar_usar(on_volver),
              **estilos.estilo_boton(color_fg=estilos.COLOR_VERDE)
              ).pack(anchor="w", pady=(0, 12))
    tk.Button(panel_conf, text="VOLVER AL JUEGO", pady=12,
              command=on_volver,
              **estilos.estilo_boton(color_fg=estilos.COLOR_TEXTO_OSCURO)
              ).pack(anchor="w")

    return frame


def actualizar_usar():
    """
    Entrada: Ninguna (usa variables globales y logica_interfaz).
    Salida: Ninguna.
    Funcionamiento: Refresca la lista de artefactos usables del inventario.
    """
    for w in _usar_lista_frame.winfo_children():
        w.destroy()
    _usar_seleccion_var.set("")

    estado = logica_interfaz.obtener_estado_jugador()
    _usar_origen_var.set(f"Inventario de: {estado['ubicacion']}")

    artefactos = logica_interfaz.obtener_artefactos_usables()
    if not artefactos:
        tk.Label(_usar_lista_frame, text="No hay artefactos usables.",
                 **estilos.estilo_label(fg=estilos.COLOR_TEXTO_OSCURO, font=("Courier", 11, "italic"))
                 ).pack(anchor="w", pady=6)
        return
    for a in artefactos:
        tk.Button(_usar_lista_frame, text=a, pady=10,
                  command=lambda x=a: _usar_seleccion_var.set(x),
                  **estilos.estilo_boton(color_fg=estilos.COLOR_AMARILLO)
                  ).pack(anchor="w", pady=6)


def _ejecutar_usar(on_volver):
    """
    Entrada: on_volver (callable).
    Salida: Ninguna.
    Funcionamiento: Intenta usar el artefacto seleccionado y muestra el resultado.
    """
    artefacto = _usar_seleccion_var.get().strip()
    if not artefacto:
        messagebox.showwarning("Usar", "Primero selecciona un artefacto.")
        return
    if logica_interfaz.usar(artefacto):
        messagebox.showinfo("Usar", f"Usaste {artefacto}.")
        on_volver()
    else:
        messagebox.showerror("Usar", f"No se pudo usar {artefacto}.")


# ==============================================
# DONDE ESTÁ EL ARTEFACTO
# ==============================================

_donde_seleccion_var = None
_donde_ubicacion_var = None
_donde_lista_frame   = None


def construir_donde(ventana, on_volver):
    """
    Entrada: ventana (tk.Tk), on_volver (callable).
    Salida: frame (tk.Frame).
    Funcionamiento: Construye y retorna la interfaz para consultar ubicación de artefactos.
    """
    global _donde_seleccion_var, _donde_ubicacion_var, _donde_lista_frame

    frame = tk.Frame(ventana, bg=estilos.COLOR_FONDO)
    frame.config(width=900, height=550)
    frame.pack_propagate(False)

    _donde_seleccion_var = tk.StringVar(value="")
    _donde_ubicacion_var = tk.StringVar(value="")

    contenedor = tk.Frame(frame, bg=estilos.COLOR_FONDO)
    contenedor.pack(fill="both", expand=True, padx=18, pady=16)

    panel = tk.Frame(contenedor, bg=estilos.COLOR_FONDO, width=430)
    panel.pack(side="left", fill="both", expand=True, padx=(0, 14))
    panel.pack_propagate(False)

    tk.Label(panel, text="ARTEFACTOS FUERA DEL INVENTARIO",
             **estilos.estilo_label(fg=estilos.COLOR_BOTON_TEXTO, font=("Courier", 18, "bold"))
             ).pack(anchor="w", pady=(0, 10))

    _donde_lista_frame = tk.Frame(panel, bg=estilos.COLOR_FONDO)
    _donde_lista_frame.pack(fill="both", expand=True)

    panel_res = tk.Frame(contenedor, bg=estilos.COLOR_FONDO, width=300)
    panel_res.pack(side="left", fill="y")
    panel_res.pack_propagate(False)

    tk.Label(panel_res, text="SELECCION",
             **estilos.estilo_label(fg=estilos.COLOR_AMARILLO, font=("Courier", 15, "bold"))
             ).pack(anchor="w", pady=(0, 12))
    tk.Entry(panel_res, textvariable=_donde_seleccion_var,
             state="readonly", width=26, font=("Courier", 13),
             bg=estilos.COLOR_BOTON_FONDO, fg=estilos.COLOR_TEXTO, relief="flat",
             readonlybackground=estilos.COLOR_BOTON_FONDO, justify="center"
             ).pack(anchor="w", pady=(0, 16))
    tk.Label(panel_res, textvariable=_donde_ubicacion_var,
             wraplength=260, justify="left",
             **estilos.estilo_label(fg=estilos.COLOR_TEXTO, font=("Courier", 12, "bold"))
             ).pack(anchor="w", pady=(0, 16))
    tk.Button(panel_res, text="VOLVER AL JUEGO", pady=12,
              command=on_volver,
              **estilos.estilo_boton(color_fg=estilos.COLOR_TEXTO_OSCURO)
              ).pack(anchor="w")

    return frame


def actualizar_donde():
    """
    Entrada: Ninguna (usa variables globales y logica_interfaz).
    Salida: Ninguna.
    Funcionamiento: Refresca la lista de artefactos fuera del inventario.
    """
    for w in _donde_lista_frame.winfo_children():
        w.destroy()
    _donde_seleccion_var.set("")
    _donde_ubicacion_var.set("")

    artefactos = logica_interfaz.obtener_artefactos_faltantes()
    if not artefactos:
        tk.Label(_donde_lista_frame, text="No hay artefactos fuera del inventario.",
                 **estilos.estilo_label(fg=estilos.COLOR_TEXTO_OSCURO, font=("Courier", 11, "italic"))
                 ).pack(anchor="w", pady=6)
        return
    for a in artefactos:
        tk.Button(_donde_lista_frame, text=a, pady=10,
                  command=lambda x=a: _seleccionar_donde(x),
                  **estilos.estilo_boton(color_fg=estilos.COLOR_AZUL)
                  ).pack(anchor="w", pady=6)


def _seleccionar_donde(artefacto):
    """
    Entrada: artefacto (str).
    Salida: Ninguna.
    Funcionamiento: Muestra el módulo donde se encuentra el artefacto seleccionado.
    """
    _donde_seleccion_var.set(artefacto)
    modulo = logica_interfaz.donde_esta(artefacto)
    _donde_ubicacion_var.set(f"Se encuentra en: {modulo}")


# ==============================================
# INVENTARIO
# ==============================================

_inv_seleccion_var = None
_inv_detalle_var   = None
_inv_lista_frame   = None


def construir_inventario(ventana, on_volver):
    """
    Entrada: ventana (tk.Tk), on_volver (callable).
    Salida: frame (tk.Frame).
    Funcionamiento: Construye y retorna la interfaz del inventario del jugador.
    """
    global _inv_seleccion_var, _inv_detalle_var, _inv_lista_frame

    frame = tk.Frame(ventana, bg=estilos.COLOR_FONDO)
    frame.config(width=900, height=550)
    frame.pack_propagate(False)

    _inv_seleccion_var = tk.StringVar(value="")
    _inv_detalle_var   = tk.StringVar(value="")

    contenedor = tk.Frame(frame, bg=estilos.COLOR_FONDO)
    contenedor.pack(fill="both", expand=True, padx=18, pady=16)

    panel = tk.Frame(contenedor, bg=estilos.COLOR_FONDO, width=430)
    panel.pack(side="left", fill="both", expand=True, padx=(0, 14))
    panel.pack_propagate(False)

    tk.Label(panel, text="INVENTARIO DEL JUGADOR",
             **estilos.estilo_label(fg=estilos.COLOR_BOTON_TEXTO, font=("Courier", 18, "bold"))
             ).pack(anchor="w", pady=(0, 10))

    _inv_lista_frame = tk.Frame(panel, bg=estilos.COLOR_FONDO)
    _inv_lista_frame.pack(fill="both", expand=True)

    panel_det = tk.Frame(contenedor, bg=estilos.COLOR_FONDO, width=300)
    panel_det.pack(side="left", fill="y")
    panel_det.pack_propagate(False)

    tk.Label(panel_det, text="SELECCION",
             **estilos.estilo_label(fg=estilos.COLOR_AMARILLO, font=("Courier", 15, "bold"))
             ).pack(anchor="w", pady=(0, 12))
    tk.Entry(panel_det, textvariable=_inv_seleccion_var,
             state="readonly", width=26, font=("Courier", 13),
             bg=estilos.COLOR_BOTON_FONDO, fg=estilos.COLOR_TEXTO, relief="flat",
             readonlybackground=estilos.COLOR_BOTON_FONDO, justify="center"
             ).pack(anchor="w", pady=(0, 16))
    tk.Label(panel_det, textvariable=_inv_detalle_var,
             wraplength=260, justify="left",
             **estilos.estilo_label(fg=estilos.COLOR_TEXTO, font=("Courier", 12, "bold"))
             ).pack(anchor="w", pady=(0, 16))
    tk.Button(panel_det, text="VOLVER AL JUEGO", pady=12,
              command=on_volver,
              **estilos.estilo_boton(color_fg=estilos.COLOR_TEXTO_OSCURO)
              ).pack(anchor="w")

    return frame


def actualizar_inventario():
    """
    Entrada: Ninguna (usa variables globales y logica_interfaz).
    Salida: Ninguna.
    Funcionamiento: Refresca la lista de artefactos en el inventario.
    """
    for w in _inv_lista_frame.winfo_children():
        w.destroy()
    _inv_seleccion_var.set("")
    _inv_detalle_var.set("")

    inventario = logica_interfaz.obtener_inventario_artefactos()
    if not inventario:
        tk.Label(_inv_lista_frame, text="El jugador no tiene artefactos.",
                 **estilos.estilo_label(fg=estilos.COLOR_TEXTO_OSCURO, font=("Courier", 11, "italic"))
                 ).pack(anchor="w", pady=6)
        return
    for item in inventario:
        etiqueta = item["artefacto"]
        if item["usado"]:
            etiqueta = f"{etiqueta}  [USADO]"
        tk.Button(_inv_lista_frame, text=etiqueta, pady=10,
                  command=lambda i=item: _seleccionar_inventario(i),
                  **estilos.estilo_boton(color_fg=estilos.COLOR_VERDE)
                  ).pack(anchor="w", pady=6)


def _seleccionar_inventario(item):
    """
    Entrada: item (dict con claves "artefacto", "usado", "modulo").
    Salida: Ninguna.
    Funcionamiento: Muestra los detalles del artefacto seleccionado del inventario.
    """
    _inv_seleccion_var.set(item["artefacto"])
    usado_texto = "Sí" if item["usado"] else "No"
    _inv_detalle_var.set(f"Usado: {usado_texto}\nObtenido en: {item['modulo']}")