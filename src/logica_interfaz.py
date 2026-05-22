# =========================================
# LOGICA DE INTERFAZ — navegación, acciones
# =========================================

from tkinter import messagebox

try:
    from pyswip import Prolog
    prolog = Prolog()
    prolog.consult("logica.pl")
    PROLOG_OK = True
except Exception:
    PROLOG_OK = False
    prolog = None

# Referencias a widgets — se asignan desde main.py
frame_activo   = None
frame_menu     = None
frame_jugar    = None
frame_partida  = None
ubicacion_label = None
resultado_label = None
entrada_origen  = None
entrada_destino = None

# =========================================
# NAVEGACIÓN
# =========================================

def mostrar_frame(frame):
    global frame_activo
    if frame_activo:
        frame_activo.place_forget()
    frame.place(relx=0.5, rely=0.5, anchor="center")
    frame_activo = frame

def ir_a_menu():
    mostrar_frame(frame_menu)

def ir_a_jugar():
    mostrar_frame(frame_jugar)

def ir_a_partida():
    resultado_label.config(text="")
    entrada_origen.delete(0, "end")
    entrada_destino.delete(0, "end")
    actualizar_ubicacion()
    mostrar_frame(frame_partida)

def salir(ventana):
    if messagebox.askyesno("Salir", "¿Confirmar que desea salir?"):
        ventana.destroy()

def reproducir_partida():
    messagebox.showinfo("Reproducir Partida", "Funcionalidad en desarrollo.")

# =========================================
# ACCIONES DEL JUEGO
# =========================================

def actualizar_ubicacion():
    if not PROLOG_OK:
        ubicacion_label.config(text="Ubicacion actual:\n—")
        return
    try:
        res = list(prolog.query("jugador(X)"))
        if res:
            lugar = str(res[0]["X"])
            ubicacion_label.config(text=f"Ubicacion actual:\n{lugar}")
        else:
            ubicacion_label.config(text="Ubicacion actual:\nDesconocida")
    except Exception:
        ubicacion_label.config(text="Ubicacion actual:\n—")

def verificar_movimiento():
    destino = entrada_destino.get().strip()

    if not entrada_origen.get().strip() or not destino:
        resultado_label.config(text="Completa ambos campos.")
        return

    if not PROLOG_OK:
        resultado_label.config(text="Prolog no disponible.")
        return

    try:
        resultado = list(prolog.query(f"puedo_ir({destino})"))
        if resultado:
            list(prolog.query(f"mover({destino})"))
            resultado_label.config(text="SI puede ir")
            entrada_origen.delete(0, "end")
            entrada_destino.delete(0, "end")
            actualizar_ubicacion()
        else:
            resultado_label.config(text="NO puede ir")
    except Exception as e:
        resultado_label.config(text=f"Error: {e}")
