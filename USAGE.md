# 📖 Ultimate Boss Agent - Usage Guide

Полное руководство по использованию Ultimate Boss Agent с Task-Centric Memory.

## 🚀 Быстрый старт

### 1. Настройка окружения

```bash
# Клонируйте репозиторий
git clone https://github.com/evgenygurin/agent-boss.git
cd agent-boss

# Скопируйте .env.example в .env
cp .env.example .env

# Отредактируйте .env и добавьте ваши API ключи:
# CODEGEN_ORG_ID=your_org_id
# CODEGEN_API_TOKEN=your_token
# OPENAI_API_KEY=your_key
```

### 2. Запуск с помощью скрипта

```bash
# Автоматический запуск (рекомендуется)
./run.sh
```

### 3. Ручной запуск

```bash
# Сборка
docker-compose build

# Запуск
docker-compose up -d

# Инициализация базы знаний
python init_boss_knowledge.py

# Проверка
curl http://localhost:8000/health
```

## 💡 Основные возможности

### 1. Делегирование задач

#### Простая задача

```bash
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Add input validation to login form",
    "mode": "boss"
  }'
```

#### Сложная задача (командная работа)

```bash
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Implement payment system with Stripe integration",
    "mode": "team"
  }'
```

#### Задача с обучением

```bash
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Optimize database queries",
    "mode": "learn"
  }'
```

### 2. Обучение босса

#### Добавление урока

```bash
curl -X POST http://localhost:8000/teach \
  -H "Content-Type: application/json" \
  -d '{
    "lesson": "Always run security scans before deployment"
  }'
```

#### Демонстрация решения

```bash
curl -X POST http://localhost:8000/demonstrate \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Deploy to production",
    "solution": "1. Check staging\n2. Run tests\n3. Deploy\n4. Monitor"
  }'
```

### 3. Работа с памятью

#### Поиск в памяти

```bash
curl "http://localhost:8000/memory/search?query=authentication"
```

#### Статистика памяти

```bash
curl http://localhost:8000/memory/stats
```

## 🐍 Python примеры

### Базовое использование

```python
import asyncio
import httpx

async def delegate_task():
    async with httpx.AsyncClient() as client:
        # Делегируем задачу
        response = await client.post(
            "http://localhost:8000/process",
            json={
                "task": "Fix bug in authentication module",
                "mode": "auto"  # Автоматический выбор стратегии
            }
        )
        result = response.json()
        print(f"Agent ID: {result['agent_id']}")
        print(f"Used memory: {result['used_memory']}")
        print(f"Web URL: {result.get('web_url')}")

asyncio.run(delegate_task())
```

### Обучение и демонстрация

```python
import asyncio
import httpx

async def teach_boss():
    async with httpx.AsyncClient() as client:
        # Обучаем новому правилу
        await client.post(
            "http://localhost:8000/teach",
            json={"lesson": "Use meaningful variable names"}
        )
        
        # Демонстрируем решение
        await client.post(
            "http://localhost:8000/demonstrate",
            json={
                "task": "Code review",
                "solution": "1. Check logic\n2. Review security\n3. Verify tests"
            }
        )
        
        print("Boss taught successfully!")

asyncio.run(teach_boss())
```

### Мониторинг памяти

```python
import asyncio
import httpx

async def monitor_memory():
    async with httpx.AsyncClient() as client:
        # Получаем статистику
        stats = await client.get("http://localhost:8000/memory/stats")
        data = stats.json()
        
        print(f"Total memories: {data['total_memories']}")
        print(f"Total solutions: {data['total_solutions']}")
        print(f"Active delegations: {data['active_delegations']}")
        
        # Ищем в памяти
        search = await client.get(
            "http://localhost:8000/memory/search",
            params={"query": "deployment"}
        )
        results = search.json()
        
        print(f"\nFound {len(results['results'])} memories about deployment")
        for memory in results['results'][:3]:
            print(f"  - {memory['content'][:100]}...")

asyncio.run(monitor_memory())
```

## 🎯 Режимы работы

### `mode="auto"` (по умолчанию)
Автоматически выбирает стратегию на основе сложности задачи:
- Простые задачи → boss
- Сложные задачи → team

```python
response = await client.post(
    "http://localhost:8000/process",
    json={"task": "Your task", "mode": "auto"}
)
```

### `mode="boss"`
Простое делегирование через босс-агента:
- Быстрое выполнение
- Использует память для оптимизации
- Подходит для большинства задач

```python
response = await client.post(
    "http://localhost:8000/process",
    json={"task": "Your task", "mode": "boss"}
)
```

### `mode="team"`
Командная работа для сложных задач:
- Анализ задачи аналитиком
- Планирование координатором
- Делегирование боссом
- Подходит для multi-step задач

```python
response = await client.post(
    "http://localhost:8000/process",
    json={"task": "Your complex task", "mode": "team"}
)
```

### `mode="learn"`
Обучение через практику с retry:
- Делегирует задачу
- Мониторит выполнение
- Учится на ошибках
- Повторяет при неудаче

```python
response = await client.post(
    "http://localhost:8000/process",
    json={"task": "Your task", "mode": "learn"}
)
```

## 🧠 Система памяти

### Типы памяти

1. **Simple Memory** (всегда доступна)
   - Базовый fallback
   - Работает без дополнительных зависимостей
   - Простой поиск по ключевым словам

2. **Task-Centric Memory** (опционально)
   - Специализированная для задач
   - Доказанные решения
   - Паттерны успеха

3. **Mem0** (опционально)
   - Долгосрочная память
   - Персистентное хранилище
   - Контекстный поиск

4. **ChromaDB** (опционально)
   - Векторный поиск
   - Семантическое сходство
   - Быстрый retrieval

### Установка дополнительной памяти

```bash
# Task-Centric Memory
pip install autogen-ext[task-centric-memory]

# Mem0
pip install autogen-ext[mem0] mem0ai

# ChromaDB
pip install autogen-ext[chromadb] chromadb sentence-transformers
```

## 🔧 Конфигурация

### Environment Variables

```bash
# Обязательные
CODEGEN_ORG_ID=your_org_id
CODEGEN_API_TOKEN=your_token
OPENAI_API_KEY=your_key

# Опциональные
MODEL_NAME=gpt-4-turbo-preview  # Модель OpenAI
MEMORY_RESET=false              # Сброс памяти при запуске
MEMORY_PATH=./boss_memories     # Путь к хранилищу
LOG_LEVEL=INFO                  # Уровень логирования
LOG_PATH=./logs                 # Путь к логам
```

### Docker Volumes

```yaml
volumes:
  - ./pagelogs:/app/pagelogs              # Task-centric memory logs
  - ./boss_mem0_storage:/app/boss_mem0_storage  # Mem0 storage
  - ./boss_chroma_db:/app/boss_chroma_db  # ChromaDB storage
  - ./logs:/app/logs                      # Application logs
```

## 📊 Мониторинг

### Логи

```bash
# Все логи
docker-compose logs -f

# Только boss agent
docker-compose logs -f ultimate-boss-memory

# Последние 100 строк
docker-compose logs --tail=100
```

### Health Check

```bash
# Проверка здоровья
curl http://localhost:8000/health

# Ожидаемый ответ:
{
  "status": "healthy",
  "components": {
    "codegen": true,
    "memory": true,
    "model": true
  }
}
```

### Memory Stats

```bash
# Статистика памяти
curl http://localhost:8000/memory/stats

# Ожидаемый ответ:
{
  "total_memories": 25,
  "total_solutions": 8,
  "active_delegations": 2,
  "memory_types": {
    "simple": true,
    "task_centric": true,
    "mem0": true,
    "vector": true
  }
}
```

## 🧪 Тестирование

### Запуск тестов

```bash
# Все тесты
python test_boss.py

# Или через Docker
docker-compose exec ultimate-boss-memory python test_boss.py
```

### Unit тесты

```bash
# Создайте tests/ директорию
mkdir tests

# Запустите pytest
pytest tests/
```

## 🔍 Troubleshooting

### Проблема: Service не стартует

```bash
# Проверьте логи
docker-compose logs

# Пересоберите образ
docker-compose build --no-cache

# Перезапустите
docker-compose down
docker-compose up -d
```

### Проблема: API ключи не работают

```bash
# Проверьте .env
cat .env

# Убедитесь что нет пробелов
CODEGEN_API_TOKEN=your_token  # ✓ Правильно
CODEGEN_API_TOKEN = your_token  # ✗ Неправильно

# Перезапустите после изменений
docker-compose restart
```

### Проблема: Память не сохраняется

```bash
# Проверьте volumes
docker-compose down
ls -la ./boss_mem0_storage
ls -la ./boss_chroma_db

# Пересоздайте volumes
docker-compose up -d
```

## 📚 Best Practices

### 1. Регулярно обучайте босса

```python
# Добавляйте уроки из реального опыта
await client.post("/teach", json={
    "lesson": "Always validate user input before processing"
})
```

### 2. Демонстрируйте успешные решения

```python
# Сохраняйте proven solutions
await client.post("/demonstrate", json={
    "task": "Deploy to production",
    "solution": "Your working process"
})
```

### 3. Мониторьте память

```python
# Регулярно проверяйте статистику
stats = await client.get("/memory/stats")
print(f"Total memories: {stats.json()['total_memories']}")
```

### 4. Используйте правильные режимы

```python
# Простые задачи
mode = "boss"

# Сложные multi-step задачи
mode = "team"

# Экспериментальные задачи
mode = "learn"
```

### 5. Backup памяти

```bash
# Регулярно делайте backup
tar -czf boss_memory_backup.tar.gz \
  boss_mem0_storage \
  boss_chroma_db \
  pagelogs
```

## 🚀 Production Deployment

### Docker в production

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  ultimate-boss-memory:
    image: your-registry/ultimate-boss:latest
    restart: always
    environment:
      - CODEGEN_ORG_ID=${CODEGEN_ORG_ID}
      - CODEGEN_API_TOKEN=${CODEGEN_API_TOKEN}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - boss_memory:/app/boss_mem0_storage
      - boss_vector:/app/boss_chroma_db
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  boss_memory:
  boss_vector:
```

### Kubernetes

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ultimate-boss
spec:
  replicas: 2
  selector:
    matchLabels:
      app: ultimate-boss
  template:
    metadata:
      labels:
        app: ultimate-boss
    spec:
      containers:
      - name: boss
        image: your-registry/ultimate-boss:latest
        ports:
        - containerPort: 8000
        env:
        - name: CODEGEN_ORG_ID
          valueFrom:
            secretKeyRef:
              name: boss-secrets
              key: org-id
        volumeMounts:
        - name: memory
          mountPath: /app/boss_mem0_storage
      volumes:
      - name: memory
        persistentVolumeClaim:
          claimName: boss-memory-pvc
```

## 💬 Support

- GitHub Issues: [Report a bug](https://github.com/evgenygurin/agent-boss/issues)
- Documentation: [Full docs](https://github.com/evgenygurin/agent-boss)

---

Made with ❤️ by [Evgeny Gurin](https://github.com/evgenygurin)

