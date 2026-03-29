import os
import tkinter as tk
from tkinter import ttk, messagebox
import polysolver as ps
from polyparser import parse_challenge

def analyser_challenge(challenge):
        """Analyse les données pour extraire les particularités du challenge."""
        info = challenge["informationGeneralesSimulation"]
        
        nb_inter = len(challenge["listeIntersection"])
        nb_rues = len(challenge["listeStreet"])
        
        nb_voitures = 0
        total_rues_trajet = 0
        for d_voiture in challenge["listeCar"]:
            nb_voitures += len(d_voiture)
            for v in d_voiture.values():
                total_rues_trajet += len(v.streetsTraverse)
        
        avg_path = total_rues_trajet / nb_voitures
        densite = nb_voitures / nb_inter
        
        return {
            "D": info.duree,
            "Intersections": nb_inter,
            "Rues": nb_rues,
            "Voitures": nb_voitures,
            "AvgPath": round(avg_path, 1),
            "Densite": round(densite, 2)
        }

class PolySolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PolyHash Solver Interface")
        self.root.geometry("600x600")
        self.root.configure(padx=20, pady=20)

        # Titre
        self.label_title = tk.Label(root, text="Traffic Signaling Solver", font=("Arial", 16, "bold"))
        self.label_title.pack(pady=(0, 20))

        # Sélection du Challenge
        self.label_select = tk.Label(root, text="Sélectionnez un challenge :")
        self.label_select.pack(anchor="w")

        self.challenge_folder = "challenges/"
        self.files = self.get_challenge_files()
        
        self.combo_files = ttk.Combobox(root, values=self.files, state="readonly", width=40)
        self.combo_files.pack(pady=5)
        if self.files:
            self.combo_files.current(0)

        # Bouton de Lancement
        self.btn_run = tk.Button(root, text="Lancer la simulation", command=self.run_process, 
                                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), height=2)
        self.btn_run.pack(pady=20, fill="x")

        # Zone de Résultats et d'Analyses
        self.res_frame = tk.LabelFrame(root, text="Résultats & Analyse", padx=15, pady=10)
        self.res_frame.pack(fill="both", expand=True)

        self.label_score = tk.Label(self.res_frame, text="Score : --", font=("Courier", 12, "bold"))
        self.label_score.pack(pady=5)

        ttk.Separator(self.res_frame, orient='horizontal').pack(fill='x', pady=10)

        self.stats_label = tk.Label(self.res_frame, text="Sélectionnez un fichier pour l'analyse", 
                                    justify="left", font=("Consolas", 9), fg="#333")
        self.stats_label.pack(anchor="w")

        self.label_status = tk.Label(root, text="Statut : En attente de challenge", fg="gray", font=("Arial", 8))
        self.label_status.pack(pady=5)
        
        self.on_file_selected(None)
        
        self.combo_files.bind("<<ComboboxSelected>>", self.on_file_selected)

    def get_challenge_files(self):
        """Récupère la liste des fichiers dans le dossier challenges/"""
        if not os.path.exists(self.challenge_folder):
            os.makedirs(self.challenge_folder)
            return []
        return [f for f in os.listdir(self.challenge_folder) if f.endswith(".in")]
    
    def run_process(self):
        selected_file = self.combo_files.get()
        if not selected_file:
            messagebox.showwarning("Erreur", "Veuillez sélectionner un fichier.")
            return

        input_path = os.path.join(self.challenge_folder, selected_file)
        output_path = f"sortie/sortie.txt"

        try:
            self.label_status.config(text="Calcul en cours...", fg="blue")
            self.root.update_idletasks()

            # 1. Parsing
            challenge_data = parse_challenge(input_path) 
            
            # 2. Résolution
            solution = ps.resolution(challenge_data)

            # 3. Sauvegarde
            ps.sauvegarde_solution(output_path, solution)

            # 4. Calcul du Score
            score = ps.score_solution(challenge_data, solution)

            self.label_score.config(text=f"Score : {score}", fg="green")
            self.label_status.config(text=f"Terminé ! Solution sauvegardée.", fg="black")

        except Exception as e:
            self.label_status.config(text="Erreur lors du calcul"+str(e), fg="red")

    def on_file_selected(self, event):
        selected_file = self.combo_files.get()
        input_path = os.path.join(self.challenge_folder, selected_file)
        
        self.label_status.config(text=f"Analyse du challenge en cours...", fg="black")
        
        try:
            challenge_data = parse_challenge(input_path) 
            stats = analyser_challenge(challenge_data)
            
            # Mise à jour du texte des statistiques
            texte_stats = (
                f"Durée : {stats['D']}s | Voitures : {stats['Voitures']}\n"
                f"Intersections : {stats['Intersections']} | Rues : {stats['Rues']}\n"
                f"Moy. Rues/Trajet : {stats['AvgPath']} | Densité : {stats['Densite']} v/int\n"
            )
            self.stats_label.config(text=texte_stats)
            
            # Réinitialisation visuelle des champs de résultats précédents
            self.label_score.config(text="Score : --", fg="black")

        except Exception as e:
            self.stats_label.config(text=f"Erreur d'analyse : {str(e)}")
            
# Lancement de l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = PolySolverGUI(root)
    root.mainloop()