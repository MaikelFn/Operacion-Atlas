"""
frame_victoria.py
Pantalla de victoria y guía de como ganar:
muestra el estado de victoria del jugador con el resumen completo,
o bien el plan de pendientes si aún no ha ganado.
"""

import tkinter as tk
import estilos as estilos
import logica_interfaz as logica_interfaz


_frame_contenedor = None
_texto_victoria = None
_boton_volver = None
_boton_menu = None
_callback_volver = None
_callback_menu = None


def construir(ventana, on_volver=None, on_menu=None):
    """
    Entrada: ventana (tk.Tk), on_volver (callable o None).
    Salida: frame (tk.Frame).
    Funcionamiento: Construye y retorna el frame de la pantalla de victoria.
    """

    global _frame_contenedor
    global _texto_victoria
    global _callback_volver
    global _callback_menu
    global _boton_volver
    global _boton_menu

    _callback_volver = on_volver
    _callback_menu = on_menu

    # Frame principal
    _frame_contenedor = tk.Frame(
        ventana,
        bg=estilos.COLOR_FONDO
    )
    _frame_contenedor.config(width=900, height=550)
    _frame_contenedor.pack_propagate(False)

    # ÁREA SCROLLABLE
    contenedor_scroll = tk.Frame(_frame_contenedor, bg=estilos.COLOR_FONDO)
    contenedor_scroll.pack(fill="both", expand=True, padx=25, pady=(15, 0))

    scrollbar = tk.Scrollbar(contenedor_scroll)
    scrollbar.pack(side="right", fill="y")

    _texto_victoria = tk.Text(
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
    scrollbar.config(command=_texto_victoria.yview)

    # TAGS DE ESTILO
    estilos.configurar_tags_victoria(_texto_victoria)
    _texto_victoria.pack(
        side="left",
        fill="both",
        expand=True
    )

    # FRAME BOTONES
    frame_botones = tk.Frame(_frame_contenedor, bg=estilos.COLOR_FONDO)
    frame_botones.pack(pady=(8, 14))

    # BOTÓN VOLVER AL JUEGO
    _boton_volver = tk.Button(
        frame_botones,
        text="Volver al Juego",
        pady=12,
        command=lambda: _volver(),
        **estilos.estilo_boton(
            color_fg=estilos.COLOR_TEXTO_OSCURO
        )
    )
    _boton_volver.pack(side="left", padx=5)

    # BOTÓN VOLVER AL MENÚ
    _boton_menu = tk.Button(
        frame_botones,
        text="Volver al Menú Principal",
        pady=12,
        command=lambda: _volver_menu(),
        **estilos.estilo_boton(
            color_fg=estilos.COLOR_TEXTO_OSCURO
        )
    )
    _boton_menu.pack(side="left", padx=5)
    _boton_menu.pack_forget()  # Oculto por defecto

    return _frame_contenedor


def _obtener_historial_ruta():
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

    global _texto_victoria

    if _texto_victoria is None:
        return

    _texto_victoria.config(state="normal")
    _texto_victoria.delete("1.0", "end")

    exito, estado = logica_interfaz.verifica_gane()

    # VICTORIA ALCANZADA
    if exito:
        # Mostrar ambos botones en victoria
        _boton_volver.pack(side="left", padx=5)
        _boton_menu.pack(side="left", padx=5)
        
        _texto_victoria.insert(
            "end",
            "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n",
            "separador"
        )
        _texto_victoria.insert(
            "end",
            "¡CONDICIÓN DE VICTORIA ALCANZADA!\n",
            "victoria"
        )
        _texto_victoria.insert(
            "end",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n",
            "separador"
        )

        # RESUMEN FINAL
        _texto_victoria.insert(
            "end",
            "» RESUMEN FINAL\n",
            "seccion"
        )

        # ARTEFACTOS
        _texto_victoria.insert(
            "end",
            "\n  Artefactos Logrados:\n",
            "item"
        )
        artefactos = (estado or {}).get("artefactos") or []
        if artefactos:
            for artefacto in artefactos:
                _texto_victoria.insert(
                    "end",
                    f"    ✓ {artefacto}\n",
                    "exito"
                )
        else:
            _texto_victoria.insert(
                "end",
                "    (ninguno)\n",
                "item"
            )

        # MÓDULOS
        visitados = (estado or {}).get("visitados") or []
        _texto_victoria.insert(
            "end",
            f"\n  Módulos Visitados: {len(visitados)}\n",
            "item"
        )
        for modulo in visitados[:10]:
            _texto_victoria.insert(
                "end",
                f"    ✓ {modulo}\n",
                "exito"
            )
        if len(visitados) > 10:
            restantes = len(visitados) - 10
            _texto_victoria.insert(
                "end",
                f"    ... y {restantes} más\n",
                "item"
            )

        # SISTEMAS
        _texto_victoria.insert(
            "end",
            "\n  Sistemas Reparados:\n",
            "item"
        )
        sistemas = (estado or {}).get("sistemas_reparados") or []
        if sistemas:
            for sistema in sistemas:
                _texto_victoria.insert(
                    "end",
                    f"    ✓ {sistema}\n",
                    "exito"
                )
        else:
            _texto_victoria.insert(
                "end",
                "    (ninguno)\n",
                "item"
            )

        # TRIPULANTES
        _texto_victoria.insert(
            "end",
            "\n  Tripulación Rescatada:\n",
            "item"
        )
        tripulantes = (estado or {}).get("tripulantes_rescatados") or []
        if tripulantes:
            for tripulante in tripulantes:
                _texto_victoria.insert(
                    "end",
                    f"    ✓ {tripulante}\n",
                    "exito"
                )
        else:
            _texto_victoria.insert(
                "end",
                "    (ninguno)\n",
                "item"
            )

        # RUTA REALIZADA
        _texto_victoria.insert(
            "end",
            "\n  Ruta Realizada:\n",
            "item"
        )
        historial = _obtener_historial_ruta()
        if historial:
            for evento in historial:
                _texto_victoria.insert(
                    "end",
                    f"    → {evento}\n",
                    "item"
                )
        else:
            _texto_victoria.insert(
                "end",
                "    (sin historial)\n",
                "item"
            )

        # MENSAJE FINAL
        _texto_victoria.insert(
            "end",
            "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n",
            "separador"
        )
        _texto_victoria.insert(
            "end",
            "¡Has completado la misión con éxito!\n",
            "victoria"
        )
        _texto_victoria.insert(
            "end",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n",
            "separador"
        )

    # VICTORIA PENDIENTE
    else:
        # Mostrar solo botón volver en victoria pendiente
        _boton_volver.pack(side="left", padx=5)
        _boton_menu.pack_forget()
        
        sistemas_objetivo = logica_interfaz.obtener_sistemas_objetivo_en_falla()
        tripulantes_atrapados = logica_interfaz.obtener_tripulantes_objetivo_atrapados()
        _texto_victoria.insert(
            "end",
            "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n",
            "separador"
        )
        _texto_victoria.insert(
            "end",
            "VICTORIA PENDIENTE\n",
            "pendiente"
        )
        _texto_victoria.insert(
            "end",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n",
            "separador"
        )

        # OBJETIVOS
        _texto_victoria.insert(
            "end",
            "» OBJETIVOS PENDIENTES\n",
            "seccion"
        )

        # SISTEMAS EN FALLA
        if sistemas_objetivo:
            _texto_victoria.insert(
                "end",
                f"\n  Sistemas en Falla: {len(sistemas_objetivo)}\n",
                "item"
            )
            for sistema_info in sistemas_objetivo:
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
                _texto_victoria.insert(
                    "end",
                    f"    ✗ {sistema} (en {modulo})\n",
                    "fallo"
                )
                if artefactos:
                    _texto_victoria.insert(
                        "end",
                        f"      Requiere: {', '.join(artefactos)}\n",
                        "item"
                    )

        # TRIPULANTES ATRAPADOS
        if tripulantes_atrapados:
            _texto_victoria.insert(
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
                _texto_victoria.insert(
                    "end",
                    f"    ✗ {nombre} (en {modulo})\n",
                    "fallo"
                )
                if sistemas:
                    _texto_victoria.insert(
                        "end",
                        f"      Necesita: {', '.join(sistemas)}\n",
                        "item"
                    )

        # VALIDACIÓN FINAL
        if not sistemas_objetivo and not tripulantes_atrapados:
            _texto_victoria.insert(
                "end",
                "\n¡Verifica nuevamente para confirmar la victoria!\n",
                "pendiente"
            )

        # MENSAJE FINAL
        _texto_victoria.insert(
            "end",
            "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n",
            "separador"
        )
        _texto_victoria.insert(
            "end",
            "Continúa cumpliendo los objetivos...\n",
            "pendiente"
        )
        _texto_victoria.insert(
            "end",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n",
            "separador"
        )

    _texto_victoria.config(state="disabled")
    _texto_victoria.yview_moveto(0)


def _volver():
    """
    Entrada: Ninguna.
    Salida: Ninguna.
    Funcionamiento: Ejecuta el callback de volver si está definido.
    """

    if _callback_volver:
        _callback_volver()


def _volver_menu():
    """
    Entrada: Ninguna.
    Salida: Ninguna.
    Funcionamiento: Ejecuta el callback de volver al menú si está definido.
    """

    if _callback_menu:
        _callback_menu()