import tkinter as tk
import mysql.connector

#POWERED BY ONE
class Application:
    def __init__(self, master):
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        # Connexion à la base de données
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="employes",
            ssl_disabled=True
        )
        self.c = self.conn.cursor()
        

        # Création de la table employes
        self.c.execute('''CREATE TABLE IF NOT EXISTS employes (
                       id INTEGER PRIMARY KEY AUTO_INCREMENT,
                       nom TEXT,
                       prenom TEXT,
                       salaire INT,
                       id_service INT
                   )''')

        

        # Création des widgets
        self.nom_label = tk.Label(self.master, text="Nom:")
        self.nom_label.grid(row=0, column=0)
        self.nom_entry = tk.Entry(self.master)
        self.nom_entry.grid(row=0, column=1)

        self.prenom_label = tk.Label(self.master, text="Prénom:")
        self.prenom_label.grid(row=1, column=0)
        self.prenom_entry = tk.Entry(self.master)
        self.prenom_entry.grid(row=1, column=1)

        self.salaire_label = tk.Label(self.master, text="Salaire:")
        self.salaire_label.grid(row=2, column=0)
        self.salaire_entry = tk.Entry(self.master)
        self.salaire_entry.grid(row=2, column=1)
        
        self.id_service_label = tk.Label(self.master, text="id_service:")
        self.id_service_label.grid(row=3, column=0)
        self.id_service_entry = tk.Entry(self.master)
        self.id_service_entry.grid(row=3, column=1)

        self.id_label = tk.Label(self.master, text="ID a supprimer:")
        self.id_label.grid(row=4, column=0)
        self.id_entry = tk.Entry(self.master)
        self.id_entry.grid(row=4, column=1) 

        self.ajouter_button = tk.Button(self.master, text="Ajouter", command=self.ajouter_employe)
        self.ajouter_button.grid(row=5, columnspan=2)
        
        self.supprimer_button = tk.Button(self.master, text="Supprimer", command=self.supprimer_employe)
        self.supprimer_button.grid(row=7, columnspan=2)
        
        self.ajouter_button = tk.Button(self.master, text="Afficher les données", command=self.afficher_donnees)
        self.ajouter_button.grid(row=6, columnspan=2)

    def ajouter_employe(self):
        # Récupération des valeurs des champs
        nom = self.nom_entry.get()
        prenom = self.prenom_entry.get()
        salaire = int(self.salaire_entry.get())
        id_service = int(self.id_service_entry.get())

        # Ajout de l'employé à la base de données
        sql = "INSERT INTO employes (nom, prenom, salaire, id_service) VALUES (%s, %s, %s, %s)"
        val = (nom, prenom, salaire, id_service)
        self.c.execute(sql, val)
        
        # Validation de la transaction
        self.conn.commit()

    def supprimer_employe(self):
        # Récupération de l'ID de l'employé à supprimer
        id_employe = int(self.id_entry.get())

    # Suppression de l'employé de la base de données
        sql = "DELETE FROM employes WHERE id = %s"
        val = (id_employe,)
        self.c.execute(sql, val)

    # Validation de la transaction
        self.conn.commit()
    

    def afficher_donnees(self):
        self.c.execute("SELECT * FROM employes")
        rows = self.c.fetchall()
        top = tk.Toplevel(self.master)
        tk.Label(top, text="ID").grid(row=0, column=0)
        tk.Label(top, text="Nom").grid(row=0, column=1)
        tk.Label(top, text="Prénom").grid(row=0, column=2)
        tk.Label(top, text="Salaire").grid(row=0, column=3)
        tk.Label(top, text="ID service").grid(row=0, column=4)
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                tk.Label(top, text=value).grid(row=i+1, column=j)
            tk.Button(top, text="Modifier", command=lambda row=row: self.modifier_employe(row)).grid(row=i+1, column=5)
        tk.Button(top, text="Fermer", command=top.destroy).grid(row=len(rows)+1, columnspan=6)


    def modifier_employe(self, row):
    # Créer une nouvelle fenêtre pour la modification
        top = tk.Toplevel(self.master)
    
    # Créer les widgets pour la saisie des nouvelles valeurs
        tk.Label(top, text="Nom").grid(row=0, column=0)
        nom_entry = tk.Entry(top)
        nom_entry.grid(row=0, column=1)
    
        tk.Label(top, text="Prénom").grid(row=1, column=0)
        prenom_entry = tk.Entry(top)
        prenom_entry.grid(row=1, column=1)
    
        tk.Label(top, text="Salaire").grid(row=2, column=0)
        salaire_entry = tk.Entry(top)
        salaire_entry.grid(row=2, column=1)
    
        tk.Label(top, text="ID service").grid(row=3, column=0)
        id_service_entry = tk.Entry(top)
        id_service_entry.grid(row=3, column=1)
    
    # Récupérer les anciennes valeurs de la ligne sélectionnée
        id_employe = row[0]
        nom = row[1]
        prenom = row[2]
        salaire = row[3]
        id_service = row[4]
    
    # Afficher les anciennes valeurs dans les widgets de saisie
        nom_entry.insert(0, nom)
        prenom_entry.insert(0, prenom)
        salaire_entry.insert(0, salaire)
        id_service_entry.insert(0, id_service)
    
    # Définir la fonction pour enregistrer les nouvelles valeurs
        def enregistrer():
        # Récupérer les nouvelles valeurs saisies
            nouveau_nom = nom_entry.get()
            nouveau_prenom = prenom_entry.get()
            nouveau_salaire = float(salaire_entry.get())
            nouveau_id_service = int(id_service_entry.get())
        
        # Mettre à jour les valeurs dans la base de données
            sql = "UPDATE employes SET nom = %s, prenom = %s, salaire = %s, id_service = %s WHERE id = %s"
            val = (nouveau_nom, nouveau_prenom, nouveau_salaire, nouveau_id_service, id_employe)
            self.c.execute(sql, val)
            self.conn.commit()
        
        # Mettre à jour les valeurs affichées dans la fenêtre "Afficher les données"
            self.afficher_donnees()
        
        # Fermer la fenêtre de modification
            top.destroy()
    
    # Ajouter un bouton pour enregistrer les nouvelles valeurs
        tk.Button(top, text="Enregistrer", command=enregistrer).grid(row=4, column=0, columnspan=2)



root = tk.Tk()
app = Application(root)
root.mainloop()