import os
import json
import tkinter as tk
from tkinter import ttk, messagebox

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'assets', 'js', 'evenements.js')

os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)


def load_events():
    """Charge les prochaines sorties depuis assets/js/evenements.js"""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        start = content.find('[')
        end = content.rfind(']')
        if start == -1 or end == -1 or end <= start:
            return []
        data = content[start:end+1]
        return json.loads(data)
    except Exception:
        return []


def save_events(events):
    """Sauvegarde les prochaines sorties dans assets/js/evenements.js"""
    content = "const evenements = " + json.dumps(events, ensure_ascii=False, indent=2) + ";\n\nwindow.evenementsData = evenements;\n"
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        f.write(content)


class EventEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Gestion des Prochaines Sorties')
        self.geometry('750x450')

        self.events = load_events()

        # Barre d'outils
        toolbar = ttk.Frame(self)
        toolbar.pack(fill='x', padx=10, pady=10)

        ttk.Button(toolbar, text='Ajouter une sortie', command=self.add_event).pack(side='left', padx=5)
        ttk.Button(toolbar, text='Modifier la sortie', command=self.edit_event).pack(side='left', padx=5)
        ttk.Button(toolbar, text='Supprimer la sortie', command=self.delete_event).pack(side='left', padx=5)

        # Tableau des sorties (Jour / Heure | Type | Rendez-vous)
        columns = ('jourHeure', 'type', 'rendezVous')
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        self.tree.heading('jourHeure', text='Jour / Heure')
        self.tree.heading('type', text='Type')
        self.tree.heading('rendezVous', text='Rendez-vous')

        self.tree.column('jourHeure', width=180)
        self.tree.column('type', width=250)
        self.tree.column('rendezVous', width=250)

        self.tree.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        self.refresh_list()

    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for event in self.events:
            self.tree.insert('', 'end', values=(
                event.get('jourHeure', ''),
                event.get('type', ''),
                event.get('rendezVous', '')
            ))
        save_events(self.events)

    def add_event(self):
        self.open_dialog()

    def edit_event(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Attention', 'Veuillez sélectionner une sortie à modifier.')
            return
        index = self.tree.index(selected[0])
        self.open_dialog(self.events[index], index)

    def delete_event(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Attention', 'Veuillez sélectionner une sortie à supprimer.')
            return
        if messagebox.askyesno('Confirmation', 'Voulez-vous vraiment supprimer cette sortie ?'):
            index = self.tree.index(selected[0])
            del self.events[index]
            self.refresh_list()

    def open_dialog(self, event=None, index=None):
        dialog = tk.Toplevel(self)
        dialog.title('Modifier la sortie' if event else 'Ajouter une sortie')
        dialog.geometry('450x300')
        dialog.grab_set()

        # Champ 1 : Jour / Heure
        tk.Label(dialog, text='Jour / Heure').pack(anchor='w', padx=10, pady=(10, 2))
        jour_entry = ttk.Entry(dialog, width=50)
        jour_entry.pack(padx=10, fill='x')

        # Champ 2 : Type
        tk.Label(dialog, text='Type').pack(anchor='w', padx=10, pady=(8, 2))
        type_entry = ttk.Entry(dialog, width=50)
        type_entry.pack(padx=10, fill='x')

        # Champ 3 : Rendez-vous
        tk.Label(dialog, text='Rendez-vous').pack(anchor='w', padx=10, pady=(8, 2))
        lieu_entry = ttk.Entry(dialog, width=50)
        lieu_entry.pack(padx=10, fill='x')

        # Pré-remplissage si modification
        if event:
            jour_entry.insert(0, event.get('jourHeure', ''))
            type_entry.insert(0, event.get('type', ''))
            lieu_entry.insert(0, event.get('rendezVous', ''))

        def validate():
            new_event = {
                'jourHeure': jour_entry.get().strip(),
                'type': type_entry.get().strip(),
                'rendezVous': lieu_entry.get().strip(),
            }
            if not new_event['jourHeure'] or not new_event['type'] or not new_event['rendezVous']:
                messagebox.showwarning('Attention', 'Tous les champs sont obligatoires.')
                return

            if index is None:
                self.events.append(new_event)
            else:
                self.events[index] = new_event

            self.refresh_list()
            dialog.destroy()

        ttk.Button(dialog, text='Enregistrer', command=validate).pack(pady=20)


if __name__ == '__main__':
    app = EventEditor()
    app.mainloop()