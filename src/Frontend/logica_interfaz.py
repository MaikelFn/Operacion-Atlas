from pathlib import Path

from pyswip import Prolog


# Referencias a frames
frame_activo = None
frame_menu = None
frame_juego = None
frame_mover = None
frame_tomar = None
frame_usar = None
frame_donde = None
frame_inventario = None
frame_rescatar = None
frame_visitados = None
frame_como_gano = None


# Ruta
archivo_logica = Path(__file__).resolve().parent.parent / "Backend" / "logica.pl"
_prolog = Prolog()
_prolog.consult(str(archivo_logica).replace("\\", "/"))


def obtener_prolog():
    """
    Entrada: Ninguna.
    Salida: Prolog.
    Funcionamiento: Retorna la instancia del motor Prolog utilizada por el módulo.
    """
    return _prolog


def consultar_uno(query):
    """
    Entrada: query (str).
    Salida: dict o None.
    Funcionamiento: Ejecuta una consulta Prolog y retorna el primer resultado si existe.
    """
    return next(obtener_prolog().query(query), None)

def consultar_todos(query):
    """
    Entrada: query (str).
    Salida: list[dict].
    Funcionamiento: Ejecuta una consulta Prolog y retorna todos los resultados.
    """
    return list(obtener_prolog().query(query))


def lista_a_texto(valor):
    """
    Entrada: valor (Atom, list o None).
    Salida: list[str].
    Funcionamiento: Convierte un término Prolog (átomo o lista) en una lista plana de strings.
    """
    if valor is None:
        return []
    if isinstance(valor, list):
        return [str(elemento) for elemento in valor]
    return [str(valor)]


def obtener_estado_jugador():
    """
    Entrada: Ninguna.
    Salida: dict.
    Funcionamiento: Consulta a Prolog el estado actual del jugador (ubicación, artefactos,
                    sistemas en falla, tripulantes atrapados) y lo retorna estructurado.
    """
    jugador = consultar_uno("jugador(Modulo)") or {}
    ubicacion = str(jugador.get("Modulo") or "") or "desconocido"

    descripcion = consultar_uno(f"modulo({ubicacion}, Descripcion)") or {}
    descripcion_modulo = limpiar_string(descripcion.get("Descripcion") or "") or "Sin descripcion disponible."

    artefactos = consultar_uno("que_tengo(Lista)") or {}
    artefactos_tenidos = lista_a_texto(artefactos.get("Lista"))

    usados = consultar_uno("usados(Lista)") or {}
    artefactos_usados = lista_a_texto(usados.get("Lista"))

    sistemas_en_falla = []
    for resultado in consultar_todos("sistema(Modulo, Sistema, Artefactos, fallo)"):
        sistemas_en_falla.append({
            "modulo": str(resultado.get("Modulo") or ""),
            "sistema": str(resultado.get("Sistema") or ""),
            "artefactos": lista_a_texto(resultado.get("Artefactos")),
        })

    tripulantes_atrapados = []
    for resultado in consultar_todos("tripulante(Tripulante, Modulo, Sistemas, atrapado)"):
        tripulantes_atrapados.append({
            "nombre": str(resultado.get("Tripulante") or ""),
            "modulo": str(resultado.get("Modulo") or ""),
            "sistemas_necesarios": lista_a_texto(resultado.get("Sistemas")),
        })

    return {
        "ubicacion": ubicacion,
        "descripcion_modulo": descripcion_modulo,
        "artefactos": artefactos_tenidos,
        "artefactos_usados": artefactos_usados,
        "sistemas_en_falla": sistemas_en_falla,
        "tripulantes_atrapados": tripulantes_atrapados,
    }

def obtener_tripulantes_objetivo_atrapados():
    """
    Entrada: Ninguna.
    Salida: list[dict].
    Funcionamiento: Retorna solo los tripulantes atrapados que forman parte de los objetivos
                    de victoria (condición objetivoT rescatado).
    """
    objetivos = set()
    for r in consultar_todos("objetivoT(Tripulante, rescatado)"):
        objetivos.add(str(r.get("Tripulante") or ""))

    tripulantes = []
    for r in consultar_todos("tripulante(Tripulante, Modulo, Sistemas, atrapado)"):
        nombre = str(r.get("Tripulante") or "")
        if nombre in objetivos:
            tripulantes.append({
                "nombre": nombre,
                "modulo": str(r.get("Modulo") or ""),
                "sistemas_necesarios": lista_a_texto(r.get("Sistemas")),
            })
    return tripulantes

def mostrar_frame(frame):
    """
    Entrada: frame (tk.Frame).
    Salida: Ninguna.
    Funcionamiento: Oculta el frame actual y muestra el frame indicado en el centro de la ventana.
    """
    global frame_activo
    if frame_activo:
        try:
            frame_activo.place_forget()
        except Exception:
            pass
    try:
        frame.place(relx=0.5, rely=0.5, anchor="center")
    except Exception:
        pass
    frame_activo = frame


def ir_a_menu():
    """
    Entrada: Ninguna.
    Salida: Ninguna.
    Funcionamiento: Muestra el frame del menú principal si está construido.
    """
    if frame_menu:
        mostrar_frame(frame_menu)


def ir_a_jugar():
    """
    Entrada: Ninguna.
    Salida: Ninguna.
    Funcionamiento: Muestra el frame de juego si está construido.
    """
    if frame_juego:
        mostrar_frame(frame_juego)


def ir_a_mover():
    """
    Entrada: Ninguna.
    Salida: Ninguna.
    Funcionamiento: Muestra el frame de movimiento si está construido.
    """
    if frame_mover:
        mostrar_frame(frame_mover)


def ir_a_tomar():
    """
    Entrada: Ninguna.
    Salida: Ninguna.
    Funcionamiento: Muestra el frame de tomar artefacto si está construido.
    """
    if frame_tomar:
        mostrar_frame(frame_tomar)


def ir_a_usar():
    """
    Entrada: Ninguna.
    Salida: Ninguna.
    Funcionamiento: Muestra el frame de usar artefacto si está construido.
    """
    if frame_usar:
        mostrar_frame(frame_usar)


def ir_a_donde():
    """
    Entrada: Ninguna.
    Salida: Ninguna.
    Funcionamiento: Muestra el frame de consultar ubicación de artefacto si está construido.
    """
    if frame_donde:
        mostrar_frame(frame_donde)


def ir_a_inventario():
    """
    Entrada: Ninguna.
    Salida: Ninguna.
    Funcionamiento: Muestra el frame de inventario si está construido.
    """
    if frame_inventario:
        mostrar_frame(frame_inventario)


def ir_a_rescatar():
    """
    Entrada: Ninguna.
    Salida: Ninguna.
    Funcionamiento: Muestra el frame de rescate si está construido.
    """
    if frame_rescatar:
        mostrar_frame(frame_rescatar)


def ir_a_visitados():
    """
    Entrada: Ninguna.
    Salida: Ninguna.
    Funcionamiento: Muestra el frame de módulos visitados si está construido.
    """
    if frame_visitados:
        mostrar_frame(frame_visitados)


# Acciones del juego

def tomar(artefacto):
    """
    Entrada: artefacto (str).
    Salida: bool.
    Funcionamiento: Intenta tomar el artefacto mediante Prolog; retorna True si tuvo éxito.
    """
    return consultar_uno(f"tomar({artefacto})") is not None


def usar(artefacto):
    """
    Entrada: artefacto (str).
    Salida: bool.
    Funcionamiento: Intenta usar el artefacto mediante Prolog; retorna True si tuvo éxito.
    """
    return consultar_uno(f"usar({artefacto})") is not None


def inicializar_juego():
    """
    Entrada: Ninguna.
    Salida: bool.
    Funcionamiento: Inicializa el estado del juego en Prolog; retorna True si la operación se realizó.
    """
    return consultar_uno("inicializar_juego") is not None

def reiniciar_juego():
    """
    Entrada: Ninguna.
    Salida: bool.
    Funcionamiento: Reinicia el estado del juego en Prolog; retorna True si la operación se realizó.
    """
    return consultar_uno("reiniciar_juego") is not None

def reparar(sistema):
    """
    Entrada: sistema (str).
    Salida: bool.
    Funcionamiento: Intenta reparar el sistema mediante Prolog; retorna True si tuvo éxito.
    """
    return consultar_uno(f"reparar({sistema})") is not None


def obtener_tripulantes_atrapados_modulo_actual():
    """
    Entrada: Ninguna.
    Salida: list[str].
    Funcionamiento: Retorna los nombres de los tripulantes atrapados en el módulo actual.
    """
    jugador = consultar_uno("jugador(Modulo)") or {}
    ubicacion = str(jugador.get("Modulo") or "")

    tripulantes = []
    for resultado in consultar_todos(f"tripulante(Tripulante, {ubicacion}, Sistemas, atrapado)"):
        tripulante = str(resultado.get("Tripulante") or "")
        if tripulante:
            tripulantes.append(tripulante)
    return tripulantes


def obtener_sistemas_requeridos_tripulante(tripulante):
    """
    Entrada: tripulante (str).
    Salida: list[str].
    Funcionamiento: Retorna los sistemas requeridos para rescatar al tripulante en el módulo actual.
    """
    jugador = consultar_uno("jugador(Modulo)") or {}
    ubicacion = str(jugador.get("Modulo") or "")

    resultado = consultar_uno(f"tripulante({tripulante}, {ubicacion}, Sistemas, atrapado)") or {}
    return lista_a_texto(resultado.get("Sistemas"))


def obtener_sistemas_en_fallo():
    """
    Entrada: Ninguna.
    Salida: list[str].
    Funcionamiento: Retorna los sistemas en fallo del módulo actual.
    """
    jugador = consultar_uno("jugador(Modulo)") or {}
    ubicacion = str(jugador.get("Modulo") or "")

    sistemas = []
    for resultado in consultar_todos(f"sistema({ubicacion}, Sistema, Artefactos, fallo)"):
        sistema = str(resultado.get("Sistema") or "")
        if sistema:
            sistemas.append(sistema)
    return sistemas


def obtener_artefactos_requeridos_sistema(sistema):
    """
    Entrada: sistema (str).
    Salida: list[str].
    Funcionamiento: Retorna los artefactos necesarios para reparar el sistema en el módulo actual.
    """
    jugador = consultar_uno("jugador(Modulo)") or {}
    ubicacion = str(jugador.get("Modulo") or "")

    resultado = consultar_uno(f"sistema({ubicacion},{sistema},Artefactos, fallo)") or {}
    return lista_a_texto(resultado.get("Artefactos"))


def rescatar(tripulante):
    """
    Entrada: tripulante (str).
    Salida: bool.
    Funcionamiento: Intenta rescatar al tripulante mediante Prolog; retorna True si tuvo éxito.
    """
    return consultar_uno(f"rescatar({tripulante})") is not None


def puedo_ir(destino):
    """
    Entrada: destino (str).
    Salida: bool.
    Funcionamiento: Verifica si el jugador puede moverse al módulo destino desde la ubicación actual.
    """
    return consultar_uno(f"puedo_ir({destino})") is not None


def mover(modulo):
    """
    Entrada: modulo (str).
    Salida: bool.
    Funcionamiento: Intenta mover al jugador al módulo indicado; retorna True si tuvo éxito.
    """
    return consultar_uno(f"mover({modulo})") is not None


def obtener_destinos_disponibles():
    """
    Entrada: Ninguna.
    Salida: list[str].
    Funcionamiento: Retorna los módulos a los que el jugador puede moverse desde la ubicación actual.
    """
    destinos = []
    for resultado in consultar_todos("modulo(Destino, _)"):
        destino = str(resultado.get("Destino") or "")
        if destino and puedo_ir(destino):
            destinos.append(destino)
    return destinos


def donde_esta(artefacto):
    """
    Entrada: artefacto (str).
    Salida: str.
    Funcionamiento: Retorna el módulo donde se encuentra actualmente el artefacto.
    """
    resultado = consultar_uno(f"donde_esta({artefacto}, Modulo)") or {}
    return str(resultado.get("Modulo") or "")


def que_tengo():
    """
    Entrada: Ninguna.
    Salida: list[str].
    Funcionamiento: Retorna la lista de artefactos que el jugador tiene en el inventario.
    """
    resultado = consultar_uno("que_tengo(Lista)") or {}
    return lista_a_texto(resultado.get("Lista"))


def usados():
    """
    Entrada: Ninguna.
    Salida: list[str].
    Funcionamiento: Retorna la lista de artefactos que ya han sido usados.
    """
    resultado = consultar_uno("usados(Lista)") or {}
    return lista_a_texto(resultado.get("Lista"))


def obtener_artefactos_usables():
    """
    Entrada: Ninguna.
    Salida: list[str].
    Funcionamiento: Retorna los artefactos del inventario que aún no han sido usados.
    """
    inventario = que_tengo()
    usados_actuales = set(usados())
    return [artefacto for artefacto in inventario if artefacto not in usados_actuales]


def obtener_artefactos_disponibles():
    """
    Entrada: Ninguna.
    Salida: list[str].
    Funcionamiento: Retorna los artefactos presentes en el módulo actual que el jugador aún no posee.
    """
    jugador = consultar_uno("jugador(Modulo)") or {}
    ubicacion = str(jugador.get("Modulo") or "")

    logrados = set(que_tengo())
    artefactos = []
    for resultado in consultar_todos(f"artefacto(Artefacto, {ubicacion})"):
        artefacto = str(resultado.get("Artefacto") or "")
        if artefacto and artefacto not in logrados:
            artefactos.append(artefacto)
    return artefactos


def obtener_artefactos_faltantes():
    """
    Entrada: Ninguna.
    Salida: list[str].
    Funcionamiento: Retorna todos los artefactos del juego que el jugador no tiene en el inventario.
    """
    inventario = set(que_tengo())
    artefactos = []
    for resultado in consultar_todos("artefacto(Artefacto, Modulo)"):
        artefacto = str(resultado.get("Artefacto") or "")
        if artefacto and artefacto not in inventario:
            artefactos.append(artefacto)
    return artefactos


def obtener_inventario_artefactos():
    """
    Entrada: Ninguna.
    Salida: list[dict].
    Funcionamiento: Retorna una lista con detalles de cada artefacto del inventario
                    (nombre, si fue usado y módulo donde se obtuvo).
    """
    inventario = que_tengo()
    usados_actuales = set(usados())
    artefactos = []

    for artefacto in inventario:
        artefactos.append({
            "artefacto": artefacto,
            "usado": artefacto in usados_actuales,
            "modulo": donde_esta(artefacto),
        })

    return artefactos


def modulos_visitados():
    """
    Entrada: Ninguna.
    Salida: list[str].
    Funcionamiento: Retorna la lista de módulos visitados por el jugador.
    """
    resultado = consultar_uno("modulos_visitados(Lista)") or {}
    return lista_a_texto(resultado.get("Lista"))


def ruta(inicio, fin):
    """
    Entrada: inicio (str), fin (str).
    Salida: list[str].
    Funcionamiento: Calcula y retorna la ruta más corta entre dos módulos.
    """
    if not inicio or not fin:
        return []
    resultado = consultar_uno(f"ruta({inicio},{fin},Ruta)") or {}
    ruta_prolog = resultado.get("Ruta") if resultado else None
    return lista_a_texto(ruta_prolog)


def obtener_modulos():
    """
    Entrada: Ninguna.
    Salida: list[str].
    Funcionamiento: Retorna la lista de todos los módulos del juego.
    """
    modulos = []
    for resultado in consultar_todos("modulo(Modulo, _)"):
        modulo = str(resultado.get("Modulo") or "")
        if modulo:
            modulos.append(modulo)
    return modulos


def obtener_descripcion_modulo(modulo):
    """
    Entrada: modulo (str).
    Salida: str.
    Funcionamiento: Retorna la descripción textual del módulo indicado.
    """
    resultado = consultar_uno(f"modulo({modulo}, Descripcion)") or {}
    return str(resultado.get("Descripcion") or "")

def obtener_enlaces():
    """
    Entrada: Ninguna.
    Salida: list[tuple[str, str]].
    Funcionamiento: Retorna todos los enlaces entre módulos como pares ordenados.
    """
    enlaces = []
    vistos = set()
    for r in consultar_todos("enlace(A, B)"):
        a = str(r.get("A") or "")
        b = str(r.get("B") or "")
        if a and b:
            clave = tuple(sorted([a, b]))
            if clave not in vistos:
                vistos.add(clave)
                enlaces.append((a, b))
    return enlaces

def como_gano():
    """
    Entrada: Ninguna.
    Salida: list[list[dict]].
    Funcionamiento: Consulta posibles planes para ganar; retorna una lista de planes,
                    cada uno compuesto por pasos con acción y argumento.
    """
    resultado = consultar_uno("como_gano(Planes)") or {}
    planes_prolog = resultado.get("Planes") or []

    planes = []
    for plan_prolog in planes_prolog:
        pasos = []
        pasos_lista = plan_prolog if isinstance(plan_prolog, list) else [plan_prolog]
        for paso in pasos_lista:
            paso_str = str(paso)
            # Cada paso es un termino como ir(modulo), tomar(art), etc.
            if "(" in paso_str and paso_str.endswith(")"):
                accion = paso_str[:paso_str.index("(")]
                argumento = paso_str[paso_str.index("(")+1:-1]
            else:
                accion = paso_str
                argumento = ""
            pasos.append({"accion": accion, "argumento": argumento})
        planes.append(pasos)

    return planes

def verifica_gane():
    """
    Entrada: Ninguna.
    Salida: tuple (bool, dict o None).
    Funcionamiento: Verifica si se alcanzó la victoria. Retorna True y un resumen del estado final
                    si se cumple, o False y None en caso contrario.
    """
    resultado = consultar_uno("verifica_gane")
    
    if resultado is not None:
        # Victoria alcanzada - recopilar estado final
        artefactos_logrados = que_tengo()
        visitados = modulos_visitados()
        
        sistemas_rep = []
        for resultado_sis in consultar_todos("sistemas_reparados(Lista), member(X, Lista)"):
            sistema = str(resultado_sis.get("X") or "")
            if sistema:
                sistemas_rep.append(sistema)
        
        tripulantes_resc = []
        for resultado_trip in consultar_todos("tripulantes_rescatados(Lista), member(X, Lista)"):
            tripulante = str(resultado_trip.get("X") or "")
            if tripulante:
                tripulantes_resc.append(tripulante)
        
        return True, {
            "artefactos": artefactos_logrados,
            "visitados": visitados,
            "sistemas_reparados": sistemas_rep,
            "tripulantes_rescatados": tripulantes_resc,
        }
    
    return False, None

def obtener_modulo_inicial():
    """
    Entrada: Ninguna.
    Salida: str.
    Funcionamiento: Retorna el modulo inicial del juego consultando el ultimo
                    elemento de la lista de visitados, que fue el primero registrado.
    """
    resultado = consultar_uno("modulos_visitados(Lista)") or {}
    lista = resultado.get("Lista") or []
    if isinstance(lista, list) and len(lista) > 0:
        return str(lista[-1])
    jugador = consultar_uno("jugador(Modulo)") or {}
    return str(jugador.get("Modulo") or "")


def limpiar_string(valor):
    """
    Entrada: valor (str o bytes-string de Prolog).
    Salida: str limpio.
    Funcionamiento: Elimina el prefijo b'...' que Prolog retorna en strings con comillas.
    """
    t = str(valor)
    if t.startswith("b'") and t.endswith("'"):
        return t[2:-1]
    if t.startswith('b"') and t.endswith('"'):
        return t[2:-1]
    return t


def guardar_partida():
    """
    Entrada: Ninguna.
    Salida: bool.
    Funcionamiento: Guarda la partida actual en el archivo DataBase/Partida.txt
                    mediante una consulta a Prolog.
    """
    return consultar_uno("guardar_repeticion") is not None


def reproducir_partida():
    """
    Entrada: Ninguna.
    Salida: bool.
    Funcionamiento: Reproduce la partida guardada desde el archivo DataBase/Partida.txt
                    mediante una consulta a Prolog.
    """
    return consultar_uno("reproducir_repeticion") is not None


__all__ = [
    "mostrar_frame",
    "ir_a_menu",
    "ir_a_jugar",
    "ir_a_mover",
    "ir_a_tomar",
    "ir_a_usar",
    "ir_a_donde",
    "ir_a_inventario",
    "obtener_estado_jugador",
    "obtener_destinos_disponibles",
    "obtener_artefactos_disponibles",
    "obtener_artefactos_faltantes",
    "obtener_inventario_artefactos",
    "obtener_artefactos_usables",
    "puedo_ir",
    "mover",
    "tomar",
    "usar",
    "ruta",
    "obtener_modulos",
    "obtener_enlaces",
    "como_gano",
    "verifica_gane",
    "obtener_modulo_inicial",
    "limpiar_string",
]