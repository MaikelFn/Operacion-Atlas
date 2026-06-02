"""
frame_victoria.py
Pantalla de victoria y guía de como ganar:
muestra el estado de victoria del jugador con el resumen completo,
o bien el plan de pendientes si aún no ha ganado.
"""

import tkinter as tk
import estilos as estilos
import logica_interfaz as logica_interfaz

frame_contenedor = None
texto_victoria = None
boton_volver = None
callback_volver = None

def construir(ventana, on_volver=None):
    """
    Entrada: ventana (tk.Tk), on_volver (callable o None).
    Salida: frame (tk.Frame).
    Funcionamiento: Construye y retorna el frame de la pantalla de victoria.
    """

    global frame_contenedor, texto_victoria, boton_volver, callback_volver

    callback_volver = on_volver

    # Frame principal
    frame_contenedor = tk.Frame(
        ventana,
        bg=estilos.COLOR_FONDO
    )
    frame_contenedor.config(width=900, height=550)
    frame_contenedor.pack_propagate(False)

    # ÁREA SCROLLABLE
    contenedor_scroll = tk.Frame(frame_contenedor, bg=estilos.COLOR_FONDO)
    contenedor_scroll.pack(fill="both", expand=True, padx=25, pady=(15, 0))

    scrollbar = tk.Scrollbar(contenedor_scroll)
    scrollbar.pack(side="right", fill="y")

    texto_victoria = tk.Text(
        contenedor_scroll,
        bg=estilos.COLOR_FONDO,
        fg=estilos.COLOR_TEXTO,
        relief="flat",
        bd=0,
        wrap="word",
        font=estilos.TIPOGRAFIA_NORMAL,
        highlightthickness=0,
        cursor="arrow",
        padx=20,
        pady=15,
        yscrollcommand=scrollbar.set,
    )
    scrollbar.config(command=texto_victoria.yview)

    # TAGS DE ESTILO
    estilos.configurar_tags_victoria(texto_victoria)
    texto_victoria.pack(
        side="left",
        fill="both",
        expand=True
    )

    # BOTÓN VOLVER
    boton_volver = tk.Button(
        frame_contenedor,
        text="Volver al Juego",
        pady=12,
        command=lambda: volver(),
        **estilos.estilo_boton(
            color_fg=estilos.COLOR_TEXTO_OSCURO
        )
    )
    boton_volver.pack(
        pady=(8, 14)
    )

    return frame_contenedor

def obtener_historial_ruta():
    """
    Entrada: Ninguna (usa logica_interfaz).
    Salida: list[str].
    Funcionamiento: Consulta el historial de ruta desde Prolog y lo retorna como lista de strings.
    """
    resultado = logica_interfaz.consultar_uno("historial_ruta(Lista)") or {}
    valor = resultado.get("Lista")
    if valor is None:
        return []
    if isinstance(valor, list):
        return [str(e) for e in valor]
    return [str(valor)]

def actualizar():
    """
    Entrada: Ninguna (usa variables globales y logica_interfaz).
    Salida: Ninguna.
    Funcionamiento: Refresca el contenido del panel de victoria consultando el estado en Prolog.
                    Muestra un resumen si se alcanzó la victoria o los objetivos pendientes.
    """

    if texto_victoria is None:
        return

    texto_victoria.config(state="normal")
    texto_victoria.delete("1.0", "end")

    exito, estado = logica_interfaz.verifica_gane()

    # VICTORIA ALCANZADA
    if exito:
        texto_victoria.insert(
            "end",
            "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n",
            "separador"
        )
        texto_victoria.insert(
            "end",
            "¡CONDICIÓN DE VICTORIA ALCANZADA!\n",
            "victoria"
        )
        texto_victoria.insert(
            "end",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n",
            "separador"
        )

        # RESUMEN FINAL
        texto_victoria.insert(
            "end",
            "» RESUMEN FINAL\n",
            "seccion"
        )

        # ARTEFACTOS
        texto_victoria.insert(
            "end",
            "\n  Artefactos Logrados:\n",
            "item"
        )
        artefactos = (estado or {}).get("artefactos") or []
        if artefactos:
            for artefacto in artefactos:
                texto_victoria.insert(
                    "end",
                    f"    ✓ {artefacto}\n",
                    "exito"
                )
        else:
            texto_victoria.insert(
                "end",
                "    (ninguno)\n",
                "item"
            )

        # MÓDULOS
        visitados = (estado or {}).get("visitados") or []
        texto_victoria.insert(
            "end",
            f"\n  Módulos Visitados: {len(visitados)}\n",
            "item"
        )
        for modulo in visitados[:10]:
            texto_victoria.insert(
                "end",
                f"    ✓ {modulo}\n",
                "exito"
            )
        if len(visitados) > 10:
            restantes = len(visitados) - 10
            texto_victoria.insert(
                "end",
                f"    ... y {restantes} más\n",
                "item"
            )

        # SISTEMAS
        texto_victoria.insert(
            "end",
            "\n  Sistemas Reparados:\n",
            "item"
        )
        sistemas = (estado or {}).get("sistemas_reparados") or []
        if sistemas:
            for sistema in sistemas:
                texto_victoria.insert(
                    "end",
                    f"    ✓ {sistema}\n",
                    "exito"
                )
        else:
            texto_victoria.insert(
                "end",
                "    (ninguno)\n",
                "item"
            )

        # TRIPULANTES
        texto_victoria.insert(
            "end",
            "\n  Tripulación Rescatada:\n",
            "item"
        )
        tripulantes = (estado or {}).get("tripulantes_rescatados") or []
        if tripulantes:
            for tripulante in tripulantes:
                texto_victoria.insert(
                    "end",
                    f"    ✓ {tripulante}\n",
                    "exito"
                )
        else:
            texto_victoria.insert(
                "end",
                "    (ninguno)\n",
                "item"
            )

        # RUTA REALIZADA
        texto_victoria.insert(
            "end",
            "\n  Ruta Realizada:\n",
            "item"
        )
        historial = obtener_historial_ruta()
        if historial:
            for evento in historial:
                texto_victoria.insert(
                    "end",
                    f"    → {evento}\n",
                    "item"
                )
        else:
            texto_victoria.insert(
                "end",
                "    (sin historial)\n",
                "item"
            )

        # MENSAJE FINAL
        texto_victoria.insert(
            "end",
            "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n",
            "separador"
        )
        texto_victoria.insert(
            "end",
            "¡Has completado la misión con éxito!\n",
            "victoria"
        )
        texto_victoria.insert(
            "end",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n",
            "separador"
        )

    # VICTORIA PENDIENTE
    else:
        sistemas_en_falla = logica_interfaz.obtener_sistemas_objetivo_en_falla()
        tripulantes_atrapados = logica_interfaz.obtener_tripulantes_objetivo_atrapados()

        texto_victoria.insert(
            "end",
            "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n",
            "separador"
        )
        texto_victoria.insert(
            "end",
            "VICTORIA PENDIENTE\n",
            "pendiente"
        )
        texto_victoria.insert(
            "end",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n",
            "separador"
        )

        # OBJETIVOS
        texto_victoria.insert(
            "end",
            "» OBJETIVOS PENDIENTES\n",
            "seccion"
        )

        # SISTEMAS EN FALLA
        if sistemas_en_falla:
            texto_victoria.insert(
                "end",
                f"\n  Sistemas en Falla: {len(sistemas_en_falla)}\n",
                "item"
            )
            for sistema_info in sistemas_en_falla:
                modulo = sistema_info.get(
                    "modulo",
                    "desconocido"
                )
                sistema = sistema_info.get(
                    "sistema",
                    "desconocido"
                )
                artefactos = sistema_info.get(
                    "artefactos",
                    []
                )
                texto_victoria.insert(
                    "end",
                    f"    ✗ {sistema} (en {modulo})\n",
                    "fallo"
                )
                if artefactos:
                    texto_victoria.insert(
                        "end",
                        f"      Requiere: {', '.join(artefactos)}\n",
                        "item"
                    )

        # TRIPULANTES ATRAPADOS
        if tripulantes_atrapados:
            texto_victoria.insert(
                "end",
                f"\n  Tripulantes Atrapados: {len(tripulantes_atrapados)}\n",
                "item"
            )
            for tripulante_info in tripulantes_atrapados:
                nombre = tripulante_info.get(
                    "nombre",
                    "desconocido"
                )
                modulo = tripulante_info.get(
                    "modulo",
                    "desconocido"
                )
                sistemas = tripulante_info.get(
                    "sistemas_necesarios",
                    []
                )
                texto_victoria.insert(
                    "end",
                    f"    ✗ {nombre} (en {modulo})\n",
                    "fallo"
                )
                if sistemas:
                    texto_victoria.insert(
                        "end",
                        f"      Necesita: {', '.join(sistemas)}\n",
                        "item"
                    )

        # VALIDACIÓN FINAL
        if not sistemas_en_falla and not tripulantes_atrapados:
            texto_victoria.insert(
                "end",
                "\n¡Verifica nuevamente para confirmar la victoria!\n",
                "pendiente"
            )

        # MENSAJE FINAL
        texto_victoria.insert(
            "end",
            "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n",
            "separador"
        )
        texto_victoria.insert(
            "end",
            "Continúa cumpliendo los objetivos...\n",
            "pendiente"
        )
        texto_victoria.insert(
            "end",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n",
            "separador"
        )

    texto_victoria.config(state="disabled")
    texto_victoria.yview_moveto(0)

def volver():
    """
    Entrada: Ninguna.
    Salida: Ninguna.
    Funcionamiento: Ejecuta el callback de volver si está definido.
    """

    if callback_volver:
        callback_volver()