# (1) Importi un dati
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import hashlib
from datetime import datetime

END_DATE = "2025-05-01 00:00:00"

genres = {
    "Roks": ["The Beatles", "Queen", "Linkin Park", "Metallica", "The Rolling Stones"],
    "Pops": ["Kendrick Lamar", "Ed Sheeran", "Tyler, The Creator", "Lady Gaga", "Ariana Grande"],
    "Džezs": ["Louis Armstrong", "Miles Davis", "John Coltrane", "Duke Ellington", "Ella Fitzgerald"],
    "Hip-hops": ["5opka", "Post Malone", "Eminem", "Kanye West", "Jay-Z"],
    "Elektronika": ["Daft Punk", "Skrillex", "Radiohead", "The Prodigy", "Deadmau5"]
}

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
    vote_counts = {genre: {m: 0 for m in musicians} for genre, musicians in genres.items()}
    try:
        with open("balsis.json", "r", encoding="utf-8") as f:
            all_votes = json.load(f)
    except:
        return vote_counts
    for vote in all_votes.values():
        for genre, musician in vote.items():
            if genre in vote_counts and musician in vote_counts[genre]:
                vote_counts[genre][musician] += 1
    return vote_counts

def is_voting_closed():
    now = datetime.now()
    end = datetime.strptime(END_DATE, "%Y-%m-%d %H:%M:%S")
    return now >= end

# (2) GUI inicializācija
root = tk.Tk()
root.title("Balsošana par mūziķiem")
root.geometry("1920x1080")
root.configure(bg="black")
root.withdraw()

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
    days = remaining.days
    hours, rem = divmod(remaining.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    timer_label.config(text=f"Laiks līdz beigām: {days}d {hours:02d}:{minutes:02d}:{seconds:02d}")
    root.after(1000, update_timer)

# (3) Pieslēgšanās logs
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
        messagebox.showwarning("Kļūda", "Ievadi e-pastu un paroli!")
        return

    hashed_pw = hash_password(password)
    try:
        with open("balsotaji.json", "r", encoding="utf-8") as f:
            users = json.load(f)
    except:
        users = {}

    if is_voting_closed():
        show_results_window()
        auth_window.destroy()
        return

    if email in users:
        messagebox.showwarning("Kļūda", "Jūs jau esat balsojis!")
        auth_window.destroy()
        return

    users[email] = hashed_pw
    with open("balsotaji.json", "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)

    user_email = email
    auth_window.destroy()
    root.deiconify()
    update_timer()

tk.Button(auth_window, text="Pieslēgties", command=authenticate_user).pack()

# (4) Balsošanas logs
user_votes = {genre: tk.StringVar() for genre in genres}
vote_counts = count_votes()
genre_photos = {}

tk.Label(root, text="Izvēlieties mūziķus katrā žanrā:", font=("Arial", 24), bg="black", fg="white").pack(pady=10)

selected_genre_filter = tk.StringVar(value="Visi")
genre_options = ["Visi"] + list(genres.keys())

genre_filter_menu = tk.OptionMenu(root, selected_genre_filter, *genre_options)
genre_filter_menu.config(font=("Arial", 14))
genre_filter_menu.pack(pady=10)

main_frame = tk.Frame(root, bg="black")
main_frame.pack(pady=10)

def update_genre_display(*args):
    for widget in main_frame.winfo_children():
        widget.destroy()
    for genre, musicians in genres.items():
        if selected_genre_filter.get() != "Visi" and genre != selected_genre_filter.get():
            continue
        frame = tk.Frame(main_frame, bg="black")
        frame.pack(side="left", padx=20)

        if genre in genre_images:
            try:
                img = Image.open(genre_images[genre]).resize((200, 150))
                genre_photos[genre] = ImageTk.PhotoImage(img)
                tk.Label(frame, image=genre_photos[genre], bg="black").pack()
            except:
                tk.Label(frame, text="[Nav attēla]", fg="red", bg="black").pack()

        tk.Label(frame, text=genre, font=("Arial", 20, "bold"), fg="white", bg="black").pack()
        for musician in musicians:
            count = vote_counts[genre][musician]
            label = f"{musician} ({count})" if is_voting_closed() else musician
            tk.Radiobutton(frame, text=label, variable=user_votes[genre], value=musician,
                           font=("Arial", 16), bg="black", fg="white", selectcolor="gray").pack(anchor="w")

selected_genre_filter.trace_add("write", update_genre_display)
update_genre_display()

tk.Button(root, text="Saglabāt balsis", font=("Arial", 20), bg="gray", fg="black",
          command=lambda: save_votes_to_json()).pack(pady=20)

def save_votes_to_json():
    votes = {g: v.get() for g, v in user_votes.items()}
    if "" in votes.values():
        messagebox.showwarning("Kļūda", "Izvēlieties visus žanrus!")
        return
    try:
        with open("balsis.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        data = {}
    data[user_email] = votes
    with open("balsis.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    messagebox.showinfo("Paldies!", "Jūsu balsis ir saglabātas!")
    root.destroy()

# (5) Rezultātu logs ar meklēšanas filtru
def show_results_window():
    def update_filter(*args):
        kw = filter_var.get().lower()
        for widget in result_frame.winfo_children():
            widget.destroy()
        for genre, musicians in results.items():
            if kw and not any(kw in m.lower() for m in musicians):
                continue
            g_frame = tk.Frame(result_frame, bg="black", bd=2, relief="groove")
            g_frame.pack(side="left", padx=20, pady=10)
            tk.Label(g_frame, text=genre, font=("Arial", 20, "bold"), fg="cyan", bg="black").pack(pady=10)
            for musician, count in sorted(musicians.items(), key=lambda x: -x[1]):
                if kw in musician.lower():
                    tk.Label(g_frame, text=f"{musician}: {count}", font=("Arial", 14), fg="white", bg="black").pack(anchor="w", padx=10)

    results = count_votes()
    win = tk.Toplevel()
    win.title("Rezultāti")
    win.geometry("1400x600")
    win.configure(bg="black")

    tk.Label(win, text="Balsošanas rezultāti", font=("Arial", 30), bg="black", fg="white").pack(pady=20)
    tk.Label(win, text="Filtrešana pec muziķa nosaukuma", font=("Arial", 22), bg="black", fg="white").pack(pady=20)
    filter_var = tk.StringVar()
    filter_var.trace_add("write", update_filter)
    tk.Entry(win, textvariable=filter_var, font=("Arial", 14)).pack(pady=10)
    result_frame = tk.Frame(win, bg="black")
    result_frame.pack()
    update_filter()

root.mainloop()