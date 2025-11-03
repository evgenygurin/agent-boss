# 🤖 Ultimate Boss Agent with Task-Centric Memory

> Интеллектуальный босс-агент на базе Autogen с полной памятью, который делегирует ВСЕ задачи через Codegen API

## 🌟 Особенности

### 💾 Тройная система памяти
- **Task-Centric Memory** - специализированная память для задач и решений от Autogen
- **Mem0** - долгосрочная персистентная память
- **ChromaDB** - векторный поиск для похожих задач

### 🎓 Обучение через практику
- **Apprentice Mode** - учится через повторение задач
- **Teachability** - обучение от пользователя
- **Demonstrations** - обучение через примеры успешных решений

### 🚀 100% Делегирование
- Босс НИКОГДА не пишет код сам
- ВСЕ задачи делегируются через Codegen API
- Память оптимизирует каждое делегирование

### 👥 Командная работа
- Общая память для всех агентов команды
- Синхронизация знаний между агентами
- Коллективное обучение

### 📈 Автоматическое улучшение
- Учится на каждой ошибке
- Запоминает успешные паттерны
- Не повторяет прошлые ошибки

## 🏗️ Архитектура

```
┌─────────────────────────────────────────────────────────────┐
│                    Ultimate Boss Agent                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           Task-Centric Memory Controller            │   │
│  │  • Proven solutions                                 │   │
│  │  • Failure patterns                                 │   │
│  │  • Best practices                                   │   │
│  └─────────────────────────────────────────────────────┘   │
│                          ↕                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │    Mem0      │  │  ChromaDB    │  │ Teachability │    │
│  │ Long-term    │  │  Vector      │  │   User       │    │
│  │   Memory     │  │   Search     │  │  Teaching    │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
└─────────────────────────────────────────────────────────────┘
                          ↓
                   Codegen API
                          ↓
              ┌───────────────────────┐
              │  Codegen Agents       │
              │  • Code writing       │
              │  • PR creation        │
              │  • Testing            │
              │  • Deployment         │
              └───────────────────────┘
```

## 🚀 Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/evgenygurin/agent-boss.git
cd agent-boss
```

### 2. Настройка окружения

```bash
# Создайте .env файл
cp .env.example .env

# Заполните необходимые ключи:
# - CODEGEN_ORG_ID
# - CODEGEN_API_TOKEN
# - OPENAI_API_KEY
```

### 3. Запуск с Docker Compose

```bash
docker-compose up -d
```

### 4. Инициализация базы знаний

```bash
python init_boss_knowledge.py
```

## 📚 API Endpoints

### POST /process
Обработка задачи с автоматическим выбором стратегии

```bash
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Fix bug in authentication module",
    "mode": "auto"
  }'
```

Режимы (`mode`):
- `auto` - автоматический выбор стратегии
- `boss` - простое делегирование через босса
- `team` - сложная задача через команду агентов
- `learn` - обучение через практику с retry

### POST /teach
Обучение босса новому знанию

```bash
curl -X POST http://localhost:8000/teach \
  -H "Content-Type: application/json" \
  -d '{
    "lesson": "Always run security scans before deployment"
  }'
```

### POST /demonstrate
Демонстрация успешного решения

```bash
curl -X POST http://localhost:8000/demonstrate \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Deploy to production",
    "solution": "1. Check staging\\n2. Run smoke tests\\n3. Deploy\\n4. Monitor"
  }'
```

### GET /memory/search
Поиск в памяти босса

```bash
curl "http://localhost:8000/memory/search?query=authentication"
```

### GET /memory/stats
Статистика памяти

```bash
curl http://localhost:8000/memory/stats
```

## 💡 Примеры использования

### Простая задача
```python
import httpx

async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://localhost:8000/process",
        json={
            "task": "Add input validation to login form",
            "mode": "boss"
        }
    )
    print(response.json())
```

### Сложная задача с командой
```python
async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://localhost:8000/process",
        json={
            "task": "Implement complex payment system with Stripe integration",
            "mode": "team"
        }
    )
    print(response.json())
```

### Обучение с retry
```python
async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://localhost:8000/process",
        json={
            "task": "Optimize database queries for performance",
            "mode": "learn"
        }
    )
    print(response.json())
```

## 🔧 Конфигурация

### Memory Configuration

Настройка в `ultimate_boss_with_memory.py`:

```python
# Task-Centric Memory
memory_controller = MemoryController(
    reset=False,  # Не сбрасывать память при перезапуске
    client=model_client._impl,
    logger=PageLogger(config={"level": "DEBUG", "path": "./pagelogs/boss"})
)

# Mem0 Long-term Memory
mem0_memory = Mem0Memory(
    is_cloud=False,  # Локальное хранилище
    config={"path": "./boss_mem0_storage"},
    user_id="boss",
    limit=10  # Количество релевантных воспоминаний
)

# ChromaDB Vector Memory
vector_memory = ChromaDBVectorMemory(
    config=ChromaDBVectorMemoryConfig(
        collection_name="boss_memories",
        persist_directory="./boss_chroma_db",
        embedding_function=SentenceTransformerEmbeddingFunctionConfig(
            model_name="all-MiniLM-L6-v2"
        )
    )
)
```

## 📊 Мониторинг

### Логи Task-Centric Memory
```bash
# Просмотр логов обучения
cat pagelogs/boss/memory_log.json
```

### Статистика делегирований
```bash
curl http://localhost:8000/memory/stats
```

### Docker logs
```bash
docker-compose logs -f ultimate-boss-memory
```

## 🧪 Тестирование

```bash
# Unit тесты
pytest tests/

# Интеграционные тесты
pytest tests/integration/

# Тесты памяти
pytest tests/memory/
```

## 🌐 Интеграции

### Codegen API
- Полная интеграция для делегирования
- Мониторинг статуса агентов
- Детальные логи выполнения

### Linear (опционально)
- Создание issue для задач
- Обновление статусов
- Комментарии с прогрессом

### Slack (опционально)
- Уведомления о завершении
- Интерактивные апдейты
- Отчеты о памяти

## 📈 Roadmap

- [x] Task-Centric Memory интеграция
- [x] Apprentice Mode для обучения
- [x] Командная работа с общей памятью
- [ ] Web UI для визуализации памяти
- [ ] GraphQL API
- [ ] Экспорт/импорт базы знаний
- [ ] Multi-tenant support
- [ ] Distributed memory system

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Autogen](https://github.com/microsoft/autogen) - для Task-Centric Memory
- [Codegen](https://codegen.com) - за потрясающий API
- [Mem0](https://mem0.ai) - за долгосрочную память
- [ChromaDB](https://www.trychroma.com/) - за векторный поиск

## 📞 Support

- GitHub Issues: [Report a bug](https://github.com/evgenygurin/agent-boss/issues)
- Email: support@example.com
- Telegram: @agent_boss_support

---

Made with ❤️ by [Evgeny Gurin](https://github.com/evgenygurin)

