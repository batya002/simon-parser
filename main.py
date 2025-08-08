from simon_parser import run_simon
from zolando_parser import run_zalando

def main():
    print("Выберите парсер:")
    print("1 — Simon")
    print("2 — Zalando")
    choice = input("Введите номер: ")

    if choice == "1":
        run_simon()
    elif choice == "2":
        run_zalando()
    else:
        print("❌ Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
