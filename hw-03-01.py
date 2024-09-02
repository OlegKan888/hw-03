import os
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor


# Структура директорій та файлів
structure = {
    "picture": {
        "icons": ["e-learning_icon.jpg", "mongodb.jpg"],
        "Logo": ["IBM+Logo.png", "ibm.svg", "logo-tm.png"],
        "Other": {
            "Icons": ["1600.png"],
            "": ["golang.png", "hqdefault.jpg", "nodejslogo.png"],
        },
        "wallpaper": ["js.png", "node-wallpaper.jpg"],
        "": ["bot-icon.png", "javascript_encapsulation.jpg"],
    }
}


def create_files(base_path, structure):
    for folder, content in structure.items():
        folder_path = base_path / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        if isinstance(content, dict):
            create_files(folder_path, content)
        elif isinstance(content, list):
            for file_name in content:
                file_path = folder_path / file_name
                file_path.touch()  # Створює порожній файл


if __name__ == "__main__":
    base_directory = Path("picture")  # Коренева директорія
    create_files(base_directory, structure)
    print("Структура директорій та файлів створена.")

# Функція для копіювання файлів у відповідні директорії за розширеннями
def copy_file(file_path, target_dir):
    extension = file_path.suffix[1:]  # Отримуємо розширення файлу без крапки
    target_folder = Path(target_dir) / extension
    target_folder.mkdir(
        parents=True, exist_ok=True
    )  # Створюємо директорію, якщо її ще не існує
    shutil.copy(file_path, target_folder / file_path.name)  # Копіюємо файл


# Функція для рекурсивного обходу директорій
def process_directory(source_dir, target_dir):
    with ThreadPoolExecutor() as executor:
        for root, dirs, files in os.walk(source_dir):
            for file_name in files:
                file_path = Path(root) / file_name
                # Викликаємо функцію copy_file у окремому потоці
                executor.submit(copy_file, file_path, target_dir)


# Основна функція
def main(source_dir, target_dir="dist"):
    source_path = Path(source_dir)
    target_path = Path(target_dir)

    if not source_path.exists() or not source_path.is_dir():
        print(f"Директорія {source_dir} не існує або не є директорією.")
        return

    target_path.mkdir(
        parents=True, exist_ok=True
    )  # Створюємо цільову директорію, якщо її ще не існує
    process_directory(source_path, target_path)
    print("Файли успішно скопійовані та відсортовані за розширеннями.")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Використання: python script.py <source_directory> [target_directory]")
    else:
        source_directory = sys.argv[1]
        target_directory = sys.argv[2] if len(sys.argv) > 2 else "dist"
        main(source_directory, target_directory)
