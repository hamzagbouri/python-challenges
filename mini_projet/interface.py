from tkinter import *
from tkinter import messagebox
from database import get_session
from database import get_all_tasks
from database import *
app = Tk()
app.geometry("800x500")
app.title("Todo List - Trello Style")


task_id_counter = 1
choix_priorite = StringVar()
choix_priorite.set("P1")
options = ["P1", "P2", "P3"]

#---------------------------- function 
def string_to_dict(string: str):
    parts = [p.strip() for p in string.split("|")]
    return get_task_by_id(int(parts[0]))

def ajouter_tache():
    description = description_entry.get()
    priorite = choix_priorite
    if(description.strip()):
        task = Task(description = description,priorite = priorite.get())
        res = add_task(task)
        if(res.id):
            messagebox.showinfo(message="Tache Ajouter Avec success")
            description_entry.insert(0,"")
            afficher_taches()
    else:
        messagebox.showwarning(message="Fill the description")
    pass

def supprimer_tache(task):
    result  = messagebox.askyesno("Confirmation", message=f"Are you sure you want to delete this task?, {task.id}")
    if result:
        if(supprimer_task(task.id)):
            messagebox.showinfo("Tache supprimer avec succe")
            afficher_taches()
    pass

def terminer_tache(task):
    if terminer_task(task):
        messagebox.showinfo(message='Tache marquer comme termine ')
        afficher_taches()
    else:
        messagebox.showerror(message="Couldn't fin task")
    pass

def afficher_taches():
    listbox_encours.delete(0, END)
    listbox_terminee.delete(0, END)
    tasks = get_all_tasks()
    for t in tasks:
        if t.status == "En cours":
            listbox_encours.insert(END, f"{t.id} | {t.description} | {t.priorite}")
        elif t.status == "Terminé":
            listbox_terminee.insert(END, f"{t.id} | {t.description} | {t.priorite}")

def on_select(event):
    listbox_selected = event.widget
    index = listbox_selected.curselection()
    if(index):
        value = listbox_selected.get(index)
        task = string_to_dict(str(value))
        if(listbox_selected == listbox_encours):
            marquer_terminer.config(state="active", command=lambda: terminer_tache(task))
        elif listbox_selected == listbox_terminee:
            marquer_terminer.config(state="disabled")
        tache_suprimer.config(state="active", command=lambda: supprimer_tache(task))

        print(task)
#-------------------------------- Interface
top_frame = Frame(app, pady=10)
top_frame.pack()

Label(top_frame, text="Description:").grid(row=0, column=0)
description_entry = Entry(top_frame, width=30)
description_entry.grid(row=0, column=1, padx=5, ipadx=10)

Label(top_frame, text="Priorité:").grid(row=1, column=0)
dropdown_priorite = OptionMenu(top_frame, choix_priorite, *options)
dropdown_priorite.grid(row=1, column=1,pady=20)

Button(top_frame, text="Ajouter Tâche", command=ajouter_tache).grid(row=2, column=0, columnspan=2, pady=5)

bottom_frame = Frame(app)
bottom_frame.pack(fill="both", expand=True, padx=10)

listbox_frame = Frame(bottom_frame)
listbox_frame.place(relx=0, rely=0, relwidth=1, relheight=0.8)  

frame_encours = Frame(listbox_frame, width=350)
frame_encours.pack(side="left", fill="both", expand=True, padx=5, pady=5)
Label(frame_encours, text="En cours").pack(pady=5)
listbox_encours = Listbox(frame_encours)
listbox_encours.pack(fill="both", expand=True, padx=5, pady=5)
listbox_encours.bind("<<ListboxSelect>>", on_select)

frame_terminee = Frame(listbox_frame, width=350)
frame_terminee.pack(side="left", fill="both", expand=True, padx=5, pady=5)
Label(frame_terminee, text="Terminée").pack(pady=5)
listbox_terminee = Listbox(frame_terminee)
listbox_terminee.pack(fill="both", expand=True, padx=5, pady=5)
listbox_terminee.bind("<<ListboxSelect>>", on_select)

buttons_frame = Frame(bottom_frame)
buttons_frame.place(relx=0, rely=0.8, relwidth=1, relheight=0.2)
marquer_terminer= Button(buttons_frame, text="Terminer tache", state="disabled")
marquer_terminer.pack(side="right")
tache_suprimer = Button(buttons_frame, text="Supprimer tache", state="disabled")
tache_suprimer.pack(side='right')
afficher_taches()
app.mainloop()
