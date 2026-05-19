import tkinter as tk
from pyswip import Prolog

# CONECTAR PROLOG
prolog = Prolog()

# CARGAR LOGICA
prolog.consult("logica.pl")

# VENTANA
ventana = tk.Tk()
ventana.title("Operacion Atlas")
ventana.geometry("500x400")

# TITULO
titulo = tk.Label(
    ventana,
    text="OPERACION ATLAS",
    font=("Arial", 20)
)
titulo.pack(pady=10)

# ORIGEN
tk.Label(ventana, text="Origen").pack()

entrada_origen = tk.Entry(ventana)
entrada_origen.pack()

# DESTINO
tk.Label(ventana, text="Destino").pack()

entrada_destino = tk.Entry(ventana)
entrada_destino.pack()

# RESULTADO
resultado_label = tk.Label(
    ventana,
    text="",
    font=("Arial", 14)
)

resultado_label.pack(pady=20)

# FUNCION
def verificar_movimiento():

    origen = entrada_origen.get()
    destino = entrada_destino.get()

    consulta = f"puedo_ir({origen}, {destino})"

    resultado = list(prolog.query(consulta))

    if resultado:
        resultado_label.config(
            text="SI puede ir"
        )
    else:
        resultado_label.config(
            text="NO puede ir"
        )

# BOTON
boton = tk.Button(
    ventana,
    text="Verificar Ruta",
    command=verificar_movimiento
)

boton.pack(pady=10)

# EJECUTAR
ventana.mainloop()