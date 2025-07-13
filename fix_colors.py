import os
import json
import re

TARGET_DIR = "quests_translated"

COLOR_ROOTS = {
    "черв": "red",
    "син": "blue",
    "зел": "green",
    "жовт": "yellow",
    "фіолет": "purple",
    "бірюз": "aqua",
    "рожев": "pink",
    "біл": "white",  # білий, біла, білого, білої...
    "чор": "black",
    "сір": "gray",
    "помаранч": "orange",
    "оранж": "orange",
    "лайм": "lime",
    "блакит": "light_blue",
    "коричн": "brown"
}


def fix_color_tags(text):
    def replacer(match):
        inner = match.group(1).strip().lower()

        for root, color in COLOR_ROOTS.items():
            if inner.startswith(root):
                return f"$({color})"
        return match.group(0)  # залишити без змін

    return re.sub(r"\$\((.*?)\)", replacer, text)


def process_json_file(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    def fix_recursive(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == "text" and isinstance(v, str):
                    obj[k] = fix_color_tags(v)
                else:
                    fix_recursive(v)
        elif isinstance(obj, list):
            for item in obj:
                fix_recursive(item)

    fix_recursive(data)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                print(f"Fixing: {file_path}")
                process_json_file(file_path)


if __name__ == "__main__":
    process_directory(TARGET_DIR)
    print("✅ Колірні теги виправлено з урахуванням коренів.")
