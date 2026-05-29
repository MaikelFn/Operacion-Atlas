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

:- consult('conocimiento.pl').

% =========================================
% ESTADO INICIAL
% =========================================

visitados([]).
usados([]).
tripulantes_rescatados([]).
sistemas_reparados([]).
ruta_historial([]).

% Nombre: inicializar_juego/0
% Entrada: Ninguna
% Salida: Registra la visita del modulo inicial del jugador
% Funcion: Inicializa el estado de recorrido del juego a partir del modulo actual
% Autor: Maikel Flores
inicializar_juego :-
    jugador(ModuloInicial),
    registrar_visita(ModuloInicial).

% =========================================
% CONECTIVIDAD ENTRE MODULOS
% =========================================

% Nombre: esta_conectado/2
% Entrada: Dos modulos
% Salida: Verdadero si existe conexion entre ambos modulos
% Funcion: Determina si hay enlace directo entre X y Y (bidireccional)
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
% Salida: Verdadero si todos los objetivos de sistemas estan restaurados
% Funcion: Comprueba que cada objetivoS/2 requerido termine en estado restaurado
% Autor: Maikel Flores
cumple_objetivos_sistemas :-
    forall(
        objetivoS(Sistema, restaurado),
        esta_reparado(Sistema)
    ).

% Nombre: cumple_objetivos_tripulantes/0
% Entrada: Ninguna
% Salida: Verdadero si todos los objetivos de tripulantes estan rescatados
% Funcion: Comprueba que cada objetivoT/2 requerido termine en estado rescatado
% Autor: Maikel Flores
cumple_objetivos_tripulantes :-
    forall(
        objetivoT(Tripulante, rescatado),
        esta_rescatado(Tripulante)
    ).

% Nombre: gano/0
% Entrada: Ninguna
% Salida: Verdadero si se cumplieron todos los objetivos
% Funcion: Determina la condicion de victoria completa del juego
% Autor: Maikel Flores
gano :-
    cumple_objetivos_sistemas,
    cumple_objetivos_tripulantes.

% =========================================
% COMO GANO
% =========================================

% Nombre: pasos_para_artefacto/4
% Entrada: Artefacto, ModuloActual, ModuloSiguiente, Pasos
% Salida: Lista de pasos [ir?, tomar, usar] para un artefacto pendiente
% Funcion: Si el artefacto no fue usado, genera pasos para ir a buscarlo y usarlo.
%          ModuloSiguiente unifica con el modulo donde queda el jugador tras los pasos.
pasos_para_artefacto(Artefacto, ModuloActual, ModuloSig, Pasos) :-
    \+ uso(Artefacto),
    artefacto(Artefacto, ModuloArtefacto),
    (   ModuloActual \= ModuloArtefacto
    ->  Pasos = [ir(ModuloArtefacto), tomar(Artefacto), usar(Artefacto)],
        ModuloSig = ModuloArtefacto
    ;   Pasos = [tomar(Artefacto), usar(Artefacto)],
        ModuloSig = ModuloActual
    ).

pasos_para_artefacto(Artefacto, ModuloActual, ModuloActual, []) :-
    uso(Artefacto).

% Nombre: pasos_para_lista_artefactos/4
% Entrada: ListaArtefactos, ModuloActual, ModuloFinal, Pasos
% Salida: Lista de pasos para obtener y usar todos los artefactos de la lista
% Funcion: Recursion sobre cada artefacto requerido, acumulando pasos en orden
pasos_para_lista_artefactos([], Modulo, Modulo, []).
pasos_para_lista_artefactos([Art|Resto], ModuloActual, ModuloFinal, Pasos) :-
    pasos_para_artefacto(Art, ModuloActual, ModuloTras, PasosArt),
    pasos_para_lista_artefactos(Resto, ModuloTras, ModuloFinal, PasosResto),
    append(PasosArt, PasosResto, Pasos).

% Nombre: pasos_para_sistema/4
% Entrada: Sistema, ModuloActual, ModuloFinal, Pasos
% Salida: Lista de pasos para reparar el sistema desde ModuloActual
% Funcion: Genera pasos para conseguir artefactos, ir al modulo y reparar
pasos_para_sistema(Sistema, ModuloActual, ModuloFinal, Pasos) :-
    \+ esta_reparado(Sistema),
    sistema(ModuloSistema, Sistema, Artefactos, fallo),
    pasos_para_lista_artefactos(Artefactos, ModuloActual, ModuloTras, PasosArts),
    (   ModuloTras \= ModuloSistema
    ->  PasosMover = [ir(ModuloSistema)]
    ;   PasosMover = []
    ),
    append(PasosArts, PasosMover, PasosBase),
    append(PasosBase, [reparar(Sistema)], Pasos),
    ModuloFinal = ModuloSistema.

% Nombre: pasos_para_sistemas/4
% Entrada: ListaSistemas, ModuloActual, ModuloFinal, Pasos
% Salida: Lista de pasos para reparar todos los sistemas pendientes en orden
% Funcion: Recursion sobre cada sistema, encadenando el modulo final como siguiente inicio
pasos_para_sistemas([], Modulo, Modulo, []).
pasos_para_sistemas([Sys|Resto], ModuloActual, ModuloFinal, Pasos) :-
    pasos_para_sistema(Sys, ModuloActual, ModuloTras, PasosSys),
    pasos_para_sistemas(Resto, ModuloTras, ModuloFinal, PasosResto),
    append(PasosSys, PasosResto, Pasos).

% Nombre: pasos_para_tripulante/4
% Entrada: Tripulante, ModuloActual, ModuloFinal, Pasos
% Salida: Lista de pasos para rescatar al tripulante desde ModuloActual
% Funcion: Genera pasos para ir al modulo del tripulante y rescatarlo
pasos_para_tripulante(Tripulante, ModuloActual, ModuloFinal, Pasos) :-
    \+ esta_rescatado(Tripulante),
    tripulante(Tripulante, ModuloTripulante, _, atrapado),
    (   ModuloActual \= ModuloTripulante
    ->  Pasos = [ir(ModuloTripulante), rescatar(Tripulante)]
    ;   Pasos = [rescatar(Tripulante)]
    ),
    ModuloFinal = ModuloTripulante.

% Nombre: pasos_para_tripulantes/4
% Entrada: ListaTripulantes, ModuloActual, ModuloFinal, Pasos
% Salida: Lista de pasos para rescatar todos los tripulantes pendientes en orden
% Funcion: Recursion sobre cada tripulante, encadenando posicion tras cada rescate
pasos_para_tripulantes([], Modulo, Modulo, []).
pasos_para_tripulantes([Trip|Resto], ModuloActual, ModuloFinal, Pasos) :-
    pasos_para_tripulante(Trip, ModuloActual, ModuloTras, PasosTrip),
    pasos_para_tripulantes(Resto, ModuloTras, ModuloFinal, PasosResto),
    append(PasosTrip, PasosResto, Pasos).

% Nombre: generar_plan/1
% Entrada: Ninguna (variable de salida)
% Salida: Lista de pasos del tipo ir/1, tomar/1, usar/1, reparar/1, rescatar/1
% Funcion: Genera un plan completo usando backtracking sobre el orden de sistemas y tripulantes.
%          El backtracking de Prolog explora distintas permutaciones, generando soluciones distintas.
generar_plan(Plan) :-
    jugador(ModuloInicial),
    findall(S, (objetivoS(S, restaurado), \+ esta_reparado(S)), Sistemas),
    findall(T, (objetivoT(T, rescatado), \+ esta_rescatado(T)), Tripulantes),
    permutation(Sistemas, OrdenSistemas),
    permutation(Tripulantes, OrdenTripulantes),
    pasos_para_sistemas(OrdenSistemas, ModuloInicial, ModuloTras, PasosSistemas),
    pasos_para_tripulantes(OrdenTripulantes, ModuloTras, _, PasosTripulantes),
    append(PasosSistemas, PasosTripulantes, Plan).

% Nombre: como_gano/1
% Entrada: Ninguna (variable de salida)
% Salida: Lista de hasta 2 planes distintos
% Funcion: Obtiene hasta 2 soluciones distintas usando findall sobre generar_plan
como_gano(Planes) :-
    findall(Plan, generar_plan(Plan), TodosPlanes),
    list_to_set(TodosPlanes, PlanesUnicos),
    (   PlanesUnicos = []
    ->  Planes = []
    ;   length(PlanesUnicos, N),
        Max is min(N, 2),
        length(Planes, Max),
        append(Planes, _, PlanesUnicos)
    ).

% =========================================
% VERIFICACION DE VICTORIA
% =========================================

% Nombre: verifica_gane/0
% Entrada: Ninguna
% Salida: Imprime el resumen de victoria si se alcanzó la condición de ganar
% Funcion: Si gano/0 es verdadero, recopila y muestra por consola la ruta realizada, artefactos logrados, sistemas reparados y tripulantes rescatados
% Autor: Tayler Wynta
verifica_gane :-
    gano,
    !,
    write('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'), nl,
    write('¡CONDICION DE VICTORIA ALCANZADA!'), nl,
    write('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'), nl, nl,
    
    write('RUTA REALIZADA:'), nl,
    ruta_historial(Ruta),
    write(Ruta), nl, nl,
    
    write('ARTEFACTOS LOGRADOS:'), nl,
    artefactosLogrados(Artefactos),
    write(Artefactos), nl, nl,
    
    write('SISTEMAS REPARADOS:'), nl,
    sistemas_reparados(Sistemas),
    write(Sistemas), nl, nl,
    
    write('TRIPULACION RESCATADA:'), nl,
    tripulantes_rescatados(Tripulantes),
    write(Tripulantes), nl.
