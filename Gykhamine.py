import hashlib
import time
import customtkinter as ctk
import tkinter as tk
from tkinter import scrolledtext, messagebox

# --- Partie 1 : Logique de la Blockchain (Reprise et Légèrement Adaptée) ---

class Transaction:
    """Représente une transaction dans la blockchain."""
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def __repr__(self):
        return f"De: {self.sender}, À: {self.recipient}, Montant: {self.amount}"

class Block:
    """Représente un bloc dans la blockchain."""
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """Calcule le hachage SHA256 du bloc."""
        # Assurez-vous que les transactions sont sérialisables (converties en str)
        transactions_str = "".join([str(t) for t in self.transactions])
        block_string = (
            str(self.index) +
            transactions_str +
            str(self.timestamp) +
            str(self.previous_hash) +
            str(self.nonce)
        )
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    """Gère la chaîne de blocs."""
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.difficulty = 2  # Nombre de zéros requis pour le PoW
        self.create_genesis_block()

    def create_genesis_block(self):
        """Crée le premier bloc de la chaîne (bloc de genèse)."""
        genesis_block = Block(0, [], time.time(), "0")
        self.chain.append(genesis_block)

    def get_last_block(self):
        """Retourne le dernier bloc de la chaîne."""
        return self.chain[-1]

    def proof_of_work(self, block):
        """Trouve un 'nonce' qui satisfait la difficulté du minage."""
        print("Démarrage du minage...")
        while block.hash[:self.difficulty] != "0" * self.difficulty:
            block.nonce += 1
            block.hash = block.calculate_hash()
        print(f"Bloc miné : {block.hash}")

    def mine_pending_transactions(self, miner_address="Miner Générique"):
        """Mine un nouveau bloc avec les transactions en attente."""
        if not self.pending_transactions:
            print("Aucune transaction en attente à miner.")
            return None

        last_block = self.get_last_block()
        new_index = last_block.index + 1
        current_timestamp = time.time()

        # Créer le nouveau bloc avec les transactions en attente
        new_block = Block(
            new_index,
            list(self.pending_transactions), # Copie les transactions
            current_timestamp,
            last_block.hash
        )

        self.proof_of_work(new_block)

        # Ajoute le bloc à la chaîne
        self.chain.append(new_block)
        self.pending_transactions = [] # Vide les transactions en attente

        print(f"Nouveau bloc #{new_block.index} ajouté à la chaîne.")
        return new_block

    def add_transaction(self, sender, recipient, amount):
        """Ajoute une nouvelle transaction à la liste des transactions en attente."""
        try:
            amount = float(amount)
            if amount <= 0:
                print("Le montant doit être positif.")
                return False
            transaction = Transaction(sender, recipient, amount)
            self.pending_transactions.append(transaction)
            print(f"Transaction ajoutée : {transaction}")
            return True
        except ValueError:
            print("Montant invalide. Veuillez entrer un nombre.")
            return False

    def is_chain_valid(self):
        """Vérifie l'intégrité de toute la chaîne."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            # Vérifie si le hachage du bloc actuel est correct
            if current_block.hash != current_block.calculate_hash():
                print(f"Erreur d'intégrité : Hachage du bloc {current_block.index} invalide.")
                return False

            # Vérifie si le hachage précédent pointe vers le bon bloc
            if current_block.previous_hash != previous_block.hash:
                print(f"Erreur d'intégrité : Lien du bloc {current_block.index} brisé.")
                return False
        return True

# --- Partie 2 : Interface Graphique avec CustomTkinter ---

class BlockchainGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Ma Blockchain Simplifiée avec CustomTkinter")
        self.geometry("1000x700")

        # Configurer la grille pour le redimensionnement
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Instance de la blockchain
        self.blockchain = Blockchain()

        # --- Cadre Principal ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1) # Pour la zone de texte

        # --- Section Ajout de Transaction ---
        self.transaction_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.transaction_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.transaction_frame.grid_columnconfigure(0, weight=1)
        self.transaction_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.transaction_frame, text="Ajouter une Transaction").grid(row=0, column=0, columnspan=2, pady=5)

        ctk.CTkLabel(self.transaction_frame, text="Expéditeur:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.sender_entry = ctk.CTkEntry(self.transaction_frame, placeholder_text="Alice")
        self.sender_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(self.transaction_frame, text="Destinataire:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.recipient_entry = ctk.CTkEntry(self.transaction_frame, placeholder_text="Bob")
        self.recipient_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(self.transaction_frame, text="Montant:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.amount_entry = ctk.CTkEntry(self.transaction_frame, placeholder_text="10.5")
        self.amount_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkButton(self.transaction_frame, text="Ajouter Transaction", command=self.add_transaction_gui).grid(row=4, column=0, columnspan=2, pady=10)

        # --- Section Minage et Validation ---
        self.actions_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.actions_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.actions_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.actions_frame, text="Actions Blockchain").grid(row=0, column=0, pady=5)
        ctk.CTkButton(self.actions_frame, text="Miner un nouveau Bloc", command=self.mine_block_gui).grid(row=1, column=0, pady=10)
        ctk.CTkButton(self.actions_frame, text="Vérifier l'Intégrité de la Chaîne", command=self.check_chain_validity_gui).grid(row=2, column=0, pady=10)

        # --- Zone d'affichage de la Blockchain ---
        self.display_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.display_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.display_frame.grid_rowconfigure(0, weight=1)
        self.display_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.display_frame, text="État Actuel de la Blockchain").grid(row=0, column=0, sticky="ew", pady=5)
        self.blockchain_text_display = scrolledtext.ScrolledText(self.display_frame, wrap=tk.WORD, width=80, height=20, font=("Cascadia Code", 10), bg="#2b2b2b", fg="#ffffff", insertbackground="#ffffff")
        self.blockchain_text_display.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.blockchain_text_display.config(state='disabled') # Rendre la zone de texte non éditable

        # Mettre à jour l'affichage au démarrage
        self.update_blockchain_display()

    def add_transaction_gui(self):
        """Récupère les entrées de l'interface et ajoute une transaction."""
        sender = self.sender_entry.get()
        recipient = self.recipient_entry.get()
        amount = self.amount_entry.get()

        if not sender or not recipient or not amount:
            messagebox.showwarning("Entrée Manquante", "Veuillez remplir tous les champs de la transaction.")
            return

        if self.blockchain.add_transaction(sender, recipient, amount):
            messagebox.showinfo("Transaction Ajoutée", "Transaction ajoutée avec succès aux transactions en attente.")
            self.sender_entry.delete(0, ctk.END)
            self.recipient_entry.delete(0, ctk.END)
            self.amount_entry.delete(0, ctk.END)
            self.update_blockchain_display()
        else:
            messagebox.showerror("Erreur de Transaction", "Impossible d'ajouter la transaction. Vérifiez le montant.")


    def mine_block_gui(self):
        """Déclenche le minage d'un nouveau bloc via l'interface."""
        if not self.blockchain.pending_transactions:
            messagebox.showinfo("Pas de Transaction", "Aucune transaction en attente. Ajoutez-en avant de miner.")
            return

        # Afficher un message pendant le minage (peut prendre du temps)
        self.blockchain_text_display.config(state='normal')
        self.blockchain_text_display.insert(tk.END, "\nMinage en cours... Veuillez patienter...\n")
        self.blockchain_text_display.config(state='disabled')
        self.update_idletasks() # Met à jour l'interface

        # Le minage peut bloquer l'interface, idéalement il faudrait le faire dans un thread séparé
        # Pour cet exemple simple, nous le faisons directement.
        mined_block = self.blockchain.mine_pending_transactions()

        if mined_block:
            messagebox.showinfo("Minage Terminé", f"Bloc #{mined_block.index} miné et ajouté à la chaîne!")
        else:
            messagebox.showinfo("Minage Annulé", "Aucune transaction à miner.")

        self.update_blockchain_display()

    def check_chain_validity_gui(self):
        """Vérifie et affiche l'intégrité de la chaîne."""
        if self.blockchain.is_chain_valid():
            messagebox.showinfo("Vérification de l'Intégrité", "La chaîne est valide ! Aucune altération détectée.")
        else:
            messagebox.showerror("Vérification de l'Intégrité", "La chaîne est INVALIDE ! Des altérations ont été détectées.")
        self.update_blockchain_display()

    def update_blockchain_display(self):
        """Met à jour le contenu de la zone de texte affichant la blockchain."""
        self.blockchain_text_display.config(state='normal')
        self.blockchain_text_display.delete(1.0, tk.END)

        self.blockchain_text_display.insert(tk.END, "--- État Actuel de la Blockchain ---\n\n")

        for block in self.blockchain.chain:
            self.blockchain_text_display.insert(tk.END, f"Block #{block.index}\n")
            self.blockchain_text_display.insert(tk.END, f"  Horodatage: {time.ctime(block.timestamp)}\n")
            self.blockchain_text_display.insert(tk.END, f"  Hash Précédent: {block.previous_hash}\n")
            self.blockchain_text_display.insert(tk.END, f"  Hash Actuel: {block.hash}\n")
            self.blockchain_text_display.insert(tk.END, f"  Nonce: {block.nonce}\n")
            self.blockchain_text_display.insert(tk.END, "  Transactions:\n")
            if block.transactions:
                for tx in block.transactions:
                    self.blockchain_text_display.insert(tk.END, f"    - {tx}\n")
            else:
                self.blockchain_text_display.insert(tk.END, "    (Aucune transaction)\n")
            self.blockchain_text_display.insert(tk.END, "-" * 50 + "\n\n")

        self.blockchain_text_display.insert(tk.END, "--- Transactions en Attente ---\n")
        if self.blockchain.pending_transactions:
            for tx in self.blockchain.pending_transactions:
                self.blockchain_text_display.insert(tk.END, f"- {tx}\n")
        else:
            self.blockchain_text_display.insert(tk.END, "Aucune transaction en attente.\n")

        self.blockchain_text_display.config(state='disabled')


# --- Point d'entrée de l'application ---
if __name__ == "__main__":
    ctk.set_appearance_mode("System")  # Modes: "System" (par défaut), "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Thèmes: "blue" (par défaut), "green", "dark-blue"

    app = BlockchainGUI()
    app.mainloop()