  Etapa 0 — Diagnóstico de violaciones a la matriz de acceso

  Entrando como ovni@lab.local (Frente OVNI, team_id = 1), el sistema corre, luego permite todas estas
  acciones que la matriz prohíbe:

  1. Listar catálogos ajenos. Las opciones 2 (fantasmas) y 3 (wizards) devuelven los
  registros completos de ghosts y wizards. Según la matriz, OVNI solo debería ver la
  tabla ovnis; las otras dos columnas son "—". El código en list_catalog() (línea 174)
   nunca recibe ni consulta el user logueado.
  2. Agregar ítems en catálogos ajenos. La opción 4 pregunta "¿Lista? 1=ovnis 2=ghosts
   3=wizards" y acepta cualquiera. Un agente OVNI puede insertar filas en ghosts o
  wizards. add_catalog_item() (línea 194) tampoco valida el equipo.
  3. Leer notas de todos los equipos. La opción 5 ejecuta _SQL_LIST_NOTAS_ALL (línea
  77), un SELECT sin WHERE team_id = %s. El agente OVNI ve notas del Frente Espectral
  y del Frente Arcano — filtración directa de expedientes ajenos.
  4. Escribir notas en nombre de otro equipo. La opción 6 deja elegir team_id a mano
  (1, 2 o 3). Un agente OVNI puede crear una nota con team_id = 3 y contaminar el
  expediente Arcano. add_nota_any_team() (línea 226) usa el input del usuario como
  team_id en vez de forzar user['team_id'].
