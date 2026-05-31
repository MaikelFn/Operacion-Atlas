% =========================================
% ESTADO DINAMICO DEL JUEGO
% =========================================
:- dynamic jugador/1.
:- dynamic artefactosLogrados/1.
:- dynamic sistema/4.
:- dynamic tripulante/4.
:- dynamic visitados/1.
:- dynamic usados/1.
:- dynamic tripulantes_rescatados/1.
:- dynamic sistemas_reparados/1.
:- dynamic ruta_historial/1.
:- dynamic comandos/1.
:- dynamic objetivoS/2.
:- dynamic objetivoT/2.
:- consult('../Backend/conocimiento.pl').
% =========================================
% ESTADO INICIAL
% =========================================

visitados([]).
usados([]).
tripulantes_rescatados([]).
sistemas_reparados([]).
ruta_historial([]).
comandos([]).

% Nombre: inicializar_juego/0
% Entrada: Ninguna
% Salida: Registra la visita del modulo inicial del jugador
% Funcion: Inicializa el estado de recorrido del juego a partir del modulo actual
% Autor: Maikel Flores
inicializar_juego :-
    jugador(ModuloInicial),
    registrar_visita(ModuloInicial).

% Nombre: reiniciar_juego/0
% Entrada: Ninguna
% Salida: Deja el juego en el estado inicial (como recién comenzado)
reiniciar_juego :-
    % 1. Limpiar todos los hechos dinámicos
    retractall(jugador(_)),
    retractall(artefactosLogrados(_)),
    retractall(sistema(_,_,_,_)),
    retractall(tripulante(_,_,_,_)),
    retractall(visitados(_)),
    retractall(usados(_)),
    retractall(tripulantes_rescatados(_)),
    retractall(sistemas_reparados(_)),
    retractall(ruta_historial(_)),
    retractall(comandos(_)),

    % 2. Recargar el archivo de conocimiento (hechos estáticos)
    consult('../Backend/conocimiento.pl'),

    % 3. Reafirmar los hechos de progreso (vacíos)
    assertz(visitados([])),
    assertz(usados([])),
    assertz(tripulantes_rescatados([])),
    assertz(sistemas_reparados([])),
    assertz(ruta_historial([])),
    assertz(comandos([])),

    % 4. Registrar el modulo inicial como visitado
    inicializar_juego.

% =========================================
% CONECTIVIDAD ENTRE MODULOS
% =========================================

% Nombre: esta_conectado/2
% Entrada: Dos modulos
% Salida: Verdadero si existe conexion entre ambos modulos
% Funcion: Determina si hay enlace directo entre dos modulos (bidireccional)
% Autor: Maikel Flores
esta_conectado(X, Y) :-
    enlace(X, Y).
esta_conectado(X, Y) :-
    enlace(Y, X).

% =========================================
% RUTAS ENTRE MODULOS
% =========================================

% Nombre: ruta/3
% Entrada: Inicio, Destino
% Salida: Ruta (lista de modulos)
% Funcion: Calcula un camino simple entre Inicio y Destino evitando ciclos
% Autor: Maikel Flores
ruta(Inicio, Destino, Ruta) :-
    ruta_aux(Inicio, Destino, [Inicio], Ruta).

% Nombre: ruta_aux/4
% Entrada: Actual, Destino, Visitados
% Salida: Ruta (lista)
% Funcion: Auxiliar recursivo para busqueda de rutas
% Autor: Maikel Flores
ruta_aux(Destino, Destino, Visitados, Visitados).
ruta_aux(Actual, Destino, Visitados, Ruta) :-
    esta_conectado(Actual, Siguiente),
    \+ member(Siguiente, Visitados),
    append(Visitados, [Siguiente], Visitados2),
    ruta_aux(Siguiente, Destino, Visitados2, Ruta).

% =========================================
% ARTEFACTOS LOGRADOS Y USO DE ARTEFACTOS
% =========================================

% Nombre: tiene/1
% Entrada: Artefacto
% Salida: Verdadero si el jugador posee el artefacto
% Funcion: Consulta la lista de artefactos obtenidos por el jugador
% Autor: Maikel Flores
tiene(Artefacto) :-
    artefactosLogrados(Lista),
    member(Artefacto, Lista).

% Nombre: uso/1
% Entrada: Artefacto
% Salida: Verdadero si el artefacto fue usado
% Funcion: Consulta la lista de artefactos consumidos
% Autor: Maikel Flores
uso(Artefacto) :-
    usados(Lista),
    member(Artefacto, Lista).

% Nombre: usar/1
% Entrada: Artefacto
% Salida: Registra el artefacto como usado
% Funcion: Marca un artefacto disponible como consumido
% Autor: Maikel Flores
usar(Artefacto) :-
    tiene(Artefacto),
    \+ uso(Artefacto),
    usados(Lista),
    retract(usados(Lista)),
    assertz(usados([Artefacto | Lista])),
    registrar_comando(usar(Artefacto)),
    agregar_a_ruta(usaste(Artefacto)).

% =========================================
% VALIDACIONES DE MOVIMIENTO
% =========================================

% Nombre: cumple_requisito_artefacto/1
% Entrada: Modulo
% Salida: Verdadero si se cumple requisito de artefacto o no existe requisito
% Funcion: Verifica si el modulo tiene el artefacto requerido o no tiene requisito
% Autor: Maikel Flores
cumple_requisito_artefacto(Modulo) :-
    necesita(Modulo, Artefacto),
    uso(Artefacto).
cumple_requisito_artefacto(Modulo) :-
    \+ necesita(Modulo, _).

% Nombre: fue_visitado/1
% Entrada: Modulo
% Salida: Verdadero si el modulo ya fue visitado
% Funcion: Consulta el historial de modulos recorridos
% Autor: Maikel Flores
fue_visitado(Modulo) :-
    visitados(Lista),
    member(Modulo, Lista).

% Nombre: esta_reparado/1
% Entrada: Sistema
% Salida: Verdadero si el sistema esta restaurado
% Funcion: Revisa el estado de un sistema en la base dinamica
% Autor: Maikel Flores
esta_reparado(Sistema) :-
    sistema(_, Sistema, _, restaurado).

% Nombre: cumple_paso_previo/1
% Entrada: Modulo
% Salida: Verdadero si el paso previo fue cumplido o no existe
% Funcion: Valida dependencia de avance entre modulos
% Autor: Maikel Flores
cumple_paso_previo(Modulo) :-
    pasoPrevio(Modulo, Requerido),
    fue_visitado(Requerido).
cumple_paso_previo(Modulo) :-
    \+ pasoPrevio(Modulo, _).

% Nombre: cumple_requisito_estado/1
% Entrada: Modulo
% Salida: Verdadero si el sistema asociado al modulo esta restaurado o no existe requisito
% Funcion: Verifica condicion de estado requerida por el modulo
% Autor: Maikel Flores
cumple_requisito_estado(Modulo) :-
    necesitaEstado(Modulo, Sistema, restaurado),
    esta_reparado(Sistema).
cumple_requisito_estado(Modulo) :-
    \+ necesitaEstado(Modulo, _, _).

% =========================================
% REGISTRO DE ESTADOS
% =========================================

% Nombre: registrar_comando/1
% Entrada: Comando (término Prolog, ej. mover(laboratorio))
% Salida: Agrega el comando al final de la lista de comandos
% Autor: Maikel Flores
registrar_comando(Comando) :-
    comandos(Lista),
    retract(comandos(Lista)),
    append(Lista, [Comando], ListaNueva),
    assertz(comandos(ListaNueva)).

% Nombre: guardar_repeticion/0
% Entrada: Nada
% Salida: Guarda la lista de comandos en el archivo
% Autor: Maikel Flores
guardar_repeticion :-
    comandos(ListaComandos),
    open('../DataBase/Partida.txt', write, Stream),
    write(Stream, ListaComandos),
    write(Stream, '.'),
    close(Stream).

% Nombre: reproducir_repeticion/0
% Entrada: Nada
% Salida: Ejecuta los comandos en orden para reproducir la partida
% Autor: Maikel Flores
reproducir_repeticion:-
    reiniciar_juego,
    open('../DataBase/Partida.txt', read, Stream),
    read(Stream, ListaComandos),
    close(Stream),
    maplist(ejecutar_comando, ListaComandos).
% Nombre: ejecutar_comando/1
% Entrada: Comando (término Prolog)
% Salida: Ejecuta el comando dado
% Autor: Maikel Flores
ejecutar_comando(Comando) :- call(Comando).

% Nombre: registrar_visita/1
% Entrada: Modulo
% Salida: Registra el modulo como visitado si no estaba
% Funcion: Inserta el modulo al inicio del historial de visita
% Autor: Maikel Flores
registrar_visita(Modulo) :-
    visitados(Lista),
    member(Modulo, Lista),
    !.
registrar_visita(Modulo) :-
    visitados(Lista),
    retract(visitados(Lista)),
    assertz(visitados([Modulo | Lista])).

% Nombre: agregar_a_ruta/1
% Entrada: Evento
% Salida: Registra el evento al final del historial de ruta
% Funcion: Guarda en orden cronologico las acciones relevantes del jugador
% Autor: Tayler Wynta
agregar_a_ruta(Evento) :-
    ruta_historial(Lista),
    retract(ruta_historial(Lista)),
    append(Lista, [Evento], ListaNueva),
    assertz(ruta_historial(ListaNueva)).

% Nombre: registrar_rescate/1
% Entrada: Tripulante
% Salida: Registra el tripulante como rescatado si no estaba
% Funcion: Evita duplicados en el historial de rescates
% Autor: Maikel Flores
registrar_rescate(Tripulante) :-
    tripulantes_rescatados(Lista),
    member(Tripulante, Lista),
    !.
registrar_rescate(Tripulante) :-
    tripulantes_rescatados(Lista),
    retract(tripulantes_rescatados(Lista)),
    assertz(tripulantes_rescatados([Tripulante | Lista])).

% Nombre: registrar_reparacion/1
% Entrada: Sistema
% Salida: Registra el sistema como reparado si no estaba
% Funcion: Evita duplicados en el historial de sistemas restaurados
% Autor: Maikel Flores
registrar_reparacion(Sistema) :-
    sistemas_reparados(Lista),
    member(Sistema, Lista),
    !.
registrar_reparacion(Sistema) :-
    sistemas_reparados(Lista),
    retract(sistemas_reparados(Lista)),
    assertz(sistemas_reparados([Sistema | Lista])).

% =========================================
% MOVIMIENTO
% =========================================

% Nombre: puedo_ir/1
% Entrada: Destino
% Salida: Verdadero si el jugador puede moverse a ese modulo
% Funcion: Valida conexion, requisitos de artefacto, paso previo y estado
% Autor: Maikel Flores
puedo_ir(Destino) :-
    jugador(Origen),
    Origen \= Destino,
    modulo(Destino, _),
    esta_conectado(Origen, Destino),
    cumple_requisito_artefacto(Destino),
    cumple_paso_previo(Destino),
    cumple_requisito_estado(Destino).

% Nombre: mover/1
% Entrada: Destino
% Salida: Actualiza la posicion del jugador y registra la visita
% Funcion: Ejecuta el traslado del jugador al modulo destino
% Autor: Maikel Flores
mover(Destino) :-
    puedo_ir(Destino),
    jugador(Actual),
    retract(jugador(Actual)),
    assertz(jugador(Destino)),
    registrar_visita(Destino),
    registrar_comando(mover(Destino)),
    agregar_a_ruta(fuiste_a(Destino)).

% =========================================
% ARTEFACTOS
% =========================================

% Nombre: tomar/1
% Entrada: Artefacto
% Salida: Agrega el artefacto a la lista de logrados si esta en el modulo actual
% Funcion: Permite recoger un artefacto disponible en el modulo del jugador
% Autor: Maikel Flores
tomar(Artefacto) :-
    jugador(ModuloActual),
    artefacto(Artefacto, ModuloActual),
    artefactosLogrados(Lista),
    \+ member(Artefacto, Lista),
    retract(artefactosLogrados(Lista)),
    assertz(artefactosLogrados([Artefacto | Lista])),
    registrar_comando(tomar(Artefacto)),
    agregar_a_ruta(tomaste(Artefacto)).

% =========================================
% REPARACION DE SISTEMAS
% =========================================

% Nombre: tiene_todos/1
% Entrada: Lista de artefactos
% Salida: Verdadero si todos los artefactos de la lista fueron usados
% Funcion: Comprueba recursivamente que cada elemento de la lista este en uso
% Autor: Maikel Flores
tiene_todos([]).
tiene_todos([Cabeza | Cola]) :-
    uso(Cabeza),
    tiene_todos(Cola).

% Nombre: reparar/1
% Entrada: Sistema
% Salida: Cambia el estado del sistema a restaurado y registra la reparacion
% Funcion: Repara el sistema actual si el jugador posee todos los artefactos necesarios
% Autor: Maikel Flores
reparar(Sistema) :-
    jugador(ModuloActual),
    sistema(
        ModuloActual,
        Sistema,
        Artefactos,
        fallo
    ),
    tiene_todos(Artefactos),
    retract(
        sistema(
            ModuloActual,
            Sistema,
            Artefactos,
            fallo
        )
    ),
    assertz(
        sistema(
            ModuloActual,
            Sistema,
            Artefactos,
            restaurado
        )
    ),
    registrar_reparacion(Sistema),
    registrar_comando(reparar(Sistema)),
    agregar_a_ruta(reparaste(Sistema)).

% =========================================
% RESCATE DE TRIPULANTES
% =========================================

% Nombre: esta_rescatado/1
% Entrada: Tripulante
% Salida: Verdadero si el tripulante se encuentra rescatado
% Funcion: Consulta el estado de rescate de un tripulante
% Autor: Maikel Flores
esta_rescatado(Tripulante) :-
    tripulante(
        Tripulante,_,_,rescatado).

% Nombre: sistemas_funcionando/1
% Entrada: Lista de sistemas
% Salida: Verdadero si todos los sistemas de la lista estan reparados
% Funcion: Verifica recursivamente que cada sistema requerido ya funcione
% Autor: Maikel Flores
sistemas_funcionando([]).
sistemas_funcionando([Cabeza | Cola]) :-
    esta_reparado(Cabeza),
    sistemas_funcionando(Cola).

% Nombre: rescatar/1
% Entrada: Tripulante
% Salida: Cambia el estado del tripulante a rescatado y registra el rescate
% Funcion: Libera un tripulante cuando el jugador cumple las condiciones requeridas
% Autor: Maikel Flores
rescatar(Tripulante) :-
    jugador(ModuloActual),
    tripulante(
        Tripulante,
        ModuloActual,
        SistemasNecesarios,
        atrapado
    ),
    sistemas_funcionando(SistemasNecesarios),
    retract(
        tripulante(
            Tripulante,
            ModuloActual,
            SistemasNecesarios,
            atrapado
        )
    ),
    assertz(
        tripulante(
            Tripulante,
            ModuloActual,
            SistemasNecesarios,
            rescatado
        )
    ),
    registrar_rescate(Tripulante),
    registrar_comando(rescatar(Tripulante)),
    agregar_a_ruta(rescataste(Tripulante)).

% =========================================
% CONSULTAS
% =========================================

% Nombre: donde_esta/2
% Entrada: Artefacto
% Salida: Modulo donde se encuentra el artefacto
% Funcion: Localiza el modulo asociado a un artefacto existente
% Autor: Maikel Flores
donde_esta(Artefacto, Modulo) :-
    artefacto(Artefacto, Modulo).

% Nombre: que_tengo/1
% Entrada: Ninguna (variable de salida)
% Salida: Lista de artefactos logrados
% Funcion: Devuelve el inventario de artefactos obtenidos por el jugador
% Autor: Maikel Flores
que_tengo(Lista) :-
    artefactosLogrados(Lista).

% Nombre: modulos_visitados/1
% Entrada: Ninguna (variable de salida)
% Salida: Lista de modulos visitados
% Funcion: Expone el historial de modulos recorridos durante la partida
% Autor: Maikel Flores
modulos_visitados(Lista) :-
    visitados(Lista).

% Nombre: historial_ruta/1
% Entrada: Ninguna (variable de salida)
% Salida: Lista de eventos registrados en la ruta del jugador
% Funcion: Expone el historial cronologico de acciones registradas
% Autor: Tayler Wynta
historial_ruta(Lista) :-
    ruta_historial(Lista).

% =========================================
% CONDICIONES DE VICTORIA
% =========================================

% Nombre: cumple_objetivos_sistemas/0
% Entrada: Ninguna
% Salida: Verdadero si todos los objetivos de sistemas estan restaurados (o no hay objetivos)
% Funcion: Comprueba que cada objetivoS/2 requerido termine en estado restaurado.
% Autor: Maikel Flores
cumple_objetivos_sistemas :-
    findall(S, objetivoS(S, restaurado), Sistemas),
    (   Sistemas = []
    ;   forall(member(S, Sistemas), esta_reparado(S))
    ).

% Nombre: cumple_objetivos_tripulantes/0
% Entrada: Ninguna
% Salida: Verdadero si todos los objetivos de tripulantes estan rescatados (o no hay objetivos)
% Funcion: Comprueba que cada objetivoT/2 requerido termine en estado rescatado.
% Autor: Maikel Flores
cumple_objetivos_tripulantes :-
    findall(T, objetivoT(T, rescatado), Tripulantes),
    (   Tripulantes = []
    ;   forall(member(T, Tripulantes), esta_rescatado(T))
    ).

% Nombre: gano/0
% Entrada: Ninguna
% Salida: Verdadero si se cumplieron todos los objetivos (o no hay ninguno)
% Funcion: Determina la condicion de victoria completa del juego.
% Autor: Maikel Flores
gano :-
    (   \+ objetivoS(_, restaurado),
        \+ objetivoT(_, rescatado);
        cumple_objetivos_sistemas,
        cumple_objetivos_tripulantes
    ).

% =========================================
% PLANIFICADOR DE SOLUCION
% =========================================

% Nombre: simulacion_posee_artefacto/2
% Entrada: Artefacto, Lista de artefactos usados
% Salida: Verdadero si el artefacto esta en la lista de usados
% Funcion: Verifica en estado simulado si el jugador posee un artefacto
% Autor: Tayler Wynta
simulacion_posee_artefacto(Artefacto, ArtefactosUsados) :- member(Artefacto, ArtefactosUsados).

% Nombre: simulacion_puede_entrar/4
% Entrada: Modulo, Artefactos usados, Sistemas reparados, Modulos visitados
% Salida: Verdadero si se cumplen todas las restricciones de entrada
% Funcion: Verifica las 3 restricciones de entrada en estado simulado
% Autor: Tayler Wynta
simulacion_puede_entrar(Modulo, ArtefactosUsados, SistemasReparados, ModulosVisitados) :-
    (   necesita(Modulo, ArtefactoRequerido)
    ->  member(ArtefactoRequerido, ArtefactosUsados)
    ;   true
    ),
    (   necesitaEstado(Modulo, SistemaRequerido, restaurado)
    ->  member(SistemaRequerido, SistemasReparados)
    ;   true
    ),
    (   pasoPrevio(Modulo, ModuloRequerido)
    ->  member(ModuloRequerido, ModulosVisitados)
    ;   true
    ).

% Nombre: pasos_obtener_artefacto/4
% Entrada: Artefacto, Estado inicial, resultado, Pasos generados
% Salida: Genera pasos para obtener y usar el artefacto
% Funcion: Calcula los pasos minimos para que un artefacto este disponible
% Autor: Tayler Wynta
pasos_obtener_artefacto(Art, estado(Mod, Usados, SisRep, Vis),
                             estado(Mod, Usados, SisRep, Vis), []) :-
    member(Art, Usados), !.

pasos_obtener_artefacto(Art, Estado0, EstadoFinal, Pasos) :-
    \+ ( Estado0 = estado(_, Usados0, _, _), member(Art, Usados0) ),
    artefacto(Art, ModArt),
    pasos_entrar_modulo(ModArt, Estado0, Estado1, PasosEntrada),
    Estado1 = estado(ModArt, Usados1, SisRep1, Vis1),
    append(Usados1, [Art], Usados2),
    EstadoFinal = estado(ModArt, Usados2, SisRep1, Vis1),
    append(PasosEntrada, [tomar(Art), usar(Art)], Pasos).

% Nombre: pasos_entrar_modulo/4
% Entrada: Modulo destino, Estado inicial, resultado, Pasos generados
% Salida: Genera pasos para navegar hacia un modulo
% Funcion: Navega desde el modulo actual hasta destino respetando restricciones
% Autor: Tayler Wynta
pasos_entrar_modulo(Destino, estado(Destino, ArtefactosUsados, SistemasReparados, ModulosVisitados),
                              estado(Destino, ArtefactosUsados, SistemasReparados, ModulosVisitados), []) :- !.

pasos_entrar_modulo(Destino, Estado0, EstadoFinal, Pasos) :-
    Estado0 = estado(ModActual, _, _, _),
    ModActual \= Destino,
    ruta(ModActual, Destino, RutaCompleta),
    RutaCompleta = [_|NodosSiguientes],
    pasos_recorrer_nodos(NodosSiguientes, Estado0, EstadoFinal, Pasos).

% Nombre: pasos_recorrer_nodos/4
% Entrada: Lista de nodos, Estado inicial, resultado, Pasos generados
% Salida: Genera pasos para recorrer una secuencia de nodos
% Funcion: Itera nodo a nodo resolviendo prerrequisitos en cada movimiento
% Autor: Tayler Wynta
pasos_recorrer_nodos([], EstadoActual, EstadoActual, []).
pasos_recorrer_nodos([Nodo|Resto], Estado0, EstadoFinal, Pasos) :-
    Estado0 = estado(_, Usados0, _, _),
    (   necesita(Nodo, ArtReq), \+ member(ArtReq, Usados0)
    ->  pasos_obtener_artefacto(ArtReq, Estado0, EstadoMedio, PasosArt)
    ;   EstadoMedio = Estado0, PasosArt = []
    ),
    EstadoMedio = estado(ModActualMedio, UsadosMedio, SisRepMedio, VisMedio),
    simulacion_puede_entrar(Nodo, UsadosMedio, SisRepMedio, VisMedio),
    (   ModActualMedio \= Nodo
    ->  ruta(ModActualMedio, Nodo, RutaANodo),
        RutaANodo = [_|SaltosANodo],
        pasos_saltos_directos(SaltosANodo, EstadoMedio, EstadoEnNodo, PasosSaltos)
    ;   EstadoEnNodo = EstadoMedio, PasosSaltos = []
    ),
    EstadoEnNodo = estado(_, UsadosEnNodo, SisRepEnNodo, VisEnNodo),
    (member(Nodo, VisEnNodo) -> VisSig = VisEnNodo ; VisSig = [Nodo|VisEnNodo]),
    EstadoTras = estado(Nodo, UsadosEnNodo, SisRepEnNodo, VisSig),
    pasos_recorrer_nodos(Resto, EstadoTras, EstadoFinal, PasosResto),
    append(PasosArt, PasosSaltos, PasosHastaNodo),
    append(PasosHastaNodo, PasosResto, Pasos).

% Nombre: pasos_saltos_directos/4
% Entrada: Lista de nodos, Estado inicial, resultado, Pasos generados
% Salida: Genera pasos de movimiento directo entre nodos
% Funcion: Genera ir/1 para cada salto de una ruta calculada
% Autor: Tayler Wynta
pasos_saltos_directos([], EstadoActual, EstadoActual, []).
pasos_saltos_directos([Nodo|NodosRestantes], estado(_, ArtefactosUsados, SistemasReparados, ModulosVisitados), EstadoFinal, [ir(Nodo)|PasosRestantes]) :-
    (member(Nodo, ModulosVisitados) -> ModulosVisitadosActualizados = ModulosVisitados ; ModulosVisitadosActualizados = [Nodo|ModulosVisitados]),
    pasos_saltos_directos(NodosRestantes, estado(Nodo, ArtefactosUsados, SistemasReparados, ModulosVisitadosActualizados), EstadoFinal, PasosRestantes).

% Nombre: pasos_reparar_sistema/4
% Entrada: Sistema, Estado inicial, resultado, Pasos generados
% Salida: Genera pasos para reparar un sistema completo
% Funcion: Obtiene artefactos necesarios y genera pasos para reparacion
% Autor: Tayler Wynta
pasos_reparar_sistema(Sistema, Estado0, EstadoFinal, Pasos) :-
    \+ esta_reparado(Sistema),
    sistema(ModSis, Sistema, Artefactos, fallo),
    pasos_obtener_lista_artefactos(Artefactos, Estado0, EstadoTras, PasosArts),
    pasos_entrar_modulo(ModSis, EstadoTras, EstadoEnSis, PasosMover),
    EstadoEnSis = estado(ModSis, Usados1, SisRep1, Vis1),
    append(SisRep1, [Sistema], SisRep2),
    EstadoFinal = estado(ModSis, Usados1, SisRep2, Vis1),
    append(PasosArts, PasosMover, PasosBase),
    append(PasosBase, [reparar(Sistema)], Pasos).

% Nombre: pasos_obtener_lista_artefactos/4
% Entrada: Lista de artefactos, Estado inicial, resultado, Pasos generados
% Salida: Genera pasos para obtener todos los artefactos de una lista
% Funcion: Permuta el orden de recoleccion para generar variantes
% Autor: Tayler Wynta
pasos_obtener_lista_artefactos(Lista, Estado0, EstadoFinal, Pasos) :-
    permutation(Lista, ListaOrden),
    pasos_obtener_lista_artefactos_ord(ListaOrden, Estado0, EstadoFinal, Pasos).

% Nombre: pasos_obtener_lista_artefactos_ord/4
% Entrada: Lista ordenada de artefactos, Estado inicial, resultado, Pasos generados
% Salida: Genera pasos para obtener artefactos en orden especifico
% Funcion: Recursivamente obtiene cada artefacto de la lista
% Autor: Tayler Wynta
pasos_obtener_lista_artefactos_ord([], EstadoActual, EstadoActual, []).
pasos_obtener_lista_artefactos_ord([Art|Resto], E0, EFinal, Pasos) :-
    pasos_obtener_artefacto(Art, E0, E1, PasosArt),
    pasos_obtener_lista_artefactos_ord(Resto, E1, EFinal, PasosResto),
    append(PasosArt, PasosResto, Pasos).

% Nombre: pasos_rescatar_tripulante/4
% Entrada: Tripulante, Estado inicial, resultado, Pasos generados
% Salida: Genera pasos para rescatar un tripulante
% Funcion: Navega hacia el tripulante y genera accion de rescate
% Autor: Tayler Wynta
pasos_rescatar_tripulante(Trip, Estado0, EstadoFinal, Pasos) :-
    \+ esta_rescatado(Trip),
    tripulante(Trip, ModTrip, _, atrapado),
    pasos_entrar_modulo(ModTrip, Estado0, EstadoFinal, PasosMover),
    append(PasosMover, [rescatar(Trip)], Pasos).

% Nombre: pasos_para_sistemas_ord/4
% Entrada: Lista ordenada de sistemas, Estado inicial, resultado, Pasos generados
% Salida: Genera pasos para reparar sistemas en orden especifico
% Funcion: Recursivamente repara cada sistema de la lista
% Autor: Tayler Wynta
pasos_para_sistemas_ord([], EstadoActual, EstadoActual, []).
pasos_para_sistemas_ord([Sys|Resto], E0, EFinal, Pasos) :-
    pasos_reparar_sistema(Sys, E0, E1, PasosSys),
    pasos_para_sistemas_ord(Resto, E1, EFinal, PasosResto),
    append(PasosSys, PasosResto, Pasos).

% Nombre: pasos_para_tripulantes_ord/4
% Entrada: Lista ordenada de tripulantes, Estado inicial, resultado, Pasos generados
% Salida: Genera pasos para rescatar tripulantes en orden especifico
% Funcion: Recursivamente rescata cada tripulante de la lista
% Autor: Tayler Wynta
pasos_para_tripulantes_ord([], EstadoActual, EstadoActual, []).
pasos_para_tripulantes_ord([Trip|Resto], E0, EFinal, Pasos) :-
    pasos_rescatar_tripulante(Trip, E0, E1, PasosTrip),
    pasos_para_tripulantes_ord(Resto, E1, EFinal, PasosResto),
    append(PasosTrip, PasosResto, Pasos).

% Nombre: generar_plan/1
% Entrada: Ninguna (variable de salida)
% Salida: Un plan completo de pasos para ganar
% Funcion: Genera un plan coherente permutando ordenes de sistemas y tripulantes
%          Si no hay objetivos, devuelve plan vacío (victoria automática)
% Autor: Tayler Wynta
generar_plan(Plan) :-
    jugador(ModuloInicial),
    usados(UsadosIni),
    EstadoIni = estado(ModuloInicial, UsadosIni, [], [ModuloInicial]),
    findall(S, (objetivoS(S, restaurado), \+ esta_reparado(S)), Sistemas),
    findall(T, (objetivoT(T, rescatado), \+ esta_rescatado(T)), Tripulantes),
    permutation(Sistemas,    OrdenSistemas),
    permutation(Tripulantes, OrdenTripulantes),
    pasos_para_sistemas_ord(OrdenSistemas,    EstadoIni,  EstadoTras, PasosSistemas),
    pasos_para_tripulantes_ord(OrdenTripulantes, EstadoTras, _,          PasosTripulantes),
    append(PasosSistemas, PasosTripulantes, Plan).

% Nombre: como_gano/1
% Entrada: Ninguna (variable de salida)
% Salida: Lista con todas las soluciones encontradas
% Funcion: Genera y devuelve todos los planes posibles para ganar
% Autor: Tayler Wynta
como_gano(Planes) :-
    findall(Plan, generar_plan(Plan), TodosPlanes),
    list_to_set(TodosPlanes, Planes).


% =========================================
% VERIFICACION DE VICTORIA
% =========================================

% Nombre: verifica_gane/0
% Entrada: Ninguna
% Salida: Verdadero si se alcanzó la condición de ganar, falso en caso contrario
% Funcion: Verifica la condición de victoria sin imprimir mensajes en consola
% Autor: Tayler Wynta
verifica_gane :-
    gano,
    !.