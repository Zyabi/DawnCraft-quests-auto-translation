
# 🗂️ Quest Translator for DawnCraft

Цей python3.11 скрипт призначений для автоматичного перекладу квестів модпаку DawnCraft із англійської на українську мову з використанням DeepL API.  
Підтримується збереження структури директорій, фільтрація перекладених елементів та корекція форматуючих тегів (наприклад, `$(red)`).

---

## 🔧 Основні можливості

- 📁 Рекурсивна обробка директорій `quests/quests_0000/quest_XXXX/...`
- 🌍 Переклад лише значень `text` у JSON-файлах
- 🧠 Виправлення кольорових тегів, які могли бути перекладені (наприклад, `$(червоне)` → `$(red)`)
- 🎯 Можливість вказати, з якого квесту почати (`quest_0016` і т.д.)
- 🗃️ Збереження структури в нову директорію `quests_translated`

---

## 📁 Структура проєкту

```
.
├── main.py              # Головний скрипт для перекладу
├── fix_colors.py        # Окремий скрипт для виправлення кольорових тегів
├── .env                 # Файл з налаштуваннями
└── README.md            # Інструкція (цей файл)
```

---

## 📦 Встановлення

1. **Клонувати репозиторій**
2. **Встановити залежності**:
   ```bash
   pip install python-dotenv deepl
   ```

3. **Створити `.env` файл**:
   ```env
   DEEPL_API_KEY=your_deepl_api_key_here
   SOURCE_DIR=quests_folder
   ```

---

## 🚀 Використання

### 1. Переклад
```bash
python main.py
```
> Це перекладе всі квести починаючи з `quest_0016`(можна змінити в мейні) у директорію `quests_translated`.

### 2. Виправлення тегів кольорів
```bash
python fix_colors.py
```
> Після перекладу виконайте цей скрипт, щоб замінити перекладені кольори на англійські теги у форматі `$(...)`.

---

## 🧠 Приклад виправлення

**Було після перекладу:**
```json
"text": "Ви вже отримали $(червону)Серце моря?"
```

**Стане після `fix_colors.py`:**
```json
"text": "Ви вже отримали $(red)Серце моря?"
```

---

## ✅ Підтримувані кольори

Виправляються усі основні кольори:
- червоне → `red`
- синє → `blue`
- зелене → `green`
- жовте → `yellow`
- фіолетове → `purple`
- та інші…

Система працює за **коренем слова**, тому охоплює всі відмінки.

---

## 📜 Ліцензія

Цей проєкт вільний для використання, редагування та поширення. Але не забудьте про обмеження DeepL API — кількість запитів залежить від вашого тарифу.

---

## 📬 Зворотній зв’язок

Якщо маєш ідеї, баги або хочеш розширити функціональність — не соромся відкривати issue або форкати проєкт.
