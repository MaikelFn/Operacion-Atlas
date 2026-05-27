"""
main.py
Punto de entrada de Operacion Atlas.
Crea la ventana principal y orquesta la navegacion entre todos los frames.
"""

import sys
import os

# Asegura que Python encuentre los modulos del Frontend
sys.path.insert(0, os.path.dirname(__file__))

import tkinter as tk
import estilos as estilos
import logica_interfaz as logica_interfaz

import frames.frame_estado      as modulo_frame_estado
import frames.frame_menu        as modulo_frame_menu
import frames.frame_juego       as modulo_frame_juego
import frames.frame_movimiento  as modulo_frame_movimiento
import frames.frame_artefactos  as modulo_frame_artefactos
import frames.frame_sistemas    as modulo_frame_sistemas
import frames.frame_tripulantes as modulo_frame_tripulantes
import frames.frame_modulos     as modulo_frame_modulos
import frames.frame_victoria    as modulo_frame_victoria


# ──────────────────────────────────────────────
# VENTANA PRINCIPAL
# ──────────────────────────────────────────────

ventana = tk.Tk()
ventana.title("Operacion Atlas")
ventana.geometry("900x550")
ventana.resizable(False, False)
ventana.configure(bg=estilos.COLOR_FONDO)


# ──────────────────────────────────────────────
# CONSTRUCCIÓN DE FRAMES
# ──────────────────────────────────────────────

# Frames contenedores persistentes
frame_juego      = tk.Frame(ventana, bg=estilos.COLOR_FONDO, width=900, height=550)
frame_mover      = modulo_frame_movimiento.construir(ventana, on_volver=lambda: abrir_juego())
frame_tomar      = modulo_frame_artefactos.construir_tomar(ventana, on_volver=lambda: abrir_juego())
frame_usar       = modulo_frame_artefactos.construir_usar(ventana, on_volver=lambda: abrir_juego())
frame_donde      = modulo_frame_artefactos.construir_donde(ventana, on_volver=lambda: abrir_juego())
frame_inventario = modulo_frame_artefactos.construir_inventario(ventana, on_volver=lambda: abrir_juego())
frame_reparar    = modulo_frame_sistemas.construir(ventana, on_volver=lambda: abrir_juego())
frame_rescatar   = modulo_frame_tripulantes.construir(ventana, on_volver=lambda: abrir_juego())
frame_visitados  = modulo_frame_modulos.construir_visitados(ventana, on_volver=lambda: abrir_juego())
frame_ruta       = modulo_frame_modulos.construir_ruta(ventana, on_volver=lambda: abrir_juego())
frame_victoria   = modulo_frame_victoria.construir(ventana, on_volver=lambda: abrir_juego())

frame_juego.config(width=900, height=550)
frame_juego.pack_propagate(False)

# Panel izquierdo de estado (dentro del frame de juego)
texto_estado = modulo_frame_estado.construir(frame_juego)

# Panel derecho de acciones (dentro del frame de juego)
modulo_frame_juego.construir(frame_juego, callbacks={
    "mover":      lambda: abrir_pantalla_mover(),
    "ruta":       lambda: abrir_pantalla_ruta(),
    "tomar":      lambda: abrir_pantalla_tomar(),
    "usar":       lambda: abrir_pantalla_usar(),
    "donde":      lambda: abrir_pantalla_donde(),
    "inventario": lambda: abrir_pantalla_inventario(),
    "reparar":    lambda: abrir_pantalla_reparar(),
    "rescatar":   lambda: abrir_pantalla_rescatar(),
    "visitados":  lambda: abrir_pantalla_visitados(),
    "victoria":   lambda: abrir_pantalla_victoria(),
    "menu":       lambda: logica_interfaz.ir_a_menu(),
})

# Frame de menú (se construye al final para capturar lambdas correctamente)
frame_menu_principal = modulo_frame_menu.construir(ventana, on_jugar=lambda: abrir_juego())


# ──────────────────────────────────────────────
# REGISTRO DE FRAMES EN logica_interfaz
# ──────────────────────────────────────────────

logica_interfaz.frame_menu       = frame_menu_principal
logica_interfaz.frame_juego      = frame_juego
logica_interfaz.frame_mover      = frame_mover
logica_interfaz.frame_tomar      = frame_tomar
logica_interfaz.frame_usar       = frame_usar
logica_interfaz.frame_donde      = frame_donde
logica_interfaz.frame_inventario = frame_inventario
logica_interfaz.frame_rescatar   = frame_rescatar
logica_interfaz.frame_visitados  = frame_visitados
logica_interfaz.frame_ruta       = frame_ruta
logica_interfaz.frame_victoria   = frame_victoria


# NAVEGACIÓN

def actualizar_estado():
    modulo_frame_estado.actualizar(texto_estado)


def abrir_juego():
    actualizar_estado()
    logica_interfaz.ir_a_jugar()


def abrir_pantalla_mover():
    actualizar_estado()
    modulo_frame_movimiento.actualizar(on_volver_callback=abrir_juego)
    logica_interfaz.ir_a_mover()


def abrir_pantalla_ruta():
    actualizar_estado()
    modulo_frame_modulos.refrescar_ruta()
    logica_interfaz.mostrar_frame(frame_ruta)


def abrir_pantalla_tomar():
    actualizar_estado()
    modulo_frame_artefactos.actualizar_tomar()
    logica_interfaz.ir_a_tomar()


def abrir_pantalla_usar():
    actualizar_estado()
    modulo_frame_artefactos.actualizar_usar()
    logica_interfaz.ir_a_usar()


def abrir_pantalla_donde():
    actualizar_estado()
    modulo_frame_artefactos.actualizar_donde()
    logica_interfaz.ir_a_donde()


def abrir_pantalla_inventario():
    actualizar_estado()
    modulo_frame_artefactos.actualizar_inventario()
    logica_interfaz.ir_a_inventario()


def abrir_pantalla_reparar():
    actualizar_estado()
    modulo_frame_sistemas.actualizar()
    logica_interfaz.mostrar_frame(frame_reparar)


def abrir_pantalla_rescatar():
    actualizar_estado()
    modulo_frame_tripulantes.actualizar()
    logica_interfaz.ir_a_rescatar()


def abrir_pantalla_visitados():
    actualizar_estado()
    modulo_frame_modulos.actualizar_visitados()
    logica_interfaz.ir_a_visitados()


def abrir_pantalla_victoria():
    modulo_frame_victoria.actualizar()
    logica_interfaz.mostrar_frame(frame_victoria)


# INICIO

logica_interfaz.inicializar_juego()
actualizar_estado()

# Registrar frame_menu en logica_interfaz
logica_interfaz.frame_menu = frame_menu_principal
logica_interfaz.mostrar_frame(frame_menu_principal)

ventana.mainloop()
