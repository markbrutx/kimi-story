# 📖 Novel Reader

Лёгкая читалка для веб-новелл на Astro + Bun. Оптимизирована для мобильных устройств.

## 🚀 Старт

```bash
# Установка
bun install

# Dev сервер
bun run dev

# Билд
bun run build
```

## 📁 Структура

```
├── src/
│   ├── components/
│   │   ├── Layout.astro    # Базовый layout
│   │   └── Reader.astro    # Компонент читалки
│   └── pages/
│       └── index.astro     # Главная страница
├── public/chapters/        # JSON главы
├── workbench/              # Вспомогательные файлы
│   ├── split_chapters.py   # Скрипт разбивки
│   └── time_traveler_novel.txt
└── .github/workflows/      # GitHub Actions
```

## 🔄 Добавить новеллу

```bash
cd workbench
# Положить novel.txt
python3 split_chapters.py
cd ..
bun run build
```

## 📤 Деплой

GitHub Actions автоматически деплоит при пуше в `main`.

## ⚡ Фичи

- Swipe навигация
- Progress bar
- Slide-over оглавление
- Keyboard navigation
- Shareable URLs (`?chapter=5`)
