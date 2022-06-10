from datetime import datetime

def calcularFechaFinal (connection, id_proyecto, Fech):
    # buscamos las actividades que pertencen al proyecto
    Actividades = connection.select(f"SELECT * FROM Actividad WHERE actividad.id_proyecto = {id_proyecto}")
    # bad es una bandera que nos ayuda a comprobar que una actividad tiene una relacion asociada a ella
    ban = 0
    relaciones = connection.select(f"SELECT * FROM relacion WHERE id_proyect = {id_proyecto}")
    #
    for act in Actividades:
        ban = 0
        # print(act)
        for rela in relaciones:
            if act[0] == rela[2]:
                ban = 1
        if ban == 0:
            fechAux = datetime.strptime((act[4].replace("/", "-")), "%Y-%m-%d").date()
            # print(act[3], "==>", (fechAux))
            fechFin = Fech.FechaSegunFechaYDias(fechAux, int(act[3]))
            # print("FECHA FINAL:", fechFin)
            connection.update(
                "actividad",
                ["fecha_culminacion","fecha_culminacion_tardio"],
                [fechFin,fechFin],
                "id_actividad",
                act[0]
            )
            finProyect = connection.select(f"SELECT fecha_final FROM Proyecto WHERE id_proyecto = {id_proyecto}")[0][0]
            if fechFin > datetime.strptime((finProyect.replace("/","-")), "%Y-%m-%d").date():
                connection.update(
                    "proyecto",
                    ["fecha_final"],
                    [fechFin],
                    "id_proyecto",
                    id_proyecto
                )
        else:

            # relaciones que van hacia la actividad ciclada es una actividad siguiente
            relaciones_siguientes = connection.select(f"SELECT * FROM relacion WHERE id_proyect = {id_proyecto} and id_actividad_sig = {act[0]}")
            if len(relaciones_siguientes) > 0:
                mayor = connection.select(f"SELECT fecha_culminacion FROM actividad WHERE id_actividad = {relaciones_siguientes[0][1]}")[0][0]
                for may in relaciones_siguientes:
                    fechAnt = connection.select(f"SELECT fecha_culminacion FROM actividad WHERE id_actividad = {may[1]}")[0][0]
                    if datetime.strptime((fechAnt.replace("/", "-")), "%Y-%m-%d").date() > datetime.strptime((mayor.replace("/", "-")), "%Y-%m-%d").date():
                        mayor = fechAnt
                fechAux = datetime.strptime((mayor.replace("/", "-")), "%Y-%m-%d").date()
                fechFin = Fech.FechaSegunFechaYDias(fechAux, int(act[3]))
                connection.update(
                    "actividad",
                    ["fecha_inicio_temprano","fecha_culminacion","fecha_inicio_tardio","fecha_culminacion_tardio"],
                    [mayor,fechFin,mayor,fechFin],
                    "id_actividad",
                    act[0]
                )
                finProyect = connection.select(f"SELECT fecha_final FROM Proyecto WHERE id_proyecto = {id_proyecto}")[0][0]
                if fechFin > datetime.strptime((finProyect.replace("/", "-")), "%Y-%m-%d").date():
                    connection.update(
                        "proyecto",
                        ["fecha_final"],
                        [fechFin],
                        "id_proyecto",
                        id_proyecto
                    )
        print("-----")