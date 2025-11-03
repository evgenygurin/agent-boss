# 🧠 Ultimate Boss Agent with Task-Centric Memory

Интеллектуальный босс-агент с полной памятью, который делегирует ВСЕ задачи через Codegen API и учится на каждом опыте.

## 🎯 Ключевые возможности

### Тройная система памяти
- **Task-Centric Memory** - специализированная память для задач и решений от Autogen
- **Mem0** - долгосрочная персистентная память
- **ChromaDB** - векторный поиск для похожих задач

### Обучение через практику
- Учится на каждом делегировании
- Запоминает успешные паттерны
- Избегает повторения ошибок
- Обучается от пользователя

### 100% делегирование
- Босс НИКОГДА не пишет код сам
- ВСЕ задачи делегируются через Codegen API
- Память оптимизирует каждое делегирование

### Командная работа
- Общая память для всех агентов
- Аналитик для анализа задач
- Координатор для планирования
- Босс для делегирования

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка окружения

```bash
cp .env.example .env
# Отредактируйте .env и добавьте ваши ключи
```

### 3. Инициализация базы знаний

```bash
python init_boss_knowledge.py
```

### 4. Запуск через Docker Compose

```bash
docker-compose up -d
```

### 5. Запуск локально

```bash
python ultimate_boss_with_memory.py
```

API будет доступен на `http://localhost:8000`

## 📡 API Endpoints

### POST /process
Обрабатывает задачу с использованием памяти

```json
{
  "task": "Fix bug in authentication module",
  "mode": "auto"  // auto, boss, team, learn
}
```

**Режимы:**
- `auto` - автоматический выбор стратегии
- `boss` - простое делегирование через босса
- `team` - сложная задача через команду
- `learn` - обучение с возможностью повторных попыток

### POST /teach
Обучает босса новому знанию

```json
{
  "lesson": "Always run security audit before deployment"
}
```

### POST /demonstrate
Демонстрирует правильное решение

```json
{
  "task": "Deploy to production",
  "solution": "1. Check tests\n2. Deploy\n3. Monitor"
}
```

### GET /memory/search?query=deployment
Ищет в памяти босса

### GET /memory/stats
Показывает статистику памяти

## 🧪 Примеры использования

### Простое делегирование

```python
import asyncio
import httpx

async def delegate_task():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/process",
            json={
                "task": "Add unit tests for user authentication",
                "mode": "boss"
            }
        )
        print(response.json())

asyncio.run(delegate_task())
```

### Обучение босса

```python
import asyncio
import httpx

async def teach():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/teach",
            json={
                "lesson": "Always use TypeScript strict mode for new projects"
            }
        )
        print(response.json())

asyncio.run(teach())
```

### Сложная задача через команду

```python
import asyncio
import httpx

async def complex_task():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/process",
            json={
                "task": "Refactor authentication system with multi-factor auth",
                "mode": "team"
            }
        )
        print(response.json())

asyncio.run(complex_task())
```

### Поиск в памяти

```python
import asyncio
import httpx

async def search():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8000/memory/search",
            params={"query": "authentication"}
        )
        print(response.json())

asyncio.run(search())
```

## 🏗️ Архитектура

```
┌─────────────────────────────────────────────────┐
│           UltimateMemoryOrchestrator            │
└────────────────┬────────────────────────────────┘
                 │
        ┌────────┴────────┐
        │                 │
        ▼                 ▼
┌───────────────┐  ┌──────────────┐
│ApprenticeBoss │  │MemoryEnabled │
│               │  │    Team      │
└───────┬───────┘  └──────┬───────┘
        │                 │
        ▼                 ▼
┌────────────────────────────────┐
│   UltimateBossWithMemory       │
│   + BossMemorySystem           │
└────────────────────────────────┘
        │
        ├── Task-Centric Memory
        ├── Mem0 Memory
        └── ChromaDB Vector Memory
        │
        ▼
┌────────────────────────────────┐
│    Codegen API Client          │
│    (Delegation Layer)          │
└────────────────────────────────┘
```

## 📊 Система памяти

### Task-Centric Memory
Хранит успешные решения задач:
- Паттерны делегирования
- Проверенные подходы
- Инструкции для типов задач

### Mem0 Memory
Долгосрочная память:
- История всех делегирований
- Уроки от пользователя
- Анализ ошибок

### ChromaDB Vector Memory
Векторный поиск:
- Поиск похожих задач
- Семантическая близость
- Контекстуальные связи

## 🔧 Конфигурация

### Переменные окружения

```env
CODEGEN_ORG_ID=your_org_id
CODEGEN_API_TOKEN=your_token
OPENAI_API_KEY=your_key
```

### Docker Compose

Сервисы:
- `ultimate-boss-memory` - основное приложение
- `chroma` - векторная база данных
- `redis` - кэширование

Volumes для персистентности:
- `pagelogs/` - логи Task-Centric Memory
- `boss_teachability_db/` - база обучаемости
- `boss_mem0_storage/` - Mem0 хранилище
- `boss_chroma_db/` - ChromaDB данные

## 🎓 Обучение босса

Босс учится тремя способами:

### 1. Автоматическое обучение
Автоматически учится на результатах каждого делегирования

### 2. Явное обучение
Через `/teach` endpoint

### 3. Демонстрации
Через `/demonstrate` endpoint с примерами решений

## 🔍 Мониторинг

### Проверка статуса памяти

```bash
curl http://localhost:8000/memory/stats
```

### Просмотр активных делегирований

```python
# В коде босса
print(boss.active_delegations)
```

### Логи

Логи сохраняются в:
- `./logs/` - application logs
- `./pagelogs/` - memory controller logs

## 🛠️ Разработка

### Запуск в режиме разработки

```bash
# С автоперезагрузкой
uvicorn ultimate_boss_with_memory:app --reload --host 0.0.0.0 --port 8000
```

### Тестирование

```bash
# Инициализация знаний
python init_boss_knowledge.py

# Тест простого делегирования
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{"task": "Add README", "mode": "boss"}'

# Тест обучения
curl -X POST http://localhost:8000/teach \
  -H "Content-Type: application/json" \
  -d '{"lesson": "Use conventional commits"}'
```

## 📈 Roadmap

- [ ] Интеграция с Linear для автоматического создания задач
- [ ] Slack уведомления о статусе делегирований
- [ ] Dashboard для визуализации памяти
- [ ] Метрики эффективности делегирований
- [ ] A/B тестирование разных подходов
- [ ] Multi-tenant support

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

## 📝 License

MIT

## 🙏 Credits

Built with:
- [Autogen](https://github.com/microsoft/autogen) - Multi-agent framework
- [Codegen API](https://codegen.com) - Code generation platform
- [Mem0](https://mem0.ai) - Long-term memory
- [ChromaDB](https://www.trychroma.com/) - Vector database
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework

---

Made with ❤️ and 🧠 by Ultimate Boss Team
