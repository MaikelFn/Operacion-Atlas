"""
frame_sistemas.py
Pantalla de reparación de sistemas:
lista los sistemas en fallo del módulo actual,
muestra los artefactos requeridos para cada uno
y permite ejecutar la reparación.
"""

import tkinter as tk
from tkinter import messagebox
import estilos as estilos
import logica_interfaz as logica_interfaz


seleccion_sistema_var      = None
lista_sistemas_frame       = None
lista_artefactos_req_frame = None


def construir(ventana, on_volver):
    """
    Entrada: ventana (tk.Tk), on_volver (callable).
    Salida: frame (tk.Frame).
    Funcionamiento: Construye y retorna la interfaz de reparación de sistemas.
    """
    global seleccion_sistema_var, lista_sistemas_frame, lista_artefactos_req_frame

    frame = tk.Frame(ventana, bg=estilos.COLOR_FONDO)
    frame.config(width=900, height=550)
    frame.pack_propagate(False)

    seleccion_sistema_var = tk.StringVar(value="")

    contenedor = tk.Frame(frame, bg=estilos.COLOR_FONDO)
    contenedor.pack(fill="both", expand=True, padx=18, pady=16)

    panel = tk.Frame(contenedor, bg=estilos.COLOR_FONDO, width=430)
    panel.pack(side="left", fill="both", expand=True, padx=(0, 14))
    panel.pack_propagate(False)

    tk.Label(
        panel, text="SISTEMAS EN FALLA (MODULO ACTUAL)",
        **estilos.estilo_label(fg=estilos.COLOR_BOTON_TEXTO, font=("Courier", 18, "bold")),
    ).pack(anchor="w", pady=(0, 10))

    lista_sistemas_frame = tk.Frame(panel, bg=estilos.COLOR_FONDO)
    lista_sistemas_frame.pack(fill="both", expand=True)

    panel_det = tk.Frame(contenedor, bg=estilos.COLOR_FONDO, width=300)
    panel_det.pack(side="left", fill="y")
    panel_det.pack_propagate(False)

    tk.Label(
        panel_det, text="SELECCION",
        **estilos.estilo_label(fg=estilos.COLOR_AMARILLO, font=("Courier", 15, "bold")),
    ).pack(anchor="w", pady=(0, 12))

    tk.Entry(
        panel_det, textvariable=seleccion_sistema_var,
        state="readonly", width=26, font=("Courier", 13),
        bg=estilos.COLOR_BOTON_FONDO, fg=estilos.COLOR_TEXTO,
        relief="flat", readonlybackground=estilos.COLOR_BOTON_FONDO, justify="center",
    ).pack(anchor="w", pady=(0, 8))

    tk.Label(
        panel_det, text="Artefactos requeridos:",
        **estilos.estilo_label(fg=estilos.COLOR_TEXTO_OSCURO, font=("Courier", 11, "bold")),
    ).pack(anchor="w", pady=(8, 4))

    lista_artefactos_req_frame = tk.Frame(panel_det, bg=estilos.COLOR_FONDO)
    lista_artefactos_req_frame.pack(fill="both", expand=True)

    tk.Button(
        panel_det, text="REPARAR", pady=12,
        command=lambda: ejecutar_reparacion(on_volver),
        **estilos.estilo_boton(color_fg=estilos.COLOR_VERDE),
    ).pack(anchor="w", pady=(0, 12))

    tk.Button(
        panel_det, text="VOLVER AL JUEGO", pady=12,
        command=on_volver,
        **estilos.estilo_boton(color_fg=estilos.COLOR_TEXTO_OSCURO),
    ).pack(anchor="w")

    return frame


def actualizar():
    """
    Entrada: Ninguna (usa variables globales y logica_interfaz).
    Salida: Ninguna.
    Funcionamiento: Recarga la lista de sistemas en fallo del módulo actual.
    """
    for widget in lista_sistemas_frame.winfo_children():
        widget.destroy()
    for widget in lista_artefactos_req_frame.winfo_children():
        widget.destroy()
    seleccion_sistema_var.set("")

    sistemas = logica_interfaz.obtener_sistemas_en_fallo()
    if not sistemas:
        tk.Label(
            lista_sistemas_frame,
            text="No hay sistemas a reparar en este módulo.",
            **estilos.estilo_label(fg=estilos.COLOR_TEXTO_OSCURO, font=("Courier", 11, "italic")),
        ).pack(anchor="w", pady=6)
        return

    for sistema in sistemas:
        tk.Button(
            lista_sistemas_frame, text=sistema, pady=10,
            command=lambda nombre=sistema: seleccionar_sistema(nombre),
            **estilos.estilo_boton(color_fg=estilos.COLOR_AMARILLO),
        ).pack(anchor="w", pady=6)


def seleccionar_sistema(sistema):
    """
    Entrada: sistema (str).
    Salida: Ninguna.
    Funcionamiento: Muestra los artefactos requeridos para reparar el sistema seleccionado.
    """
    seleccion_sistema_var.set(sistema)

    for widget in lista_artefactos_req_frame.winfo_children():
        widget.destroy()

    artefactos = logica_interfaz.obtener_artefactos_requeridos_sistema(sistema)
    if not artefactos:
        tk.Label(
            lista_artefactos_req_frame,
            text="No hay artefactos listados para este sistema.",
            **estilos.estilo_label(fg=estilos.COLOR_TEXTO_OSCURO, font=("Courier", 11, "italic")),
        ).pack(anchor="w", pady=6)
        return

    for artefacto in artefactos:
        tk.Label(
            lista_artefactos_req_frame, text=artefacto,
            **estilos.estilo_label(fg=estilos.COLOR_VERDE, font=("Courier", 12, "bold")),
        ).pack(anchor="w", pady=6)


def ejecutar_reparacion(on_volver):
    """
    Entrada: on_volver (callable).
    Salida: Ninguna.
    Funcionamiento: Intenta reparar el sistema seleccionado y muestra el resultado.
    """
    sistema = seleccion_sistema_var.get().strip()
    if not sistema:
        messagebox.showwarning("Reparar", "Selecciona primero un sistema.")
        return

    if logica_interfaz.reparar(sistema):
        messagebox.showinfo("Reparar", f"Sistema {sistema} reparado con éxito.")
        on_volver()
    else:
        messagebox.showerror(
            "Reparar",
            f"No se pudo reparar {sistema}. Asegúrate de usar los artefactos requeridos."
        )