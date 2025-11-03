# 🚀 Quick Start Guide

Быстрый старт для Ultimate Boss Agent с Task-Centric Memory.

## Предварительные требования

- Python 3.11+
- Docker и Docker Compose (опционально)
- OpenAI API ключ
- Codegen API токен и org ID

## Установка за 5 минут

### Шаг 1: Клонирование репозитория

```bash
git clone <repository-url>
cd agent-boss
git checkout dev
```

### Шаг 2: Установка зависимостей

```bash
# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate

# Установка зависимостей
pip install -r requirements.txt
```

### Шаг 3: Настройка переменных окружения

```bash
# Копирование примера
cp .env.example .env

# Редактирование .env
nano .env  # или используйте ваш любимый редактор
```

Заполните следующие переменные:

```env
CODEGEN_ORG_ID=your_org_id
CODEGEN_API_TOKEN=your_token
OPENAI_API_KEY=your_openai_key
```

### Шаг 4: Инициализация базы знаний

```bash
python init_boss_knowledge.py
```

Вы увидите:
```
🧠 Initializing Boss Knowledge Base...

📚 Teaching lessons...
  ✓ Lesson 1/10: Always check CI/CD status...
  ...

🎯 Demonstrating solutions...
  ✓ Demo 1/5: Fix failing tests
  ...

✅ Boss knowledge base initialized successfully!
```

### Шаг 5: Запуск приложения

**Вариант A: Локально**

```bash
python ultimate_boss_with_memory.py
```

**Вариант B: С Docker**

```bash
docker-compose up -d
```

**Вариант C: Режим разработки (с auto-reload)**

```bash
uvicorn ultimate_boss_with_memory:app --reload --host 0.0.0.0 --port 8000
```

**Вариант D: Через Makefile**

```bash
make run        # Локально
make docker-up  # Docker
make dev        # Dev mode
```

## Первый запрос

### Через curl

```bash
# Простое делегирование
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Create a hello world Python script",
    "mode": "boss"
  }'
```

### Через Python

```python
import httpx
import asyncio

async def main():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/process",
            json={
                "task": "Create a hello world Python script",
                "mode": "boss"
            }
        )
        print(response.json())

asyncio.run(main())
```

### Результат

```json
{
  "agent_id": "12345",
  "status": "delegated",
  "used_memory": false,
  "web_url": "https://codegen.com/agent/run/12345"
}
```

## Проверка работы

### 1. Статус памяти

```bash
curl http://localhost:8000/memory/stats
```

### 2. Поиск в памяти

```bash
curl "http://localhost:8000/memory/search?query=python"
```

### 3. Запуск тестов

```bash
python test_boss.py
```

Или через Makefile:

```bash
make test
```

## Основные команды

### Делегирование задач

```bash
# Простая задача
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{"task": "Fix bug", "mode": "boss"}'

# Сложная задача (через команду)
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{"task": "Complex: refactor auth system", "mode": "team"}'

# С обучением
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{"task": "Implement feature X", "mode": "learn"}'
```

### Обучение босса

```bash
# Обучить новому знанию
curl -X POST http://localhost:8000/teach \
  -H "Content-Type: application/json" \
  -d '{"lesson": "Always use type hints in Python"}'

# Продемонстрировать решение
curl -X POST http://localhost:8000/demonstrate \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Write tests",
    "solution": "1. Create test file\n2. Write tests\n3. Run pytest"
  }'
```

## Режимы работы

### 1. `boss` - Простое делегирование

Босс делегирует задачу напрямую через Codegen.

**Когда использовать:**
- Простые, понятные задачи
- Быстрые операции
- Когда контекст ясен

**Пример:**
```json
{"task": "Add logging to function X", "mode": "boss"}
```

### 2. `team` - Командная работа

Задача анализируется, планируется и разбивается на подзадачи.

**Когда использовать:**
- Сложные задачи
- Множественные компоненты
- Требуется планирование

**Пример:**
```json
{"task": "Complex: migrate database schema", "mode": "team"}
```

### 3. `learn` - С обучением

Босс пробует, учится на ошибках, повторяет при неудаче.

**Когда использовать:**
- Новые типы задач
- Экспериментальные подходы
- Важно зафиксировать learning

**Пример:**
```json
{"task": "Optimize performance of module Y", "mode": "learn"}
```

### 4. `auto` - Автоматический выбор (по умолчанию)

Босс сам решает, какую стратегию использовать.

**Логика выбора:**
- Если в запросе есть "complex" или "multi" → `team`
- Иначе → `boss`

## Мониторинг

### Логи приложения

```bash
# Docker
docker-compose logs -f ultimate-boss-memory

# Локально
tail -f logs/app.log
```

### Логи памяти

```bash
# Task-Centric Memory
ls -la pagelogs/

# Mem0
ls -la boss_mem0_storage/

# ChromaDB
ls -la boss_chroma_db/
```

### API документация

Откройте в браузере:
```
http://localhost:8000/docs
```

FastAPI автоматически генерирует Swagger UI.

## Типичные проблемы

### Проблема: Server not responding

**Решение:**
```bash
# Проверить статус
curl http://localhost:8000/memory/stats

# Перезапустить
docker-compose restart  # Docker
# или
pkill -f ultimate_boss_with_memory.py && python ultimate_boss_with_memory.py
```

### Проблема: Memory not working

**Решение:**
```bash
# Сброс памяти
make reset-memory

# Реинициализация
python init_boss_knowledge.py
```

### Проблема: Codegen API errors

**Проверить:**
1. Правильность `CODEGEN_ORG_ID`
2. Актуальность `CODEGEN_API_TOKEN`
3. Доступность API: `https://api.codegen.com/v1/health`

### Проблема: OpenAI API errors

**Проверить:**
1. Правильность `OPENAI_API_KEY`
2. Наличие кредитов на аккаунте
3. Rate limits

## Полезные команды Makefile

```bash
make help           # Показать все команды
make install        # Установить зависимости
make init           # Инициализировать знания
make run            # Запустить локально
make dev            # Dev режим с auto-reload
make test           # Запустить тесты
make docker-up      # Запустить в Docker
make docker-down    # Остановить Docker
make docker-logs    # Показать логи Docker
make clean          # Очистить кэши
make reset-memory   # Сбросить память
```

## Следующие шаги

1. **Изучите архитектуру**: прочитайте `ARCHITECTURE.md`
2. **Настройте интеграции**: добавьте Linear, Slack и т.д.
3. **Обучите босса**: используйте `/teach` и `/demonstrate`
4. **Мониторинг**: настройте логирование и метрики
5. **Кастомизация**: адаптируйте под ваши процессы

## Получение помощи

- **Документация**: `README.md`, `ARCHITECTURE.md`
- **Примеры**: `test_boss.py`
- **API docs**: http://localhost:8000/docs

## Быстрая проверка

Запустите полную проверку системы:

```bash
# 1. Инициализация
python init_boss_knowledge.py

# 2. Запуск
python ultimate_boss_with_memory.py &

# 3. Подождать 5 секунд
sleep 5

# 4. Тесты
python test_boss.py

# 5. Если все ОК, вы увидите:
# ✅ All tests completed successfully!
```

---

**Готово!** 🎉 Теперь ваш Ultimate Boss готов делегировать задачи через Codegen с полной памятью!
