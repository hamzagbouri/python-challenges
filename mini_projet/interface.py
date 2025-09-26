from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
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
status = ["A faire", "En cours", "Terminé"]

#---------------------------- function 


def ajouter_tache():
    description = description_entry.get()
    priorite = choix_priorite
    if(description.strip()):
        task = Task(description = description,priorite = priorite.get())
        res = add_task(task)
        if(res.id):
            afficher_taches()
            messagebox.showinfo(message="Tache Ajouter Avec success")
            description_entry.insert(0,"")
            
    else:
        messagebox.showwarning(message="Fill the description")
    pass

def supprimer_tache(task):
    result  = messagebox.askyesno("Confirmation", message=f"Are you sure you want to delete this task?, {task.id}")
    if result:
        if(supprimer_task(task.id)):
            afficher_taches()
            messagebox.showinfo(message="Tache supprimer avec succe")
    pass

def terminer_tache(task):
    if terminer_task(task):
        messagebox.showinfo(message='Tache marquer comme termine ')
        afficher_taches()
    else:
        messagebox.showerror(message="Couldn't fin task")
    pass

def afficher_taches():
    # 🧹 Clear old cards
    for container in [tasks_afaire_container, tasks_encours_container, tasks_terminee_container]:
        for widget in container.winfo_children():
            widget.destroy()

    tasks = get_all_tasks()

    for t in tasks:
        card = Frame(
            tasks_afaire_container if t.status == "A faire" else
            tasks_encours_container if t.status == "En cours" else
            tasks_terminee_container,
            bg="#f5f5f5", bd=1, relief="ridge", padx=10, pady=5, 
        )
        card.pack(fill="both", pady=5, padx=5)
        Label(card, text=t.description, font=("Arial", 12, "bold"), bg="#f5f5f5").pack(anchor="w")
        Label(card, text=f"Priorité: {t.priorite}", fg="gray", bg="#f5f5f5").pack(anchor="w")
        btn_frame = Frame(card, bg="#f5f5f5")
        btn_frame.pack(anchor="e", pady=5)

        Button(btn_frame, text="Modifier", bg="#2196F3", fg="white",
               command=lambda task=t: ouvrir_modifier(task)).pack(side="left", padx=5)

        Button(btn_frame, text="Supprimer", bg="#f44336", fg="white",
               command=lambda task=t: supprimer_tache(task)).pack(side="left", padx=5)
        choix_status = StringVar(value=t.status)
        status_options = ["A faire", "En cours", "Terminé"]

        def on_status_change(var, idx, mode,task=t, var_obj=choix_status):
            new_status = var_obj.get()
            task.status = new_status
            modify_stats(task) 
            afficher_taches()
        choix_status.trace_add("write", on_status_change)

        OptionMenu(btn_frame, choix_status, *status_options).pack(side="left", padx=5)

        if t.status != "Terminé":
            Button(btn_frame, text="Terminer", bg="#4CAF50", fg="white",
                   command=lambda task=t: terminer_tache(task)).pack(side="left", padx=5)


def ouvrir_modifier(task):
    new_win = Toplevel(app)
    new_win.title("Modifier la tâche")
    new_win.geometry("350x180")
    new_win.configure(bg="#f5f5f5")

    # ---------- Title ----------
    Label(new_win, text=f"Modifier la tâche: {task.description}", bg="#f5f5f5", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

    # ---------- Description ----------
    Label(new_win, text="Description:", bg="#f5f5f5").grid(row=1, column=0, sticky="e", padx=10, pady=5)
    desc_var = StringVar(value=task.description)
    Entry(new_win, textvariable=desc_var, width=25).grid(row=1, column=1, padx=10, pady=5)

    # ---------- Priorité ----------
    Label(new_win, text="Priorité:", bg="#f5f5f5").grid(row=2, column=0, sticky="e", padx=10, pady=5)
    priorite_var = StringVar(value=task.priorite)
    OptionMenu(new_win, priorite_var, "P1", "P2", "P3").grid(row=2, column=1, padx=10, pady=5, sticky="w")

    # ---------- Modifier Button ----------
    def modifier_task():
        task.description = desc_var.get()
        task.priorite = priorite_var.get()
        modify_task(task)
        afficher_taches()
        new_win.destroy()  

    Button(new_win, text="Modifier", bg="#4CAF50", fg="white", width=15, command=modifier_task).grid(row=3, column=0, columnspan=2, pady=15)

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

#---------------------------- Frame A faire -------------------------------------------

frame_afaire = Frame(listbox_frame, width=350)
frame_afaire.pack(side="left", fill="both", expand=True, padx=5, pady=5)

Label(frame_afaire, text="A faire").pack(pady=5)

canvas_afaire = Canvas(frame_afaire, highlightthickness=0)
scrollbar_afaire = Scrollbar(frame_afaire, orient="vertical", command=canvas_afaire.yview)
tasks_afaire_container = Frame(canvas_afaire)

tasks_afaire_container.bind(
    "<Configure>",
    lambda e: canvas_afaire.configure(scrollregion=canvas_afaire.bbox("all"))
)
canvas_afaire.bind(
    "<Configure>",
    lambda e: canvas_afaire.itemconfig(window_afaire, width=e.width)
)

window_afaire = canvas_afaire.create_window((0, 0), window=tasks_afaire_container, anchor="nw")
canvas_afaire.configure(yscrollcommand=scrollbar_afaire.set)
canvas_afaire.pack(side="left", fill="both", expand=True)
scrollbar_afaire.pack(side="right", fill="y")


#---------------------------- Frame En Cours -------------------------------------------

frame_encours = Frame(listbox_frame, width=350)
frame_encours.pack(side="left", fill="both", expand=True, padx=5, pady=5)
Label(frame_encours, text="En cours").pack(pady=5)

canvas_encours = Canvas(frame_encours, highlightthickness=0)
scrollbar_encours = Scrollbar(frame_encours, orient="vertical", command=canvas_encours.yview)
tasks_encours_container = Frame(canvas_encours)

tasks_encours_container.bind(
    "<Configure>",
    lambda e: canvas_encours.configure(scrollregion=canvas_encours.bbox("all"))
)
canvas_encours.bind(
    "<Configure>",
    lambda e: canvas_encours.itemconfig(window_afaire, width=e.width)
)

canvas_encours.create_window((0, 0), window=tasks_encours_container, anchor="nw")
canvas_encours.configure(yscrollcommand=scrollbar_encours.set)

canvas_encours.pack(side="left", fill="both", expand=True)
scrollbar_encours.pack(side="right", fill="y")


#---------------------------- Frame Termine -------------------------------------------
frame_terminee = Frame(listbox_frame, width=350)
frame_terminee.pack(side="left", fill="both", expand=True, padx=5, pady=5)
Label(frame_terminee, text="Terminée").pack(pady=5)

canvas_terminee = Canvas(frame_terminee ,highlightthickness=0)
scrollbar_terminee = Scrollbar(frame_terminee, orient="vertical", command=canvas_terminee.yview)
tasks_terminee_container = Frame(canvas_terminee)

tasks_terminee_container.bind(
    "<Configure>",
    lambda e: canvas_terminee.configure(scrollregion=canvas_terminee.bbox("all"))
)
canvas_terminee.bind(
    "<Configure>",
    lambda e: canvas_terminee.itemconfig(window_afaire, width=e.width)
)

canvas_terminee.create_window((0, 0), window=tasks_terminee_container, anchor="nw")
canvas_terminee.configure(yscrollcommand=scrollbar_terminee.set)

canvas_terminee.pack(side="left", fill="both", expand=True)
scrollbar_terminee.pack(side="right", fill="y")



buttons_frame = Frame(bottom_frame)
buttons_frame.place(relx=0, rely=0.8, relwidth=1, relheight=0.2)
# marquer_terminer= Button(buttons_frame, text="Terminer tache", state="disabled")
# marquer_terminer.pack(side="left")
# tache_suprimer = Button(buttons_frame, text="Supprimer tache", state="disabled")
# tache_modifier = Button(buttons_frame, text="Modifier tache", state="disabled")
# tache_suprimer.pack(side='right',padx=5)
# tache_modifier.pack(side='right',padx=5)
afficher_taches()
def _on_mousewheel(event, canvas):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

canvas_afaire.bind_all("<MouseWheel>", lambda e: _on_mousewheel(e, canvas_afaire))
canvas_encours.bind_all("<MouseWheel>", lambda e: _on_mousewheel(e, canvas_encours))
canvas_terminee.bind_all("<MouseWheel>", lambda e: _on_mousewheel(e, canvas_terminee))

app.mainloop()
