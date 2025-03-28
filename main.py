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
            if game.lower() in process.info['name'].lower():  # Примерное совпадение
                return True, process.info['name']  # Возвращаем полное имя процесса
    return False, None

def notify_user(message):
    root = tk.Tk()
    root.withdraw()  # Скрыть главное окно
    messagebox.showwarning("Уведомление", message)
    root.destroy()

def close_game(game_name):
    for process in psutil.process_iter(['name']):
        if game_name.lower() == process.info['name'].lower():  # Точное совпадение
            process.kill()
            print(f"Приложение '{game_name}' закрыто.")
            break

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

    print(f"Игра найдена: '{current_game}'")

    time_to_play = int(input("Введите время игры в секундах: "))  # Время в секундах

    while time_to_play > 0:
        print(f"Осталось времени: {time_to_play} секунд")
        time.sleep(1)  # Убавляем таймер каждую секунду
        time_to_play -= 1

    close_game(current_game)
    print(f"Время игры '{current_game}' закончилось. Приложение закрыто.")

if __name__ == "__main__":
    main()
