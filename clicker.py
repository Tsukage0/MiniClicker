import tkinter as tk
import math
import json
import os

# === Variables globales ===
score = 0
auto_clicks = 0
auto_click_cost = 50
save_file = "save.json"

# === Chargement de la sauvegarde ===
def load_game():
    global score, auto_clicks, auto_click_cost
    if os.path.exists(save_file):
        with open(save_file, "r") as f:
            data = json.load(f)
            score = data.get("score", 0)
            auto_clicks = data.get("auto_clicks", 0)
            auto_click_cost = data.get("auto_click_cost", 50)

def save_game():
    data = {
        "score": score,
        "auto_clicks": auto_clicks,
        "auto_click_cost": auto_click_cost
    }
    with open(save_file, "w") as f:
        json.dump(data, f)

# Charger les données avant l'interface
load_game()

# === Fonctions principales ===
def update_score():
    label_score.config(text=f"Score : {score}")
    save_game()

def click():
    global score
    score += 1
    update_score()

def auto_click():
    global score
    score += auto_clicks
    update_score()
    root.after(1000, auto_click)

# === Fenêtre du shop ===
def open_shop():
    shop_window = tk.Toplevel(root)
    shop_window.title("Shop")
    shop_window.geometry("500x200")

    def buy_auto_click():
        nonlocal btn_buy, lbl_price, lbl_autoclicks
        global score, auto_clicks, auto_click_cost
        if score >= auto_click_cost:
            score -= auto_click_cost
            auto_click_cost = math.ceil(auto_click_cost * 1.05)
            auto_clicks += 1
            update_score()
            lbl_price.config(text=f"({auto_click_cost} points)")
            lbl_autoclicks.config(text=f"Auto-Clicker ({auto_clicks})")
        else:
            lbl_price.config(text="Pas assez de points")

    # Conteneur horizontal
    frame_item = tk.Frame(shop_window)
    frame_item.pack(pady=10, fill="x", padx=10)

    # Partie gauche : bouton + prix
    left = tk.Frame(frame_item)
    left.pack(side="left", padx=10)

    btn_buy = tk.Button(left, text="Acheter", command=buy_auto_click)
    btn_buy.pack()

    lbl_price = tk.Label(left, text=f"({auto_click_cost} points)")
    lbl_price.pack()

    # Partie droite : description
    right = tk.Frame(frame_item)
    right.pack(side="left", padx=10, anchor="w")

    lbl_autoclicks = tk.Label(right, text=f"Auto-Clicker ({auto_clicks})")
    lbl_autoclicks.pack(anchor="w")

    tk.Label(right, text="Gagne 1 point automatiquement par seconde.").pack(anchor="w")

# === Interface principale ===
root = tk.Tk()
root.title("Mini Clicker")
root.geometry("400x300")

label_score = tk.Label(root, text=f"Score : {score}", font=("Arial", 16))
label_score.pack(pady=10)

btn_click = tk.Button(root, text="Clique ici !", font=("Arial", 14), width=15, height=2, command=click)
btn_click.pack(pady=10)

btn_shop = tk.Button(root, text="Shop", command=open_shop)
btn_shop.pack(pady=10)

# === Lancer le jeu ===
update_score()
auto_click()
root.mainloop()