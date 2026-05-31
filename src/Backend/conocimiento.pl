% Modulos (originales)
modulo(puente_mando, "Centro principal de la estacion - hub de comunicaciones.").
modulo(laboratorio, "Laboratorio cientifico parcialmente destruido.").
modulo(modulo_energia, "Modulo encargado del suministro energetico.").
modulo(enfermeria, "Area medica de emergencia.").
modulo(modulo_escape, "Zona de evacuacion orbital.").
% Modulos nuevos (10)
modulo(cuartel_seguridad, "Cuartel de seguridad con sistemas de control.").
modulo(centro_investigacion, "Centro avanzado de investigacion espacial.").
modulo(hidroponico, "Granja hidroponico para suministros alimenticios.").
modulo(taller_reparaciones, "Taller equipado con herramientas de reparacion.").
modulo(sala_servidores, "Sala principal de servidores de datos.").
modulo(area_recreacion, "Area de descanso y recreacion para la tripulacion.").
modulo(almacen_suministros, "Almacen general de suministros y repuestos.").
modulo(modulo_comunicaciones, "Modulo de comunicaciones intergalacticas.").
modulo(sala_control_sistemas, "Sala de control de sistemas de la estacion.").
modulo(bay_asteroides, "Bay de mineria de asteroides.").

% Enlaces (asegurando conexion sin nodos aislados)
% Hub central: puente_mando
enlace(puente_mando, laboratorio).
enlace(puente_mando, enfermeria).
enlace(puente_mando, cuartel_seguridad).
enlace(puente_mando, modulo_comunicaciones).
% Red desde laboratorio
enlace(laboratorio, modulo_energia).
enlace(laboratorio, centro_investigacion).
enlace(laboratorio, hidroponico).
% Red desde modulo_energia
enlace(modulo_energia, taller_reparaciones).
enlace(modulo_energia, sala_servidores).
enlace(modulo_energia, sala_control_sistemas).
% Red desde enfermeria
enlace(enfermeria, modulo_escape).
enlace(enfermeria, area_recreacion).
enlace(enfermeria, almacen_suministros).
% Red desde modulo_escape
enlace(modulo_escape, bay_asteroides).

% Artefactos (originales)
artefacto(traje_espacial, enfermeria).
artefacto(fusible, laboratorio).
artefacto(tarjeta_seguridad, puente_mando).
% Artefactos nuevos (5)
artefacto(cristal_reparacion, taller_reparaciones).
artefacto(codigo_acceso_elite, cuartel_seguridad).
artefacto(bateria_portatil, sala_servidores).
artefacto(sensor_radiacion, almacen_suministros).
artefacto(destornillador_plasma, hidroponico).

% Sistemas (originales)
sistema(modulo_energia, energia, [fusible], fallo).
sistema(laboratorio, comunicaciones, [fusible, traje_espacial], fallo).
% Sistemas nuevos
sistema(sala_control_sistemas, navegacion, [cristal_reparacion], fallo).
sistema(centro_investigacion, escaneadores, [sensor_radiacion, bateria_portatil], fallo).
sistema(cuartel_seguridad, defensa, [codigo_acceso_elite], fallo).
sistema(taller_reparaciones, herramientas, [destornillador_plasma], fallo).
sistema(sala_servidores, datos, [bateria_portatil], fallo).

% Tripulantes (originales)
tripulante(elena, modulo_energia, [energia], atrapado).
tripulante(kai, enfermeria, [energia], atrapado).
% Tripulantes nuevos (5)
tripulante(marcus, cuartel_seguridad, [defensa], atrapado).
tripulante(sophia, centro_investigacion, [escaneadores], atrapado).
tripulante(david, sala_servidores, [datos], atrapado).
tripulante(isabella, area_recreacion, [navegacion], atrapado).
tripulante(leo, bay_asteroides, [energia], atrapado).

% Restricciones de acceso
necesita(modulo_energia, traje_espacial).
necesita(modulo_escape, tarjeta_seguridad).
necesita(sala_servidores, codigo_acceso_elite).
necesita(bay_asteroides, traje_espacial).
necesita(centro_investigacion, sensor_radiacion).

% Restricciones de estado
necesitaEstado(modulo_escape, energia, restaurado).
necesitaEstado(bay_asteroides, navegacion, restaurado).
necesitaEstado(area_recreacion, navegacion, restaurado).

% Restricciones por pasos previos
pasoPrevio(modulo_escape, modulo_energia).
pasoPrevio(bay_asteroides, modulo_escape).
pasoPrevio(sala_servidores, modulo_energia).
pasoPrevio(centro_investigacion, laboratorio).

% Condiciones de gane
objetivoS(energia, restaurado).
objetivoS(comunicaciones, restaurado).
objetivoS(navegacion, restaurado).
objetivoS(escaneadores, restaurado).
objetivoT(elena, rescatado).
objetivoT(marcus, rescatado).
objetivoT(isabella, rescatado).


% Estado inicial
jugador(puente_mando).
artefactosLogrados([]).