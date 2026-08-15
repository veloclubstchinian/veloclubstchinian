import json
import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
UPLOADS_DIR = ROOT / "assets" / "images" / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

FILES = {
    "sorties": DATA_DIR / "sorties_exceptionnelles.js",
    "competitions": DATA_DIR / "competitions.js",
    "evenements": DATA_DIR / "evenements.js",
    "circuits": DATA_DIR / "circuits_favoris.js"
}


def load_data(file_path):
    if not file_path.exists():
        return []
    try:
        content = file_path.read_text(encoding="utf-8")
        start = content.find("[")
        end = content.rfind("]")
        if start == -1 or end == -1 or end <= start:
            return []
        array_text = content[start:end + 1]
        return json.loads(array_text)
    except Exception:
        return []


def save_data(file_path, entries):
    variable_name = {
        "sorties_exceptionnelles.js": "sortiesExceptionnellesData",
        "competitions.js": "competitionsData",
        "evenements.js": "evenementsData",
        "circuits_favoris.js": "circuitsData"
    }[file_path.name]
    payload = f"const {variable_name} = {json.dumps(entries, ensure_ascii=False, indent=2)};\n\nwindow.{variable_name} = {variable_name};\n"
    file_path.write_text(payload, encoding="utf-8")


class SiteManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestion du site - Sorties et Compétitions")
        self.geometry("900x620")
        self.resizable(False, False)

        self.mode_var = tk.StringVar(value="sorties")
        self.mode_display_var = tk.StringVar(value="Sorties exceptionnelles")
        self.entries = []
        self.current_index = None
        self.mode_labels = {
            "sorties": "Sorties exceptionnelles",
            "competitions": "Compétitions",
            "evenements": "Événements",
            "circuits": "Circuits favoris",
        }

        self.geometry("1100x760")
        self.minsize(980, 680)
        self.resizable(True, True)

        main_container = ttk.Frame(self, padding=10)
        main_container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(main_container, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.form_frame = ttk.Frame(self.canvas, padding=10)
        self.canvas.create_window((0, 0), window=self.form_frame, anchor="nw")
        self.form_frame.bind("<Configure>", lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        ttk.Label(self.form_frame, text="Type de contenu", font=("Segoe UI", 11)).grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))
        self.mode_combo = ttk.Combobox(self.form_frame, textvariable=self.mode_display_var, state="readonly", width=35)
        self.mode_combo["values"] = list(self.mode_labels.values())
        self.mode_combo.grid(row=1, column=0, sticky="w", padx=10, pady=(4, 10))
        self.mode_combo.bind("<<ComboboxSelected>>", self.on_mode_selected)

        ttk.Label(self.form_frame, text="Nom", font=("Segoe UI", 11)).grid(row=2, column=0, sticky="w", padx=10, pady=(10, 0))
        self.nom_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.nom_var, width=90).grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        ttk.Label(self.form_frame, text="Date", font=("Segoe UI", 11)).grid(row=4, column=0, sticky="w", padx=10, pady=(10, 0))
        self.date_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.date_var, width=90).grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        ttk.Label(self.form_frame, text="Description", font=("Segoe UI", 11)).grid(row=6, column=0, sticky="w", padx=10, pady=(10, 0))
        self.description_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.description_var, width=90).grid(row=7, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        ttk.Label(self.form_frame, text="Distance", font=("Segoe UI", 11)).grid(row=8, column=0, sticky="w", padx=10, pady=(10, 0))
        self.distance_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.distance_var, width=90).grid(row=9, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        ttk.Label(self.form_frame, text="Dénivelé", font=("Segoe UI", 11)).grid(row=10, column=0, sticky="w", padx=10, pady=(10, 0))
        self.denivele_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.denivele_var, width=90).grid(row=11, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        ttk.Label(self.form_frame, text="Difficulté", font=("Segoe UI", 11)).grid(row=12, column=0, sticky="w", padx=10, pady=(10, 0))
        self.difficulte_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.difficulte_var, width=90).grid(row=13, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        ttk.Label(self.form_frame, text="Lien / URL", font=("Segoe UI", 11)).grid(row=14, column=0, sticky="w", padx=10, pady=(10, 0))
        self.link_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.link_var, width=90).grid(row=15, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        ttk.Label(self.form_frame, text="Image principale (facultative)", font=("Segoe UI", 11)).grid(row=16, column=0, sticky="w", padx=10, pady=(10, 0))
        self.image_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.image_var, width=90).grid(row=17, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        ttk.Label(self.form_frame, text="Photos sélectionnées", font=("Segoe UI", 11)).grid(row=18, column=0, sticky="w", padx=10, pady=(10, 0))
        self.photos_list = tk.Listbox(self.form_frame, height=8, width=100)
        self.photos_list.grid(row=19, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        button_frame = ttk.Frame(self.form_frame)
        button_frame.grid(row=20, column=0, columnspan=2, pady=10, sticky="w")
        ttk.Button(button_frame, text="Choisir des photos", command=self.choose_photos).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Nouveau", command=self.new_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Enregistrer", command=self.save_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Supprimer", command=self.delete_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Retirer la sélection", command=self.remove_selected_photo).pack(side=tk.LEFT, padx=5)

        self.listbox = tk.Listbox(self.form_frame, width=120, height=10)
        self.listbox.grid(row=21, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.listbox.bind("<<ListboxSelect>>", self.select_entry)

        self.form_frame.grid_columnconfigure(0, weight=1)
        self.form_frame.grid_columnconfigure(1, weight=1)

        self.switch_mode()
        self.after(100, lambda: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def on_mode_selected(self, event=None):
        selected = self.mode_display_var.get()
        reverse_map = {value: key for key, value in self.mode_labels.items()}
        if selected in reverse_map:
            self.mode_var.set(reverse_map[selected])
            self.switch_mode()

    def switch_mode(self):
        mode = self.mode_var.get()
        self.entries = load_data(FILES[mode])
        self.current_index = None
        self.nom_var.set("")
        self.date_var.set("")
        self.description_var.set("")
        self.distance_var.set("")
        self.denivele_var.set("")
        self.difficulte_var.set("")
        self.link_var.set("")
        self.image_var.set("")
        self.photos_list.delete(0, tk.END)
        self.refresh_list()

    def choose_photos(self):
        files = filedialog.askopenfilenames(filetypes=[("Images", "*.png *.jpg *.jpeg *.gif *.webp")])
        if not files:
            return
        for path in files:
            source = Path(path)
            if not source.exists():
                continue
            filename = source.name
            dest = UPLOADS_DIR / filename
            counter = 1
            while dest.exists():
                dest = UPLOADS_DIR / f"{source.stem}_{counter}{source.suffix}"
                counter += 1
            shutil.copy2(source, dest)
            rel_path = os.path.relpath(dest, ROOT).replace("\\", "/")
            if rel_path not in [self.photos_list.get(i) for i in range(self.photos_list.size())]:
                self.photos_list.insert(tk.END, rel_path)

    def new_entry(self):
        self.current_index = None
        self.nom_var.set("")
        self.date_var.set("")
        self.description_var.set("")
        self.distance_var.set("")
        self.denivele_var.set("")
        self.difficulte_var.set("")
        self.link_var.set("")
        self.image_var.set("")
        self.photos_list.delete(0, tk.END)

    def remove_selected_photo(self):
        selection = self.photos_list.curselection()
        if not selection:
            return
        self.photos_list.delete(selection[0])

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for entry in self.entries:
            self.listbox.insert(tk.END, f"{entry.get('nom', '')} - {entry.get('date', '')}")

    def select_entry(self, event):
        selection = self.listbox.curselection()
        if not selection:
            return
        idx = selection[0]
        self.current_index = idx
        entry = self.entries[idx]
        self.nom_var.set(entry.get("nom", ""))
        self.date_var.set(entry.get("date", ""))
        self.description_var.set(entry.get("description", ""))
        self.distance_var.set(entry.get("distance", ""))
        self.denivele_var.set(entry.get("denivele", ""))
        self.difficulte_var.set(entry.get("difficulte", ""))
        self.link_var.set(entry.get("lienGps", entry.get("link", "")))
        self.image_var.set(entry.get("image", ""))
        self.photos_list.delete(0, tk.END)
        for photo in entry.get("photos", []):
            self.photos_list.insert(tk.END, photo)

    def save_entry(self):
        name = self.nom_var.get().strip()
        date = self.date_var.get().strip()
        if not name:
            name = "Sans nom"
        if not date:
            date = ""
        description = self.description_var.get().strip()
        distance = self.distance_var.get().strip()
        denivele = self.denivele_var.get().strip()
        difficulte = self.difficulte_var.get().strip()
        link = self.link_var.get().strip()
        image = self.image_var.get().strip()
        photos = [self.make_relative_path(self.photos_list.get(i)) for i in range(self.photos_list.size())]
        entry_data = {"nom": name, "date": date, "photos": photos}
        if description:
            entry_data["description"] = description
        if distance:
            entry_data["distance"] = distance
        if denivele:
            entry_data["denivele"] = denivele
        if difficulte:
            entry_data["difficulte"] = difficulte
        if link:
            entry_data["lienGps"] = link
        if image:
            entry_data["image"] = self.make_relative_path(image)
        if self.current_index is None:
            self.entries.append(entry_data)
        else:
            self.entries[self.current_index] = entry_data
        save_data(FILES[self.mode_var.get()], self.entries)
        self.refresh_list()
        messagebox.showinfo("Enregistré", "Le contenu a bien été enregistré.")

    def delete_entry(self):
        if self.current_index is None:
            messagebox.showwarning("Attention", "Sélectionne d'abord un élément à supprimer.")
            return
        del self.entries[self.current_index]
        save_data(FILES[self.mode_var.get()], self.entries)
        self.current_index = None
        self.nom_var.set("")
        self.date_var.set("")
        self.description_var.set("")
        self.distance_var.set("")
        self.denivele_var.set("")
        self.difficulte_var.set("")
        self.link_var.set("")
        self.image_var.set("")
        self.photos_list.delete(0, tk.END)
        self.refresh_list()
        messagebox.showinfo("Supprimé", "L'élément a bien été supprimé.")

    def make_relative_path(self, path):
        if not path:
            return ""
        path_str = str(path).strip()
        if not path_str:
            return ""
        candidate = Path(path_str)
        if candidate.is_absolute():
            try:
                return os.path.relpath(candidate, ROOT).replace("\\", "/")
            except ValueError:
                return path_str.replace("\\", "/")
        return path_str.replace("\\", "/")


if __name__ == "__main__":
    app = SiteManagerApp()
    app.mainloop()
