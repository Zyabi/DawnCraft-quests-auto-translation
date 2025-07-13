from dotenv import load_dotenv
import os
import json
import shutil
import deepl

load_dotenv()

translator = deepl.Translator(os.getenv('DEEPL_API_KEY'))
DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"

# Вихідна та цільова директорії
SOURCE_DIR = os.getenv('SOURCE_DIR')
TARGET_DIR = "quests_translated"

START_FROM_QUEST = "quest_0024"


def translate_text(text, source_lang="EN", target_lang="UK"):
    if not text.strip():
        return text
    result = translator.translate_text(text, source_lang=source_lang, target_lang=target_lang)
    print(f"{text} : {result}")
    return result.text


def process_json_file(src_path, dst_path):
    with open(src_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    def translate_recursive(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == "text" and isinstance(v, str):
                    obj[k] = translate_text(v)
                else:
                    translate_recursive(v)
        elif isinstance(obj, list):
            for item in obj:
                translate_recursive(item)

    translate_recursive(data)

    with open(dst_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def should_process_folder(folder_name, start_from):
    try:
        return folder_name >= start_from
    except:
        return True


def copy_and_translate_directory(src_dir, dst_dir, start_from_quest):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    for root, dirs, files in os.walk(src_dir):
        relative_path = os.path.relpath(root, src_dir)
        parts = relative_path.split(os.sep)

        # Перевірка: якщо в шляху є quest_xxxx, фільтруємо
        quest_folder = next((p for p in parts if p.startswith("quest_")), None)
        if quest_folder and not should_process_folder(quest_folder, start_from_quest):
            continue

        dst_root = os.path.join(dst_dir, relative_path)
        os.makedirs(dst_root, exist_ok=True)

        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(dst_root, file)
            if file.endswith(".json"):
                print(f"Translating: {src_file}")
                process_json_file(src_file, dst_file)
            else:
                shutil.copy2(src_file, dst_file)


if __name__ == "__main__":
    copy_and_translate_directory(SOURCE_DIR, TARGET_DIR, START_FROM_QUEST)
    print("✅ Переклад завершено.")
