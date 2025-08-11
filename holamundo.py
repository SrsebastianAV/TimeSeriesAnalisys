from tkinter import Tk, Label, TOP, BOTTOM, LEFT, RIGHT
#FENETRE PRINCIPALE
root = Tk()
root.geometry("500x500")
root.resizable(True, False)
root.minsize(50,50)
root.maxsize(800, 800)



etiqueta = Label(text="\n  ¡Planeamiento diario!  \n")
etiqueta1 = Label(text="\n  ¡Planeamiento diario!  \n")
etiqueta2 = Label(text="\n  ¡Planeamiento diario!  \n")
etiqueta3 = Label(text="\n  ¡Planeamiento diario!  \n")
#LOS GESTORES DE GEOMETRÍA SE UTILIZAN PARA DISTRIBUIR LOS WIDGETS EN LA FENETRE PRINCIPALE
#GESTOR DE GEOMETRÍA PACK
#IMPORTANTE: NO USAR pack y grid dentro de la misma ventana, los algoritmos utilizados para calcular las posicione no son compatibles
etiqueta.pack(side=TOP ,padx=10, pady=1)
etiqueta1.pack(side=BOTTOM ,padx=10, pady=10)
etiqueta2.pack(side=LEFT ,padx=10, pady=(100, 1))
etiqueta3.pack(side=RIGHT ,padx=10, pady=(1,10))

root.mainloop()