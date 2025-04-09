import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import hashlib
from datetime import datetime, timedelta

# Beigu datums
END_DATE = "2025-05-01 00:00:00"

# Žanri un mūziķi
genres = {
    "Roks": ["The Beatles", "Queen", "Linkin Park", "Metallica", "The Rolling Stones"],
    "Pops": ["Kendrick Lamar", "Ed Sheeran", "Tyler, The Creator", "Lady Gaga", "Ariana Grande"],
    "Džezs": ["Louis Armstrong", "Miles Davis", "John Coltrane", "Duke Ellington", "Ella Fitzgerald"],
    "Hip-hops": ["5opka", "Post Malone", "Eminem", "Kanye West", "Jay-Z"],
    "Elektronika": ["Daft Punk", "Skrillex", "Radiohead", "The Prodigy", "Deadmau5"]
}

# Attēli žanriem
genre_images = {
    "Roks": "rock.png",
    "Pops": "pop.png",
    "Džezs": "jazz.png",
    "Hip-hops": "hiphop.png",
    "Elektronika": "electro.png"
}

user_email = ""

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def count_votes():
    vote_counts = {genre: {musician: 0 for musician in musicians} for genre, musicians in genres.items()}
    try:
        with open("balsis.json", "r", encoding="utf-8") as file:
            all_votes = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return vote_counts

    for user_vote in all_votes.values():
        for genre, musician in user_vote.items():
            if genre in vote_counts and musician in vote_counts[genre]:
                vote_counts[genre][musician] += 1
    return vote_counts

def is_voting_closed():
    now = datetime.now()
    end = datetime.strptime(END_DATE, "%Y-%m-%d %H:%M:%S")
    return now >= end

# GUI
root = tk.Tk()
root.title("Balsošana par mūziķiem")
root.geometry("1920x1080")
root.configure(bg="black")
root.withdraw()

# Taimeris
timer_label = tk.Label(root, font=("Arial", 16), fg="lightgreen", bg="black")
timer_label.pack(pady=10)

def update_timer():
    now = datetime.now()
    end = datetime.strptime(END_DATE, "%Y-%m-%d %H:%M:%S")
    remaining = end - now
    if remaining.total_seconds() <= 0:
        timer_label.config(text="Balsošana ir noslēgusies.")
        show_results_window()
        return
    else:
        days = remaining.days
        hours, remainder = divmod(remaining.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        timer_text = f"Laiks līdz balsošanas beigām: {days}d {hours:02d}:{minutes:02d}:{seconds:02d}"
        timer_label.config(text=timer_text)
        root.after(1000, update_timer)

# Pieslēgšanās logs
auth_window = tk.Toplevel()
auth_window.title("Pieslēgšanās")
auth_window.geometry("400x200")
auth_window.attributes("-topmost", True)

tk.Label(auth_window, text="E-pasts:").pack()
email_entry = tk.Entry(auth_window)
email_entry.pack()

tk.Label(auth_window, text="Parole:").pack()
password_entry = tk.Entry(auth_window, show="*")
password_entry.pack()

def authenticate_user():
    global user_email
    email = email_entry.get()
    password = password_entry.get()

    if not email or not password:
        messagebox.showwarning("Kļūda", "E-pasts un parole ir obligāti!")
        return

    hashed_pw = hash_password(password)

    try:
        with open("balsotaji.json", "r", encoding="utf-8") as file:
            registered_users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        registered_users = {}

    if is_voting_closed():
        show_results_window()
        auth_window.destroy()
        return

    if email in registered_users:
        messagebox.showwarning("Kļūda", "Jūs jau esat balsojis!")
        auth_window.destroy()
        return

    registered_users[email] = hashed_pw
    with open("balsotaji.json", "w", encoding="utf-8") as file:
        json.dump(registered_users, file, ensure_ascii=False, indent=4)

    user_email = email
    auth_window.destroy()
    root.deiconify()
    update_timer()

tk.Button(auth_window, text="Pieslēgties", command=authenticate_user).pack()

# Lietotāja izvēles
user_votes = {genre: tk.StringVar() for genre in genres}

def save_votes_to_json():
    votes = {genre: var.get() for genre, var in user_votes.items()}
    if "" in votes.values():
        messagebox.showwarning("Kļūda", "Izvēlieties mūziķi katrā žanrā!")
        return

    try:
        with open("balsis.json", "r", encoding="utf-8") as file:
            all_votes = json.load(file)
            if not isinstance(all_votes, dict):
                all_votes = {}
    except (FileNotFoundError, json.JSONDecodeError):
        all_votes = {}

    all_votes[user_email] = votes

    with open("balsis.json", "w", encoding="utf-8") as file:
        json.dump(all_votes, file, ensure_ascii=False, indent=4)

    messagebox.showinfo("Balsis saglabātas", "Jūsu balsis ir veiksmīgi saglabātas!")
    root.destroy()

# UI uzstādīšana
tk.Label(root, text="Izvēlieties mūziķus katrā žanrā:", font=("Arial", 24), bg="black", fg="white").pack(pady=10)
main_frame = tk.Frame(root, bg="black")
main_frame.pack(pady=10)

vote_counts = count_votes()
genre_photos = {}

for genre, musicians in genres.items():
    frame = tk.Frame(main_frame, bg="black")
    frame.pack(side="left", padx=20)

    if genre in genre_images:
        try:
            img = Image.open(genre_images[genre])
            img = img.resize((200, 150), Image.LANCZOS)
            genre_photos[genre] = ImageTk.PhotoImage(img)
            tk.Label(frame, image=genre_photos[genre], bg="black").pack()
        except FileNotFoundError:
            tk.Label(frame, text="[Nav attēla]", bg="black", fg="red").pack()

    tk.Label(frame, text=genre, font=("Arial", 20, "bold"), bg="black", fg="white").pack()

    for musician in musicians:
        count = vote_counts.get(genre, {}).get(musician, 0)
        label_text = f"{musician} ({count})" if is_voting_closed() else musician
        tk.Radiobutton(frame, text=label_text, variable=user_votes[genre], value=musician,
                       font=("Arial", 18), bg="black", fg="white", selectcolor="gray").pack(anchor="w")

tk.Button(root, text="Saglabāt balsis", command=save_votes_to_json,
          font=("Arial", 24), bg="gray", fg="black").pack(pady=20)

# Rezultātu logs
def show_results_window():
    results = count_votes()
    win = tk.Toplevel()
    win.title("Balsošanas rezultāti")
    win.geometry("1400x400")
    win.configure(bg="black")

    tk.Label(win, text="Balsošanas rezultāti", font=("Arial", 30), fg="white", bg="black").pack(pady=20)

    result_frame = tk.Frame(win, bg="black")
    result_frame.pack()

    for genre, musicians in results.items():
        genre_frame = tk.Frame(result_frame, bg="black", bd=2, relief="groove")
        genre_frame.pack(side="left", padx=20, pady=10)

        tk.Label(genre_frame, text=genre, font=("Arial", 20, "bold"), fg="cyan", bg="black").pack(pady=10)

        for musician, count in sorted(musicians.items(), key=lambda x: -x[1]):
            tk.Label(genre_frame, text=f"{musician}: {count}", font=("Arial", 14), fg="white", bg="black").pack(anchor="w", padx=10)

root.mainloop()
