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

:- consult('conocimiento.pl').

% =========================================
% ESTADO INICIAL
% =========================================


visitados([]).
usados([]).
tripulantes_rescatados([]).
sistemas_reparados([]).

inicializar_juego :-
    jugador(ModuloInicial),
    registrar_visita(ModuloInicial).


% =========================================
% CONECTIVIDAD ENTRE MODULOS
% =========================================

esta_conectado(X, Y) :-
    enlace(X, Y).

esta_conectado(X, Y) :-
    enlace(Y, X).

% =========================================
% RUTAS ENTRE MODULOS
% =========================================

% Devuelve en Ruta la lista de modulos desde Inicio hasta Destino.
ruta(Inicio, Destino, Ruta) :-
    ruta_aux(Inicio, Destino, [Inicio], Ruta).

% Caso base: cuando el nodo actual es el destino.
ruta_aux(Destino, Destino, Visitados, Visitados).

% Paso recursivo: explorar vecinos no visitados.
ruta_aux(Actual, Destino, Visitados, Ruta) :-
    esta_conectado(Actual, Siguiente),
    \+ member(Siguiente, Visitados),
    append(Visitados, [Siguiente], Visitados2),
    ruta_aux(Siguiente, Destino, Visitados2, Ruta).

% =========================================
% ARTEFACTOS LOGRADOS Y USO DE ARTEFACTOS
% =========================================

% Verifica si el jugador posee un artefacto.
tiene(Artefacto) :-
    artefactosLogrados(Lista),
    member(Artefacto, Lista).

% Verifica si el artefacto ya fue usado.
uso(Artefacto) :-
    usados(Lista),
    member(Artefacto, Lista).

% Registra el uso de un artefacto.
usar(Artefacto) :-
    tiene(Artefacto),
    \+ uso(Artefacto),
    usados(Lista),
    retract(usados(Lista)),
    assertz(usados([Artefacto | Lista])).

% =========================================
% VALIDACIONES DE MOVIMIENTO
% =========================================

% Verifica requisito de artefacto.
cumple_requisito_artefacto(Modulo) :-
    necesita(Modulo, Artefacto),
    uso(Artefacto).

cumple_requisito_artefacto(Modulo) :-
    \+ necesita(Modulo, _).

% Verifica si un modulo ya fue visitado.
fue_visitado(Modulo) :-
    visitados(Lista),
    member(Modulo, Lista).

% Verifica si un sistema ya fue reparado.
esta_reparado(Sistema) :-
    sistema(_, Sistema, _, restaurado).

% Verifica pasos previos requeridos.
cumple_paso_previo(Modulo) :-
    pasoPrevio(Modulo, Requerido),
    fue_visitado(Requerido).

cumple_paso_previo(Modulo) :-
    \+ pasoPrevio(Modulo, _).

% Verifica requisitos de estado.
cumple_requisito_estado(Modulo) :-
    necesitaEstado(Modulo, Sistema, restaurado),
    esta_reparado(Sistema).

cumple_requisito_estado(Modulo) :-
    \+ necesitaEstado(Modulo, _, _).

% =========================================
% REGISTRO DE ESTADOS
% =========================================

% Registra modulo visitado.
registrar_visita(Modulo) :-
    visitados(Lista),
    member(Modulo, Lista),
    !.

registrar_visita(Modulo) :-
    visitados(Lista),
    retract(visitados(Lista)),
    assertz(visitados([Modulo | Lista])).

% Registra tripulante rescatado.
registrar_rescate(Tripulante) :-
    tripulantes_rescatados(Lista),
    member(Tripulante, Lista),
    !.

registrar_rescate(Tripulante) :-
    tripulantes_rescatados(Lista),
    retract(tripulantes_rescatados(Lista)),
    assertz(tripulantes_rescatados([Tripulante | Lista])).

% Registra sistema reparado.
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

% Determina si el jugador puede ir al modulo destino.
puedo_ir(Destino) :-
    jugador(Origen),
    Origen \= Destino,
    modulo(Destino, _),
    esta_conectado(Origen, Destino),
    cumple_requisito_artefacto(Destino),
    cumple_paso_previo(Destino),
    cumple_requisito_estado(Destino).

% Mueve al jugador y registra visita.
mover(Destino) :-
    puedo_ir(Destino),
    jugador(Actual),
    retract(jugador(Actual)),
    assertz(jugador(Destino)),
    registrar_visita(Destino).

% =========================================
% ARTEFACTOS
% =========================================

% Toma un artefacto del modulo actual.
tomar(Artefacto) :-
    jugador(ModuloActual),
    artefacto(Artefacto, ModuloActual),
    artefactosLogrados(Lista),
    \+ member(Artefacto, Lista),
    retract(artefactosLogrados(Lista)),
    assertz(artefactosLogrados([Artefacto | Lista])).

% =========================================
% REPARACION DE SISTEMAS
% =========================================

% Verifica si todos los artefactos fueron usados.
tiene_todos([]).

tiene_todos([Cabeza | Cola]) :-
    uso(Cabeza),
    tiene_todos(Cola).

% Repara un sistema.
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
    registrar_reparacion(Sistema).

% =========================================
% RESCATE DE TRIPULANTES
% =========================================

% Verifica si un tripulante ya fue rescatado.
esta_rescatado(Tripulante) :-
    tripulante(
        Tripulante,_,_,rescatado).

% Verifica si todos los sistemas requeridos funcionan.
sistemas_funcionando([]).

sistemas_funcionando([Cabeza | Cola]) :-
    esta_reparado(Cabeza),
    sistemas_funcionando(Cola).

% Rescata un tripulante.
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
    registrar_rescate(Tripulante).

% =========================================
% CONSULTAS
% =========================================

% Devuelve la ubicacion de un artefacto.
donde_esta(Artefacto, Modulo) :-
    artefacto(Artefacto, Modulo).

% Devuelve artefactos logrados actuales.
que_tengo(Lista) :-
    artefactosLogrados(Lista).

% Devuelve modulos visitados.
modulos_visitados(Lista) :-
    visitados(Lista).

% =========================================
% CONDICIONES DE VICTORIA
% =========================================

cumple_objetivos_sistemas :-
    forall(
        objetivoS(Sistema, restaurado),
        esta_reparado(Sistema)
    ).

cumple_objetivos_tripulantes :-
    forall(
        objetivoT(Tripulante, rescatado),
        esta_rescatado(Tripulante)
    ).

gano :-
    cumple_objetivos_sistemas,
    cumple_objetivos_tripulantes.