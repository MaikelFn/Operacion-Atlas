% Modulos
modulo(puente_mando, "Centro principal de la estacion.").
modulo(laboratorio, "Laboratorio cientifico parcialmente destruido.").
modulo(modulo_energia, "Modulo encargado del suministro energetico.").
modulo(enfermeria, "Area medica de emergencia.").
modulo(modulo_escape, "Zona de evacuacion orbital.").
modulo(hangar, "Area de almacenamiento y vehículos.").
modulo(sala_servidores, "Sala de control de sistemas críticos.").
modulo(hidroponia, "Cultivos hidroponicos de alimento.").
modulo(armeria, "Arsenal y equipos de defensa.").
modulo(crio, "Camaras criogenicas.").
% Enlaces
enlace(puente_mando, laboratorio).
enlace(laboratorio, modulo_energia).
enlace(puente_mando, enfermeria).
enlace(enfermeria, modulo_escape).
enlace(modulo_energia, hangar).
enlace(laboratorio, sala_servidores).
% Artefactos
artefacto(traje_espacial, enfermeria).
artefacto(fusible, laboratorio).
artefacto(tarjeta_seguridad, puente_mando).
% Sistemas
sistema(modulo_energia,energia,[fusible],fallo).
sistema(laboratorio,comunicaciones,[ fusible ,traje_espacial],fallo).
sistema(hangar,propulsion,[tarjeta_seguridad],fallo).
sistema(sala_servidores,navegacion,[fusible],fallo).
% Tripulantes
tripulante(elena, modulo_energia, [energia], atrapado).
tripulante(kai, enfermeria, [energia], atrapado).
tripulante(marcus, hangar, [propulsion], atrapado).
tripulante(sofia, sala_servidores, [navegacion], atrapado).
% Restricciones de acceso
necesita(modulo_energia, traje_espacial).
necesita(modulo_escape, tarjeta_seguridad).
% Restricciones de estado
necesitaEstado(modulo_escape, energia, restaurado).
% Restricciones por pasos previos
pasoPrevio(modulo_escape, modulo_energia).
%condiciones de gane
objetivoS(energia, restaurado).
objetivoS(comunicaciones, restaurado).
objetivoS(propulsion, restaurado).
objetivoS(navegacion, restaurado).
objetivoT(elena, rescatado).
objetivoT(kai, rescatado).
objetivoT(marcus, rescatado).
objetivoT(sofia, rescatado).
% Estado inicial
jugador(puente_mando).
artefactosLogrados([]).