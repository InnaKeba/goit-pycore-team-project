"""Модуль для управління нотатками. Включає класи для створення, видалення, пошуку та виведення нотаток.
Використовує UserDict для зберігання нотаток та забезпечує зручний інтерфейс для роботи з ними. """
from notes import NotesBook, NoteRecord
import textwrap

def input_error(func): # декоратор для обробки помилок введення
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return f"Помилка: {str(e)}"
    return wrapper

def parse_input(user_input):
    # 1) Видаляємо пробіли спереду/ззаду
    # 2) Розбиваємо на слова
    cmd, *args = user_input.strip().split()
    # 3) Повертаємо команду у нижньому регістрі та решту слів як аргументи
    return cmd.lower(), args

@input_error
def add_note(args, book: NotesBook): # Функція для додавання нотатки
    name = args[0] 
    text = " ".join(args[1:-1]) if len(args) > 2 else args[1] # якщо тег є, то беремо його як останній аргумент
    tag = args[-1] if len(args) > 2 else None # якщо тег не вказано, то None
    record = NoteRecord(name, text, tag) 
    book.add_note(record)
    return f"Нотатку '{name}' додано."


@input_error
def delete_note(args, book: NotesBook): # Функція для видалення нотатки
    name = args[0] 
    if book.delete_note(name):  
        return f"Нотатку '{name}' видалено." 
    return f"Ой-йой, нотатку '{name}' не знайдено 😢"

@input_error
def edit_name(args, book: NotesBook): # Функція для редагування назви нотатки
    if len(args) < 2:
        raise ValueError("Вкажи стару та нову назву нотатки.\nПриклад: edit_name [стара назва] [нова назва]")

    old_name, new_name = args[0], args[1]

    if old_name not in book.data:
        return f"Ой-йой, нотатку з назвою '{old_name}' не знайдено 😢"

    note = book.data.pop(old_name)
    note.name.value = new_name
    book.data[new_name] = note
    return f"Назву нотатки змінено з '{old_name}' на '{new_name}'."

@input_error
def edit_text(args, book: NotesBook): # Функція для редагування тексту нотатки
    if len(args) < 2:
        raise ValueError("Вкажи назву нотатки та новий текст.\nПриклад: edit_text [назва] [новий текст]")

    name = args[0]
    new_text = " ".join(args[1:])

    if name not in book.data:
        return f"Ой-йой, нотатку '{name}' не знайдено 😢"

    book.data[name].text.value = new_text
    return f"Текст нотатки '{name}' успішно оновлено."

@input_error
def show_notes(book: NotesBook): # Функція для виведення всіх нотаток
    notes = book.get_all_notes()
    if not notes:
        return "Книга нотаток порожня."
    return "\n".join(str(note) for note in notes)


@input_error
def search_note(args, book: NotesBook): # Функція для пошуку нотатки за назвою
    keyword = " ".join(args)
    results = book.search_by_name(keyword)
    return "\n".join(str(note) for note in results) if results else "Ой-йой, шось пішло не так 🤷‍♀️. Нотатки не знайдено."


@input_error
def search_note_text(args, book: NotesBook):    # Функція для пошуку нотатки за текстом
    keyword = " ".join(args)
    results = book.search_by_text(keyword)
    return "\n".join(str(note) for note in results) if results else "Ой-йой, шось пішло не так 🤷‍♀️.Нотатки не знайдено за текстом."


@input_error
def search_tag(args, book: NotesBook): # Функція для пошуку нотатки за тегом
    keyword = args[0]
    results = book.search_by_tag(keyword)
    return "\n".join(str(note) for note in results) if results else "Ой-йой, шось пішло не так 🤷‍♀️.Нотатки з таким тегом не знайдено."

def show_help(): # Функція для виведення довідки з доступними командами
    return """
 Доступні команди Notes:

• help                             – показати весь список команд
• add [назва] [текст] [тег]        – додати нову нотатку
• edit_name [стара] [нова назва]   – змінити назву нотатки
• edit_text [назва] [новий текст]  – змінити текст нотатки
• all                              – показати всі нотатки
• delete [назва]                   – видалити нотатку за назвою
• search [частина назви]           – пошук за назвою нотатки
• search_notes [ключове слово]     – пошук за текстом нотатки
• search_tag [тег]                 – пошук за тегом нотатки
• back                             – повернутися до стартового меню
• exit / close                     – завершити роботу
"""
def main():
    book = NotesBook() 
    book.load() # Завантажуємо нотатки з файлу при запуску
    print("👋 Вітаємо в блокноті Notes 🐍 від Snaky sisters!")
    print("💡 Для перегляду всього переліку команд введіть: help")

    while True:
        user_input = input("--> ")
        command, args = parse_input(user_input)

        match command:
            case "add":
                print(add_note(args, book))
                book.save() # Зберігаємо нотатки після додавання
            case "delete":
                print(delete_note(args, book))
                book.save() # Зберігаємо нотатки після видалення
        
            case "edit_name": # Редагування назви нотатки
                print(edit_name(args, book))
                book.save()

            case "edit_text": # Редагування тексту нотатки
                print(edit_text(args, book))
                book.save()

            case "search":
                print(search_note(args, book))
            case "search_notes":
                print(search_note_text(args, book))
            case "search_tag":
                print(search_tag(args, book))
            case "all":
                print(show_notes(book))
            case "back":
                print("I'll be back ↩ Але поки повертаємося в стартове меню.")
                break
            case "exit" | "close":
                print("👋 Дякуємо за використання блокноту Notes! До нових зустрічей! 🐍")
                break
            case "help":
                print(show_help())
            case _:
                print("😳 Команда не розпізнана. Можливо, ти винайшла(-ов) нову функцію? Введи help для списку доступного 😅")
           

if __name__ == "__main__":
    main()
