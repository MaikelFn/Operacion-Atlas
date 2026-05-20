modulo(puente_mando).
modulo(laboratorio).
modulo(modulo_energia).
modulo(enfermeria).
modulo(modulo_escape).

enlace(puente_mando, laboratorio).
enlace(puente_mando, enfermeria).
enlace(laboratorio, modulo_energia).
enlace(modulo_energia, modulo_escape).

artefacto(fusible, laboratorio).
artefacto(traje_espacial, enfermeria).
artefacto(tarjeta_seguridad, puente_mando).

% necesita(Modulo, Artefacto).
necesita(modulo_energia, traje_espacial).

% pasoPrevio(Modulo, ModuloNecesario).
pasoPrevio(modulo_escape, modulo_energia).


% necesitaEstado(Modulo, Sistema, Estado).
necesitaEstado(modulo_escape, energia, restaurado).


% sistema(Modulo, NombreSistema, ArtefactosNecesarios, EstadoInicial).
sistema(modulo_energia, energia, [fusible], fallo).
sistema(laboratorio, comunicaciones, [tarjeta_seguridad], fallo).


tripulante(elena, laboratorio, [energia], atrapado).

objetivo_reparar(energia).
objetivo_rescatar(elena).