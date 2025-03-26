import os
import time
import psutil
import tkinter as tk
from tkinter import messagebox

def load_games(filename):
    with open(filename, 'r') as file:
        games = [line.strip() for line in file if line.strip()]
    return games

def check_game_running(games):
    for game in games:
        for process in psutil.process_iter(['name']):
            if game.lower() in process.info['name'].lower():  # Проверяем частичное совпадение
                return True, game
    return False, None

def notify_user(message):
    root = tk.Tk()
    root.withdraw()  # Скрыть главное окно
    messagebox.showwarning("Уведомление", message)
    root.destroy()

def main():
    games_file = 'games.txt'
    games = load_games(games_file)

    game_running = False
    current_game = None

    while not game_running:
        game_running, current_game = check_game_running(games)
        if not game_running:
            print("Игра не найдена. Ожидание...")
            time.sleep(5)  # Ждем 5 секунд перед следующей проверкой

    print(f"Игра '{current_game}' запущена.")
    
    # Ввод времени игры сразу при старте программы
    time_to_play = int(input("Введите время игры в минутах: ")) * 60  # Переводим в секунды
    warning_time = 15 * 60  # 15 минут в секундах

    total_time = time_to_play
    while total_time > 0:
        if total_time <= warning_time:
            notify_user(f"Сеанс игры '{current_game}' закончится через 15 минут.")
            time.sleep(warning_time)
            break
        time.sleep(60)  # Проверяем каждую минуту
        total_time -= 60

    print(f"Время игры '{current_game}' закончилось.")

if __name__ == "__main__":
    main()
