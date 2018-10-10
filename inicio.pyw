#importamos la libreria tkinter
from tkinter import *

#----------------------------------------------------------------------------------------------------------------------------

#importamos el modulo para crear botones, el modulo con las funciones
from funciones import *

#----------------------------------------------------------------------------------------------------------------------------

#creamos la barra de MENU y de indicamos que va a estar asociado a la raiz root
barraMenus=Menu(root)

#le asignamos el menu barraMenus a la raiz root
root.config(menu=barraMenus)

#creamos los elementos del menu y le asignamos su nombre
archivo=Menu(barraMenus, tearoff=0)
barraMenus.add_cascade(label="Archivo", menu=archivo)

#creamos los elementos del menu Archivomenu
#archivo.add_command(label="Adorno")
archivo.add_command(label="Salir", command=exit)

#creamos los elementos del menu y le asignamos su nombre
ayuda=Menu(barraMenus, tearoff=0)
barraMenus.add_cascade(label="Ayuda", menu=ayuda)

#creamos los elementos del menu Ayuda
ayuda.add_command(label="Acerca de", command=acerca)

#----------------------------------------------------------------------------------------------------------------------------

# con este comando damos orden que al pulsar el boton X de la ventana root llame a la funcion exit
root.protocol("WM_DELETE_WINDOW",exit)

#----------------------------------------------------------------------------------------------------------------------------

#realizamos la llamada a la funcion principal
principal()

#----------------------------------------------------------------------------------------------------------------------------

#ponemos el mainloop para que esté constantemente reescribiendose la ventana
root.mainloop()
