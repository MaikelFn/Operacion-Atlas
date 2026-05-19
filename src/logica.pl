% Carga la base de conocimiento compartida con la interfaz.
:- consult('conocimiento.pl').

% Estado dinamico del juego: jugador actual, inventario, modulos visitados y sistemas reparados.
:- dynamic jugador/1.
:- dynamic inventario/1.
:- dynamic visitados/1.
:- dynamic sistemas_reparados/1.

jugador(modulo_energia).
inventario([fusible]).
sistemas_reparados([]).

% Relacion de conectividad entre modulos, considerando ambos sentidos.
esta_conectado(X, Y) :-
    enlace(X, Y).
esta_conectado(X, Y) :-
    enlace(Y, X).

% Consulta simple para saber si el inventario contiene un artefacto.
tiene(Artefacto) :-
    inventario(Lista),
    member(Artefacto, Lista).

% Verifica si el modulo cumple la condicion de artefacto requerido.
cumple_requisito_artefacto(Modulo) :-
    necesita(Modulo, Artefacto),
    tiene(Artefacto).
cumple_requisito_artefacto(Modulo) :-
    \+ necesita(Modulo, _).

% Comprueba si un modulo ya fue visitado.
fue_visitado(Modulo) :-
    visitados(Lista),
    member(Modulo, Lista).

% Comprueba si un sistema ya fue reparado.
esta_reparado(Sistema) :-
    sistemas_reparados(Lista),
    member(Sistema, Lista).

% Valida el paso previo requerido por algunos modulos.
cumple_paso_previo(Modulo) :-
    pasoPrevio(Modulo, Requerido),
    fue_visitado(Requerido).
cumple_paso_previo(Modulo) :-
    \+ pasoPrevio(Modulo, _).

% Valida que el estado requerido del sistema este cumplido.
cumple_requisito_estado(Modulo) :-
    necesitaEstado(Modulo, Sistema, restaurado),
    esta_reparado(Sistema).
cumple_requisito_estado(Modulo) :-
    \+ necesitaEstado(Modulo, _, _).

% Registra una visita.
registrar_visita(Modulo) :-
    visitados(Lista),
    member(Modulo, Lista),!.
registrar_visita(Modulo) :-
    visitados(Lista),
    retract(visitados(Lista)),
    assertz(visitados([Modulo | Lista])).

% Registra un sistema reparado.
registrar_sistema_reparado(Sistema) :-
    sistemas_reparados(Lista),
    member(Sistema, Lista),!.
registrar_sistema_reparado(Sistema) :-
    sistemas_reparados(Lista),
    retract(sistemas_reparados(Lista)),
    assertz(sistemas_reparados([Sistema | Lista])).

% Determina si el jugador puede moverse de un origen a un destino.
puedo_ir(Origen, Destino) :-
    Origen \= Destino,
    modulo(Destino),
    esta_conectado(Origen, Destino),
    cumple_requisito_artefacto(Destino),
    cumple_paso_previo(Destino),
    cumple_requisito_estado(Destino).

% Mueve al jugador si la ruta es valida y registra la visita.
mover(Destino) :-
    jugador(Actual),
    puedo_ir(Actual, Destino),
    retract(jugador(Actual)),
    assertz(jugador(Destino)),
    registrar_visita(Destino).

% Toma un artefacto del modulo actual y lo agrega al inventario.
tomar(Artefacto) :-
    jugador(ModuloActual),
    artefacto(Artefacto, ModuloActual),
    inventario(Lista),
    \+ member(Artefacto, Lista),
    retract(inventario(Lista)),
    assertz(inventario([Artefacto | Lista])).

tiene_todos([]).
tiene_todos([Cabeza | Cola]) :-
    tiene(Cabeza), tiene_todos(Cola).

% Repara un sistema si el jugador cumple todos los requisitos.
reparar(Sistema) :-
    jugador(ModuloActual),
    sistema(ModuloActual, Sistema, Artefactos, fallo),
    \+ esta_reparado(Sistema),
    tiene_todos(Artefactos),
    registrar_sistema_reparado(Sistema).