# NetworkBlocker

Простой инструмент для блокировки сетевого трафика процессов в Windows через правила Windows Firewall.

## 🚀 Быстрый старт (Windows)

### 1) Создать виртуальное окружение (рекомендуется)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2) Установить зависимости
```powershell
python -m pip install -U pip
python -m pip install -r requirements.txt  # если есть
python -m pip install -e .
```

> 🔎 В проекте используется `pyproject.toml` с зависимостями `psutil` и `PySide6`.

### 3) Запуск приложения

#### Вариант A — стандартный (python)
```powershell
python app.py
```

#### Вариант B — через `uv` (если установлен)
```powershell
uv run .\app.py
```

> ✅ `uv` работает как "удобный" лаунчер для Python-скриптов (может автоматически подхватить виртуальное окружение).

---

## 🧠 Как работает

- Список процессов пользователя собирается через `psutil`.
- Для каждого процесса проверяется наличие правила `Block_<имя_процесса>` в Windows Firewall.
- Кнопка **Toggle** создает/удаляет правило, блокируя или разрешая исходящий трафик для выбранного процесса.

---

## 🛠 Технические детали

- GUI: PySide6 (Qt)
- Логика работы с firewall: `netsh advfirewall firewall`

---

## ⚠️ Требование

Запуск должен быть от имени администратора (иначе команды `netsh` не выполняются).
