# 🏗️ Ultimate Boss Agent - Architecture

## Обзор

Ultimate Boss Agent - это интеллектуальная система делегирования задач с тройной системой памяти, которая полностью интегрирована с Codegen API для выполнения всех задач.

## Архитектурные принципы

### 1. **100% Делегирование**
- Босс НИКОГДА не выполняет задачи сам
- ВСЕ задачи делегируются через Codegen API
- Босс только координирует и учится

### 2. **Память превыше всего**
- Каждое действие записывается
- Каждая ошибка становится уроком
- Каждый успех становится паттерном

### 3. **Непрерывное обучение**
- Автоматическое обучение на результатах
- Явное обучение от пользователя
- Обучение через демонстрации

## Компоненты системы

```
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Application                       │
│                   (API Layer)                               │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│           UltimateMemoryOrchestrator                        │
│  - Координация всех компонентов                             │
│  - Выбор стратегии обработки                                │
│  - Управление запросами                                     │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
         ▼                               ▼
┌──────────────────┐           ┌──────────────────┐
│ ApprenticeBoss   │           │ MemoryEnabledTeam│
│                  │           │                  │
│ - Обучение       │           │ - Analyst        │
│ - Повторы        │           │ - Coordinator    │
│ - Практика       │           │ - Boss           │
└────────┬─────────┘           └────────┬─────────┘
         │                               │
         └───────────────┬───────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              UltimateBossWithMemory                         │
│                                                             │
│  CORE RESPONSIBILITIES:                                     │
│  1. Делегирование через Codegen API                         │
│  2. Мониторинг выполнения                                   │
│  3. Обучение на результатах                                 │
│  4. Управление памятью                                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  BossMemorySystem                           │
│                                                             │
│  ┌──────────────────────────────────────────────┐          │
│  │  Task-Centric Memory (MemoryController)      │          │
│  │  - Паттерны решений                           │          │
│  │  - Успешные подходы                           │          │
│  │  - Инструкции по типам задач                  │          │
│  └──────────────────────────────────────────────┘          │
│                                                             │
│  ┌──────────────────────────────────────────────┐          │
│  │  Mem0 Memory                                  │          │
│  │  - История делегирований                      │          │
│  │  - Уроки от пользователя                      │          │
│  │  - Анализ ошибок                              │          │
│  └──────────────────────────────────────────────┘          │
│                                                             │
│  ┌──────────────────────────────────────────────┐          │
│  │  ChromaDB Vector Memory                       │          │
│  │  - Векторный поиск                            │          │
│  │  - Семантическая близость                     │          │
│  │  - Контекстуальные связи                      │          │
│  └──────────────────────────────────────────────┘          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              CodegenAPIClient                               │
│                                                             │
│  METHODS:                                                   │
│  - create_agent_run()  : Создание агента                    │
│  - get_agent_run()     : Получение статуса                  │
│  - get_agent_logs()    : Получение логов                    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
                   Codegen API
                   (External Service)
```

## Потоки данных

### 1. Простое делегирование (mode: boss)

```
User Request
    │
    ▼
FastAPI (/process)
    │
    ▼
UltimateMemoryOrchestrator
    │
    ▼
ApprenticeBoss.boss.delegate_with_memory()
    │
    ├─→ BossMemorySystem.recall_best_approach()
    │   ├─→ Task-Centric Memory (ищем паттерны)
    │   └─→ ChromaDB (векторный поиск)
    │
    ▼
CodegenAPIClient.create_agent_run()
    │
    ▼
Codegen API (создание агента)
    │
    ▼
Background Monitoring (_monitor_and_learn)
    │
    ├─→ Периодическая проверка статуса
    │
    └─→ При завершении:
        ├─→ BossMemorySystem.remember_delegation()
        │   ├─→ Task-Centric Memory (паттерн)
        │   ├─→ Mem0 (история)
        │   └─→ ChromaDB (вектор)
        │
        └─→ При ошибке:
            └─→ BossMemorySystem.learn_from_failure()
```

### 2. Командное делегирование (mode: team)

```
Complex Task
    │
    ▼
MemoryEnabledTeam.process_complex_task()
    │
    ├─→ Analyst.run() (анализ задачи)
    │   │
    │   └─→ Использует Mem0 Memory
    │
    ├─→ Coordinator.run() (создание плана)
    │   │
    │   └─→ Использует Vector Memory
    │
    └─→ Boss.delegate_with_memory() (для каждой подзадачи)
        │
        └─→ Множественные делегирования через Codegen
```

### 3. Режим обучения (mode: learn)

```
Task with Learning
    │
    ▼
ApprenticeBoss.process_with_learning()
    │
    ├─→ Boss.delegate_with_memory() (первая попытка)
    │   │
    │   ▼
    │   Codegen Agent Execution
    │   │
    │   ▼
    │   Status Check
    │   │
    │   ├─→ Success: сохранить паттерн
    │   │
    │   └─→ Failure:
    │       ├─→ BossMemorySystem.learn_from_failure()
    │       └─→ Retry с новым знанием
    │
    └─→ Итеративное улучшение
```

## Система памяти

### Task-Centric Memory (MemoryController)

**Назначение:** Хранение проверенных решений и паттернов

**Структура:**
```python
{
    "task": "How to handle bug_fix tasks",
    "insight": "1. Reproduce\n2. Identify\n3. Fix\n4. Test\n5. Verify"
}
```

**API:**
- `add_memo(task, insight)` - добавить знание
- `retrieve_relevant_memos(task)` - найти релевантные
- `add_task_solution_pair_to_memory(task, solution)` - сохранить решение

**Использование:**
- Базовые паттерны делегирования
- Инструкции по типам задач
- Codegen API best practices

### Mem0 Memory

**Назначение:** Долгосрочная персистентная память

**Структура:**
```python
MemoryContent(
    content="Delegation 123: Fix bug - Success: True",
    mime_type=MemoryMimeType.TEXT,
    metadata={
        "agent_id": "123",
        "success": True,
        "timestamp": "2024-01-01T10:00:00"
    }
)
```

**Хранение:**
- История всех делегирований
- Уроки от пользователя (через /teach)
- Анализ ошибок и неудач

**Персистентность:**
- Файловая система: `./boss_mem0_storage/`
- Сохраняется между перезапусками

### ChromaDB Vector Memory

**Назначение:** Семантический поиск похожих задач

**Особенности:**
- Embedding модель: `all-MiniLM-L6-v2`
- Векторное представление задач
- Поиск по семантической близости

**Структура:**
```python
MemoryContent(
    content="Task: Fix auth bug\nResult: {...}",
    mime_type=MemoryMimeType.TEXT,
    metadata={
        "type": "delegation",
        "success": True
    }
)
```

**Использование:**
- Поиск похожих задач из прошлого
- Нахождение релевантных решений
- Контекстуальные рекомендации

## Процесс обучения

### 1. Автоматическое обучение

```python
async def _monitor_and_learn(self, agent_id: str):
    # Мониторинг выполнения
    status = await self.codegen.get_agent_run(agent_id)
    
    if status["status"] == "completed":
        # Успех → сохранить паттерн
        await self.memory_system.remember_delegation(
            agent_id, task, result, success=True
        )
    
    elif status["status"] == "failed":
        # Ошибка → учиться
        error = self._extract_error_from_logs(logs)
        await self.memory_system.learn_from_failure(task, error)
```

### 2. Явное обучение (от пользователя)

```python
@app.post("/teach")
async def teach_boss(request: TeachRequest):
    # Пользователь обучает босса
    await orchestrator.apprentice_boss.boss.teach_me(request.lesson)
```

### 3. Обучение через демонстрации

```python
@app.post("/demonstrate")
async def demonstrate_solution(request: DemonstrateRequest):
    # Показать правильное решение
    await orchestrator.apprentice_boss.demonstrate_solution(
        request.task, 
        request.solution
    )
```

## Выбор стратегии

```python
async def process_request(self, request: str, mode: str = "auto"):
    if mode == "auto":
        # Автоматическое определение
        if "complex" in request.lower() or "multi" in request.lower():
            mode = "team"
        else:
            mode = "boss"
    
    if mode == "boss":
        # Простое делегирование
        return await self.apprentice_boss.boss.delegate_with_memory(request)
    
    elif mode == "team":
        # Командная работа
        return await self.team.process_complex_task(request)
    
    elif mode == "learn":
        # С обучением и повторами
        return await self.apprentice_boss.process_with_learning(
            request, allow_retry=True
        )
```

## Интеграция с Codegen

### Создание агента

```python
result = await self.codegen.create_agent_run(
    prompt=enhanced_prompt_with_memory,
    repo_id=optional_repo_id,
    parent_agent_run_id=optional_parent_id
)
```

### Мониторинг

```python
# Асинхронный фоновый мониторинг
asyncio.create_task(self._monitor_and_learn(agent_id))

# Периодическая проверка статуса
status = await self.codegen.get_agent_run(agent_id)

# Получение детальных логов
logs = await self.codegen.get_agent_logs(agent_id)
```

### Иерархическое делегирование

```python
# Родительский агент
parent_result = await self.codegen.create_agent_run(
    prompt="Complex task"
)

# Дочерние агенты
for subtask in subtasks:
    child_result = await self.codegen.create_agent_run(
        prompt=subtask,
        parent_agent_run_id=parent_result["id"]
    )
```

## Персистентность

### Файловая структура

```
agent-boss/
├── boss_mem0_storage/       # Mem0 данные
├── boss_chroma_db/          # ChromaDB данные
├── pagelogs/                # Task-Centric Memory логи
├── boss_teachability_db/    # База обучаемости
└── logs/                    # Application логи
```

### Docker Volumes

```yaml
volumes:
  - ./pagelogs:/app/pagelogs
  - ./boss_teachability_db:/app/boss_teachability_db
  - ./boss_mem0_storage:/app/boss_mem0_storage
  - ./boss_chroma_db:/app/boss_chroma_db
  - ./logs:/app/logs
```

## Масштабирование

### Горизонтальное

- Множественные инстансы босса
- Общая база данных ChromaDB
- Redis для координации

### Вертикальное

- Увеличение размера embedding модели
- Больший контекст для LLM
- Расширенная история в памяти

## Безопасность

### API Keys

- Хранение в переменных окружения
- Никогда не логируются
- Не попадают в git

### Валидация

- Pydantic модели для API
- Проверка входных данных
- Timeout для всех запросов

### Изоляция

- Docker контейнеры
- Отдельные volumes
- Network isolation

## Мониторинг и метрики

### Доступные endpoint'ы

```python
GET /memory/stats        # Статистика памяти
GET /memory/search       # Поиск в памяти
GET /health              # Health check (TODO)
GET /metrics             # Prometheus metrics (TODO)
```

### Логирование

```python
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Все операции логируются
logger.info(f"Delegation {agent_id} completed")
logger.error(f"Error monitoring {agent_id}: {e}")
```

## Расширения

### Возможные интеграции

1. **Linear** - автоматическое создание задач
2. **Slack** - уведомления о статусе
3. **Sentry** - мониторинг ошибок
4. **Grafana** - визуализация метрик
5. **Prometheus** - сбор метрик

### Будущие улучшения

1. Multi-tenant support
2. A/B тестирование стратегий
3. Advanced analytics dashboard
4. Reinforcement learning для оптимизации
5. Real-time collaboration между боссами

---

**Версия:** 1.0.0  
**Последнее обновление:** 2024-01-01  
**Автор:** Ultimate Boss Team
