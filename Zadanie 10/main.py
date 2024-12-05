
import tkinter as tk
import random

def full_name_from_letter(letter):
    result = None
    if letter == 'K': result = 'Kamien'
    if letter == 'P': result = 'Papier'
    if letter == 'N': result = 'Nozyce'
    return result 

root = tk.Tk()
root.title("Papier, Kamien, Nozyce")
label_frame = tk.Frame(root)
label_frame.pack(pady=10)

title_label = tk.Label(label_frame, text="Wybierz: Papier, Kamien lub Nozyce", font=("Arial", 14))
title_label.grid(row=0, column=0, padx=5)

player_label = tk.Label(label_frame, text="Twój wybór: ", font=("Arial", 12))
player_label.grid(row=1, column=0, padx=5)

enemy_label = tk.Label(label_frame, text="Wybór komputera: ", font=("Arial", 12))
enemy_label.grid(row=2, column=0, padx=5)

result_label = tk.Label(label_frame, text="Wynik: ", font=("Arial", 12))
result_label.grid(row=3, column=0, padx=5)

def update_labels(player):
    enemy = random.choice(['P', 'K', 'N'])

    result = None
    if player == 'K':
        if enemy == 'K': result = 'Remis'
        if enemy == 'P': result = 'Przegrana'
        if enemy == 'N': result = 'Wygrana'
    elif player == 'P':
        if enemy == 'K': result = 'Wygrana'
        if enemy == 'P': result = 'Remis'
        if enemy == 'N': result = 'Przegrana'
    elif player == 'N':
        if enemy == 'K': result = 'Pregrana'
        if enemy == 'P': result = 'Wygrana'
        if enemy == 'N': result = 'Remis'

    player_label.config(text=f"Wybrales: {full_name_from_letter(player)}")
    enemy_label.config(text=f"Komputera wybral: {full_name_from_letter(enemy)}")
    result_label.config(text=f"Wynik: {result}")

def play_paper():
    update_labels('P')

def play_rock():
    update_labels('K')

def play_scissors():
    update_labels('N')

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

papier_button = tk.Button(button_frame, text="Papier", font=("Arial", 12), command=play_paper)
papier_button.grid(row=0, column=0, padx=5)

kamien_button = tk.Button(button_frame, text="Kamien", font=("Arial", 12), command=play_rock)
kamien_button.grid(row=0, column=1, padx=5)

nozyce_button = tk.Button(button_frame, text="Nozyce", font=("Arial", 12), command=play_scissors)
nozyce_button.grid(row=0, column=2, padx=5)

root.mainloop()
