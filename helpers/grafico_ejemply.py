import matplotlib.pyplot as plt
fig, gnt = plt.subplots()

"Limetes de x e y"
gnt.set_ylim(0, 120)
gnt.set_xlim(0, 200)
"Nombres de los ejes"
gnt.set_xlabel('Tiempo')
gnt.set_ylabel('Actividades')
"Etiquetas"
ALTURA=[15,25,35,45,55]
gnt.set_yticks(ALTURA) #Altura y cantidad
NOMBRE=['A','B','C','D','E']
gnt.set_yticklabels(NOMBRE) #Nombres las etiquetas

gnt.grid(True)

a=[40,40,70,70,90]#Inicio
b=[30,50,50,60,20]#Cantidad de dias de la actividad
for i in range(5):
    gnt.broken_barh([(a[i], (b[i]))], (10+(10*i), 9), facecolors =('tab:orange'))
#gnt.broken_barh([(start_time, duration)],
#                (lower_yaxis, height),
#                facecolors=('tab:colors'))"
plt.show()