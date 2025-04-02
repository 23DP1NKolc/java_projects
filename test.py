import tkinter as tk
from tkinter import messagebox
import time
import threading
import json

# Balsošanas beigu datums (1. aprīlis šajā gadā)
END_DATE = "2025-04-01 00:00:00"

# Žanri un mūziķi
genres = {
    "Roks": ["Mūziķis A", "Mūziķis B", "Mūziķis C", "Mūziķis D", "Mūziķis E"],
    "Pops": ["Mūziķis F", "Mūziķis G", "Mūziķis H", "Mūziķis I", "Mūziķis J"],
    "Džezs": ["Mūziķis K", "Mūziķis L", "Mūziķis M", "Mūziķis N", "Mūziķis O"],
    "Hip-hops": ["Mūziķis P", "Mūziķis Q", "Mūziķis R", "Mūziķis S", "Mūziķis T"],
    "Elektronika": ["Mūziķis U", "Mūziķis V", "Mūziķis W", "Mūziķis X", "Mūziķis Y"]
}

# Izveidojam galveno logu
root = tk.Tk()
root.title("Balsošana par mūziķiem")
root.geometry("400x500")

# Lietotāja izvēles saglabāšana
user_votes = {genre: tk.StringVar() for genre in genres}

# Funkcija, lai atjauninātu laika atskaiti
def update_timer():
    while True:
        now = time.time()
        end_time = time.mktime(time.strptime(END_DATE, "%Y-%m-%d %H:%M:%S"))
        remaining = int(end_time - now)

        if remaining <= 0:
            timer_label.config(text="Balsošana ir beigusies!")
            break

        days = remaining // 86400
        hours = (remaining % 86400) // 3600
        minutes = (remaining % 3600) // 60
        seconds = remaining % 60

        timer_label.config(text=f"Līdz 1. aprīlim: {days} d. {hours} st. {minutes} min. {seconds} sek.")
        time.sleep(1)

# Funkcija, lai saglabātu balsis JSON formātā
def save_votes_to_json():
    votes = {genre: var.get() for genre, var in user_votes.items()}
    
    # Pārbaudām, vai lietotājs izvēlējās mūziķus visos žanros
    if "" in votes.values():
        messagebox.showwarning("Kļūda", "Izvēlieties mūziķi katrā žanrā!")
        return
    
    # Ielādējam esošos balsu datus vai izveidojam jaunu
    try:
        with open("balsis.json", "r", encoding="utf-8") as file:
            all_votes = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        all_votes = []
    
    # Pievienojam jauno balsi
    all_votes.append(votes)
    
    # Saglabājam atjauninātos datus JSON failā
    with open("balsis.json", "w", encoding="utf-8") as file:
        json.dump(all_votes, file, ensure_ascii=False, indent=4)
    
    messagebox.showinfo("Balsis saglabātas", "Jūsu balsis ir veiksmīgi saglabātas!")
    root.quit()  # Aizveram logu pēc balsošanas

# UI izveide
tk.Label(root, text="Izvēlieties mūziķus katrā žanrā:", font=("Arial", 12)).pack(pady=10)

# Pievienojam žanru blokus
for genre, musicians in genres.items():
    frame = tk.Frame(root)
    frame.pack(anchor="w", padx=10, pady=5)
    
    tk.Label(frame, text=genre, font=("Arial", 10, "bold")).pack(anchor="w")
    
    for musician in musicians:
        tk.Radiobutton(frame, text=musician, variable=user_votes[genre], value=musician).pack(anchor="w")

# Poga balsu saglabāšanai
tk.Button(root, text="Saglabāt balsis", command=save_votes_to_json, font=("Arial", 12)).pack(pady=10)

# Taimeris
timer_label = tk.Label(root, text="", font=("Arial", 12, "bold"), fg="red")
timer_label.pack(pady=10)

# Palaist taimeri atsevišķā pavedienā
threading.Thread(target=update_timer, daemon=True).start()

# Programmas palaišana
root.mainloop()


    

