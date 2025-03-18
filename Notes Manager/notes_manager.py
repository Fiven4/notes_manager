import os
import threading
import time
from datetime import datetime

users = {}
notes = {}
log_file = "actions.log"
current_user = None

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
notes_file = os.path.join(desktop_path, "notes.txt")

def log_action(action_type, message):
    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    username = current_user if current_user else "Гость"
    with open(log_file, "a", encoding="utf-8") as log:
        log.write(f"[{action_type}] [{timestamp}] [{username}] – {message}\n")

def auto_save():
    while True:
        try:
            with open(notes_file, "w", encoding="utf-8") as file:
                for user, user_notes in notes.items():
                    file.write(f"{user}:\n")
                    for note in user_notes:
                        file.write(f"  {note}\n")
            time.sleep(10)
        except Exception as e:
            log_action("ERROR", f"Ошибка автосохранения: {e}")

def register():
    global users, notes
    try:
        print("\n--- Регистрация ---")
        username = input("Придумайте логин: ").strip()
        if len(username) < 3:
            print("Логин должен быть не менее 3 символов.")
            return

        if username in users:
            print("Этот логин уже занят.")
            log_action("WARNING", "Попытка повторной регистрации")
            return

        password = input("Придумайте пароль: ").strip()
        if len(password) < 4:
            print("Пароль должен быть не менее 4 символов.")
            return

        users[username] = password
        notes[username] = []
        print("Регистрация прошла успешно!")
        log_action("INFO", f"Зарегистрирован новый пользователь: {username}")

    except Exception as e:
        log_action("ERROR", f"Ошибка регистрации: {e}")

def login():
    global current_user
    try:
        print("\n--- Авторизация ---")
        username = input("Логин: ").strip()
        password = input("Пароль: ").strip()

        if username in users and users[username] == password:
            current_user = username
            print(f"\nДобро пожаловать, {username}!")
            log_action("INFO", f"Успешный вход: {username}")
            return True
        else:
            print("Неверные учетные данные.")
            log_action("WARNING", f"Неудачная попытка входа: {username}")
            return False

    except Exception as e:
        log_action("ERROR", f"Ошибка авторизации: {e}")
        return False

def add_note():
    global notes
    try:
        print("\n--- Добавление заметки ---")
        note = input("Введите текст заметки: ").strip()
        if note:
            notes[current_user].append(note)
            print("Заметка успешно добавлена.")
            log_action("INFO", f"Добавлена заметка: {note}")
        else:
            print("Заметка не может быть пустой.")
    except Exception as e:
        log_action("ERROR", f"Ошибка добавления заметки: {e}")

def delete_note():
    global notes
    try:
        print("\n--- Удаление заметки ---")
        if not notes[current_user]:
            print("У вас пока нет заметок.")
            return

        for i, note in enumerate(notes[current_user], 1):
            print(f"{i}. {note}")

        choice = input("Выберите номер заметки для удаления: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(notes[current_user]):
            deleted_note = notes[current_user].pop(int(choice) - 1)
            print(f"Заметка '{deleted_note}' успешно удалена.")
            log_action("INFO", f"Удалена заметка: {deleted_note}")
        else:
            print("Некорректный выбор.")
    except Exception as e:
        log_action("ERROR", f"Ошибка удаления заметки: {e}")

def edit_note():
    global notes
    try:
        print("\n--- Редактирование заметки ---")
        if not notes[current_user]:
            print("У вас пока нет заметок.")
            return

        for i, note in enumerate(notes[current_user], 1):
            print(f"{i}. {note}")

        choice = input("Выберите номер заметки для редактирования: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(notes[current_user]):
            new_note = input("Введите новый текст заметки: ").strip()
            if new_note:
                old_note = notes[current_user][int(choice) - 1]
                notes[current_user][int(choice) - 1] = new_note
                print(f"Заметка успешно изменена: '{old_note}' -> '{new_note}'.")
                log_action("INFO", f"Заметка изменена: {old_note} -> {new_note}")
            else:
                print("Заметка не может быть пустой.")
        else:
            print("Некорректный выбор.")
    except Exception as e:
        log_action("ERROR", f"Ошибка редактирования заметки: {e}")

def view_notes():
    print("\n--- Ваши заметки ---")
    if not notes[current_user]:
        print("Заметок пока нет.")
        return

    for i, note in enumerate(notes[current_user], 1):
        print(f"{i}. {note}")

def notes_session():
    global current_user
    while True:
        print(f"\n--- Главное меню ({current_user}) ---")
        print("1. Добавить заметку")
        print("2. Удалить заметку")
        print("3. Редактировать заметку")
        print("4. Просмотреть заметки")
        print("5. Выйти")

        choice = input("Выберите действие (1-5): ").strip()

        if choice == '1':
            add_note()
        elif choice == '2':
            delete_note()
        elif choice == '3':
            edit_note()
        elif choice == '4':
            view_notes()
        elif choice == '5':
            print("Выход из аккаунта...")
            log_action("INFO", f"Пользователь {current_user} вышел из системы")
            current_user = None
            break
        else:
            print("Некорректный выбор.")

def main():
    threading.Thread(target=auto_save, daemon=True).start()

    while True:
        print("\n=== Менеджер заметок ===")
        print("1. Зарегистрироваться")
        print("2. Войти")
        print("3. Выйти из программы")

        choice = input("Выберите действие (1-3): ").strip()

        if choice == '1':
            register()
        elif choice == '2':
            if login():
                notes_session()
        elif choice == '3':
            print("Завершение работы...")
            log_action("INFO", "Программа завершена")
            break
        else:
            print("Некорректный выбор.")

if __name__ == "__main__":
    main()