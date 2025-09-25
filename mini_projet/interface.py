from tkinter import *
from tkinter import messagebox

app = Tk()
app.geometry("800x500")
app.title("Todo List - Trello Style")

tasks = []
task_id_counter = 1
choix = StringVar()
choix.set("P1")
options = ["P1", "P2", "P3"]


def ajouter_tache():
    pass

def supprimer_tache(status, listbox):
    pass

def terminer_tache():
    pass

def afficher_taches():
    listbox_encours.delete(0, END)
    listbox_terminee.delete(0, END)
    for t in tasks:
        if t["Statut"] == "En cours":
            listbox_encours.insert(END, f"{t['Description']} | {t['Priorité']}")
        elif t["Statut"] == "Terminée":
            listbox_terminee.insert(END, f"{t['Description']} | {t['Priorité']}")

top_frame = Frame(app, pady=10)
top_frame.pack()

Label(top_frame, text="Description:").grid(row=0, column=0)
description_entry = Entry(top_frame, width=30)
description_entry.grid(row=0, column=1, padx=5)

Label(top_frame, text="Priorité:").grid(row=1, column=0)
dropdown = OptionMenu(top_frame, choix, *options)
dropdown.grid(row=1, column=1,pady=20)

Button(top_frame, text="Ajouter Tâche", command=ajouter_tache).grid(row=2, column=0, columnspan=2, pady=5)

bottom_frame = Frame(app)
bottom_frame.pack(fill="both", expand=True, padx=10)
marquer_terminer= tkk.Button()


frame_encours = Frame(bottom_frame, bg="lightyellow", width=350)
frame_encours.pack(side="left", fill="both", expand=True, padx=5, pady=5)
Label(frame_encours, text="En cours", bg="lightyellow").pack(pady=5)
listbox_encours = Listbox(frame_encours)
listbox_encours.pack(fill="both", expand=True, padx=5, pady=5)

frame_terminee = Frame(bottom_frame, bg="lightgreen", width=350)
frame_terminee.pack(side="left", fill="both", expand=True, padx=5, pady=5)
Label(frame_terminee, text="Terminée", bg="lightgreen").pack(pady=5)
listbox_terminee = Listbox(frame_terminee)
listbox_terminee.pack(fill="both", expand=True, padx=5, pady=5)

app.mainloop()
