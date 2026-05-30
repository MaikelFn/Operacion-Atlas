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
import frames.frame_como_gano   as modulo_frame_como_gano


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
frame_como_gano  = modulo_frame_como_gano.construir(ventana, on_volver=lambda: abrir_juego())

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
    "como_gano":  lambda: abrir_pantalla_como_gano(),
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
logica_interfaz.frame_como_gano  = frame_como_gano


# NAVEGACIÓN

def actualizar_estado():
    """
    Entrada: Ninguna.
    Salida: Ninguna.
    Funcionamiento: Refresca el panel de estado dentro del frame de juego.
    """
    modulo_frame_estado.actualizar(texto_estado)


def abrir_juego():
    """
    Entrada: Ninguna.
    Salida: Ninguna.
    Funcionamiento: Actualiza el estado y muestra el frame principal del juego.
    """
    actualizar_estado()
    logica_interfaz.ir_a_jugar()


def abrir_pantalla_mover():
    """
    Entrada: Ninguna.
    Salida: Ninguna.
    Funcionamiento: Actualiza el estado, refresca la pantalla de movimiento
                    y navega hacia ella.
    """
    actualizar_estado()
    modulo_frame_movimiento.actualizar(on_volver_callback=abrir_juego)
    logica_interfaz.ir_a_mover()


def abrir_pantalla_ruta():
    """
    Entrada: Ninguna.
    Salida: Ninguna.
    Funcionamiento: Actualiza el estado, refresca la información de ruta
                    y muestra la pantalla de ruta.
    """
    actualizar_estado()
    modulo_frame_modulos.refrescar_ruta()
    logica_interfaz.mostrar_frame(frame_ruta)


def abrir_pantalla_tomar():
    """
    Entrada: Ninguna.
    Salida: Ninguna.
    Funcionamiento: Actualiza el estado y navega a la pantalla de tomar artefacto.
    """
    actualizar_estado()
    modulo_frame_artefactos.actualizar_tomar()
    logica_interfaz.ir_a_tomar()


def abrir_pantalla_usar():
    """
    Entrada: Ninguna.
    Salida: Ninguna.
    Funcionamiento: Actualiza el estado y navega a la pantalla de usar artefacto.
    """
    actualizar_estado()
    modulo_frame_artefactos.actualizar_usar()
    logica_interfaz.ir_a_usar()


def abrir_pantalla_donde():
    """
    Entrada: Ninguna.
    Salida: Ninguna.
    Funcionamiento: Actualiza el estado y navega a la pantalla de consultar
                    ubicación de artefacto.
    """
    actualizar_estado()
    modulo_frame_artefactos.actualizar_donde()
    logica_interfaz.ir_a_donde()


def abrir_pantalla_inventario():
    """
    Entrada: Ninguna.
    Salida: Ninguna.
    Funcionamiento: Actualiza el estado y muestra el inventario de artefactos.
    """
    actualizar_estado()
    modulo_frame_artefactos.actualizar_inventario()
    logica_interfaz.ir_a_inventario()


def abrir_pantalla_reparar():
    """
    Entrada: Ninguna.
    Salida: Ninguna.
    Funcionamiento: Actualiza el estado y muestra la pantalla de reparación
                    de sistemas.
    """
    actualizar_estado()
    modulo_frame_sistemas.actualizar()
    logica_interfaz.mostrar_frame(frame_reparar)


def abrir_pantalla_rescatar():
    """
    Entrada: Ninguna.
    Salida: Ninguna.
    Funcionamiento: Actualiza el estado y navega a la pantalla de rescate
                    de tripulantes.
    """
    actualizar_estado()
    modulo_frame_tripulantes.actualizar()
    logica_interfaz.ir_a_rescatar()


def abrir_pantalla_visitados():
    """
    Entrada: Ninguna.
    Salida: Ninguna.
    Funcionamiento: Actualiza el estado y muestra la lista de módulos visitados.
    """
    actualizar_estado()
    modulo_frame_modulos.actualizar_visitados()
    logica_interfaz.ir_a_visitados()


def abrir_pantalla_como_gano():
    """
    Entrada: Ninguna.
    Salida: Ninguna.
    Funcionamiento: Muestra la pantalla con las condiciones de victoria.
    """
    logica_interfaz.mostrar_frame(frame_como_gano)


def abrir_pantalla_victoria():
    """
    Entrada: Ninguna.
    Salida: Ninguna.
    Funcionamiento: Actualiza el estado de victoria y muestra la pantalla
                    correspondiente.
    """
    modulo_frame_victoria.actualizar()
    logica_interfaz.mostrar_frame(frame_victoria)


# INICIO

logica_interfaz.inicializar_juego()
actualizar_estado()

# Registrar frame_menu en logica_interfaz
logica_interfaz.frame_menu = frame_menu_principal
logica_interfaz.mostrar_frame(frame_menu_principal)

ventana.mainloop()