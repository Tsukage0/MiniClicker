import tkinter as tk
import math
import json
import os
import sys

# === Variables globales ===
score = 0
score_second = 0
temps = 5000
auto_clicks = 0
auto_click_cost = 50
auto_click_cost_incr = 1.05
speed = 0
speed_per = 0
speed_cost = 100
speed_cost_incr = 1.10
plus_click = 0
plus_click_cost = 500
plus_click_cost_incr = 1.20
shop_window = None
save_file = "save.json"

# === Chargement de la sauvegarde ===
def load_game():
    global score, temps, auto_clicks, auto_click_cost, plus_click, plus_click_cost, speed, speed_cost, speed_per
    if os.path.exists(save_file):
        with open(save_file, "r") as f:
            data = json.load(f)
            score = data.get("score", 0)
            temps = data.get("temps", 5000)
            auto_clicks = data.get("auto_clicks", 0)
            auto_click_cost = data.get("auto_click_cost", auto_click_cost)
            speed = data.get("speed", 0)
            speed_per = data.get("speed_per", 0)
            speed_cost = data.get("speed_cost", speed_cost)
            plus_click = data.get("plus_click", 0)
            plus_click_cost = data.get("plus_click_cost", plus_click_cost)

def save_game():
    data = {
        "_comment": "SVP, tricher pas, merci, ça serais surper cool de votre par",
        "score": score,
        "temps": temps,
        "auto_clicks": auto_clicks,
        "auto_click_cost": auto_click_cost,
        "speed": speed,
        "speed_per": speed_per,
        "speed_cost": speed_cost,
        "plus_click": plus_click,
        "plus_click_cost": plus_click_cost
    }
    with open(save_file, "w") as f:
        json.dump(data, f)

# Chemin d'accès à l'icône compatible PyInstaller
def resource_path(relative_path):
    try:
        # PyInstaller crée un dossier temporaire et y place les fichiers
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

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
    score += (1 + plus_click) * auto_clicks
    update_score()
    root.after(temps, auto_click)

def click_second():
    global score, score_second

    score_before = score

    def measure():
        global score_second
        score_after = score
        score_second = score_after - score_before
        label_score_second.config(text=f"Score/sec : {score_second}")
        root.after(1000, click_second)  # Recommence la boucle

    root.after(1000, measure)  # Appelle "measure" après 1 seconde

# === Fenêtre du shop ===
def open_shop():
    global shop_window

    if shop_window is not None and shop_window.winfo_exists():
        shop_window.lift()  # met au premier plan
        return

    shop_window = tk.Toplevel(root)
    shop_window.iconbitmap(resource_path("frog.ico"))
    shop_window.title("Shop")
    # --- Position intelligente de la fenêtre Shop ---
    shop_w = 500
    shop_h = 200

    root.update_idletasks()  # S'assurer que les dimensions sont à jour

    main_x = root.winfo_x()
    main_y = root.winfo_y()
    main_w = root.winfo_width()
    screen_w = root.winfo_screenwidth()

    # Essayer de mettre à droite
    shop_x = main_x + main_w + 10
    shop_y = main_y

    # Sinon, mettre à gauche si pas assez de place
    if shop_x + shop_w > screen_w:
        shop_x = main_x - shop_w - 10

    shop_window.geometry(f"{shop_w}x{shop_h}+{shop_x}+{shop_y}")

    def buy_auto_click():
        nonlocal btn_buy_auto, lbl_price_auto, lbl_auto_desc
        global score, auto_clicks, auto_click_cost
        if score >= auto_click_cost:
            score -= auto_click_cost
            auto_click_cost = math.ceil(auto_click_cost * auto_click_cost_incr)
            auto_clicks += 1
            update_score()
            lbl_price_auto.config(text=f"{auto_click_cost} points")
            lbl_auto_desc.config(text=f"Auto-Clickers : {auto_clicks}")
        else:
            original_text = f"{auto_click_cost} points"
            lbl_price_auto.config(text="Pas assez de points")
            lbl_price_auto.after(1000, lambda: lbl_price_auto.config(text=original_text))
    def buy_plus_click():
        nonlocal btn_buy_plus, lbl_price_plus, lbl_plus_desc
        global score, plus_click, plus_click_cost
        if score >= plus_click_cost:
            score -= plus_click_cost
            plus_click_cost = math.ceil(plus_click_cost * plus_click_cost_incr)
            plus_click += 1
            update_score()
            lbl_price_plus.config(text=f"{plus_click_cost} points")
            lbl_plus_desc.config(text=f"Points par auto-click : +{plus_click}")
        else:
            original_text = f"{plus_click_cost} points"
            lbl_price_plus.config(text="Pas assez de points")
            lbl_price_plus.after(1000, lambda: lbl_price_plus.config(text=original_text))
    def buy_speed():
        nonlocal btn_buy_speed, lbl_price_speed, lbl_speed_desc
        global score, speed, speed_cost, speed_per, temps
        if score >= speed_cost:
            score -= speed_cost
            speed_cost = math.ceil(speed_cost * speed_cost_incr)
            speed += 1
            speed_per = speed * 10
            temps = math.ceil(temps * 0.90 ** speed)
            #Max 130 mais je le passerais peut etre a 5% plutot
            update_score()
            lbl_price_speed.config(text=f"{speed_cost} points")
            lbl_speed_desc.config(text=f"Vitesse augmentée : +{speed_per}%")
        else:
            original_text = f"{speed_cost} points"
            lbl_price_speed.config(text="Pas assez de points")
            lbl_price_speed.after(1000, lambda: lbl_price_speed.config(text=original_text))


# === Conteneur principal du shop ===
    frame_item = tk.Frame(shop_window)
    frame_item.pack(pady=10, fill="x", padx=10)

# === Partie gauche : Boutons d'achat + Prix ===
    left_panel = tk.Frame(frame_item)
    left_panel.pack(side="left", padx=10)

# --- Auto Clicker ---
    btn_buy_auto = tk.Button(left_panel, text="Acheter Auto-Clicker", command=buy_auto_click)
    btn_buy_auto.pack(pady=(0, 2))

    lbl_price_auto = tk.Label(left_panel, text=f"{auto_click_cost} points")
    lbl_price_auto.pack()

    tk.Frame(left_panel, height=2, bd=1, relief="sunken", bg="grey").pack(fill="x", pady=8)

# --- Réduction de Temps ---
    btn_buy_speed = tk.Button(left_panel, text="Réduction Temps", command=buy_speed)
    btn_buy_speed.pack(pady=(0, 2))

    lbl_price_speed = tk.Label(left_panel, text=f"{speed_cost} points")
    lbl_price_speed.pack()

    tk.Frame(left_panel, height=2, bd=1, relief="sunken", bg="grey").pack(fill="x", pady=8)

# --- Plus de Click ---
    btn_buy_plus = tk.Button(left_panel, text="Plus de Click", command=buy_plus_click)
    btn_buy_plus.pack(pady=(0, 2))

    lbl_price_plus = tk.Label(left_panel, text=f"{plus_click_cost} points")
    lbl_price_plus.pack()

# === Partie droite : Descriptions ===
    right_panel = tk.Frame(frame_item)
    right_panel.pack(side="left", padx=10, anchor="w")

# --- Description Auto Clicker ---
    lbl_auto_desc = tk.Label(right_panel, text=f"Auto-Clickers : {auto_clicks}")
    lbl_auto_desc.pack(anchor="w")
    tk.Label(right_panel, text="Ajoute 1 point toutes les 5 secondes.").pack(anchor="w")

    tk.Frame(right_panel, height=2, bd=1, relief="sunken", bg="grey").pack(fill="x", pady=8)

# --- Description Réduction de Temps ---
    lbl_speed_desc = tk.Label(right_panel, text=f"Vitesse augmentée : +{speed_per}%")
    lbl_speed_desc.pack(anchor="w")
    tk.Label(right_panel, text="Rend les clicks auto 10% plus rapides.").pack(anchor="w")

    tk.Frame(right_panel, height=2, bd=1, relief="sunken", bg="grey").pack(fill="x", pady=8)

# --- Description Plus de Click ---
    lbl_plus_desc = tk.Label(right_panel, text=f"Points par auto-click : +{plus_click}")
    lbl_plus_desc.pack(anchor="w")
    tk.Label(right_panel, text="Chaque auto-click gagne +1 point.").pack(anchor="w")

# === Interface principale ===
root = tk.Tk()
root.title("Mini Clicker v1.0")
root.geometry("400x300")

label_score = tk.Label(root, text=f"Score : {score}", font=("Arial", 16))
label_score.pack()

label_score_second = tk.Label(root, text="Score/sec : 0", font=("Arial", 12))
label_score_second.pack()

btn_click = tk.Button(root, text="Clique ici !", font=("Arial", 14), width=15, height=2, command=click)
btn_click.pack(pady=10)

btn_shop = tk.Button(root, text="Shop", command=open_shop)
btn_shop.pack(pady=10)

# === Lancer le jeu ===
update_score()
auto_click()
click_second()
root.iconbitmap(resource_path("frog.ico"))
root.mainloop()