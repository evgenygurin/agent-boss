# ultimate_boss_with_memory.py
import asyncio
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import json
import logging

# Autogen imports
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console

# Task-Centric Memory
try:
    from autogen_core.memory import (
        Memory,
        MemoryContent,
        MemoryMimeType,
        MemoryQueryResult
    )
    from autogen_ext.experimental.task_centric_memory import (
        MemoryController,
        MemoryControllerConfig
    )
    from autogen_ext.experimental.task_centric_memory.utils import (
        PageLogger,
        Apprentice,
        ApprenticeConfig,
        Teachability
    )
    MEMORY_AVAILABLE = True
except ImportError:
    MEMORY_AVAILABLE = False
    logging.warning("Task-Centric Memory not available. Install: pip install autogen-ext[task-centric-memory]")

# Memory stores
try:
    from autogen_ext.memory.mem0 import Mem0Memory, Mem0MemoryConfig
    MEM0_AVAILABLE = True
except ImportError:
    MEM0_AVAILABLE = False
    logging.warning("Mem0 not available. Install: pip install autogen-ext[mem0]")

try:
    from autogen_ext.memory.chromadb import (
        ChromaDBVectorMemory,
        ChromaDBVectorMemoryConfig,
        SentenceTransformerEmbeddingFunctionConfig
    )
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    logging.warning("ChromaDB not available. Install: pip install autogen-ext[chromadb]")

# Models
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Codegen client
import httpx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === CODEGEN API CLIENT ===

class CodegenAPIClient:
    """Полный клиент для работы с Codegen API"""
    
    def __init__(self, org_id: str, token: str):
        self.org_id = org_id
        self.token = token
        self.base_url = "https://api.codegen.com/v1"
        self.headers = {"Authorization": f"Bearer {token}"}
    
    async def create_agent_run(
        self,
        prompt: str,
        repo_id: Optional[int] = None,
        parent_agent_run_id: Optional[int] = None,
        **kwargs
    ) -> Dict:
        """Создает агента в Codegen"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.base_url}/organizations/{self.org_id}/agent/run",
                headers=self.headers,
                json={
                    "prompt": prompt,
                    "repo_id": repo_id,
                    "parent_agent_run_id": parent_agent_run_id,
                    **kwargs
                }
            )
            response.raise_for_status()
            return response.json()
    
    async def get_agent_run(self, agent_run_id: int) -> Dict:
        """Получает статус агента"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{self.base_url}/organizations/{self.org_id}/agent/run/{agent_run_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
    
    async def get_agent_logs(
        self,
        agent_run_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> Dict:
        """Получает детальные логи агента"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{self.base_url}/alpha/organizations/{self.org_id}/agent/run/{agent_run_id}/logs",
                headers=self.headers,
                params={"skip": skip, "limit": limit}
            )
            response.raise_for_status()
            return response.json()

# === SIMPLE MEMORY FALLBACK ===

class SimpleMemory:
    """Простая память на случай отсутствия продвинутых библиотек"""
    
    def __init__(self):
        self.memories: List[Dict] = []
        self.task_solutions: Dict[str, str] = {}
    
    async def add(self, content: str, metadata: Optional[Dict] = None):
        """Добавляет воспоминание"""
        self.memories.append({
            "content": content,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        })
    
    async def query(self, query: str, limit: int = 10) -> List[Dict]:
        """Простой поиск по ключевым словам"""
        results = []
        query_lower = query.lower()
        
        for memory in reversed(self.memories):
            if query_lower in memory["content"].lower():
                results.append(memory)
                if len(results) >= limit:
                    break
        
        return results
    
    async def add_task_solution(self, task: str, solution: str):
        """Сохраняет пару задача-решение"""
        self.task_solutions[task] = solution
    
    async def get_solution(self, task: str) -> Optional[str]:
        """Ищет решение для задачи"""
        task_lower = task.lower()
        for saved_task, solution in self.task_solutions.items():
            if task_lower in saved_task.lower() or saved_task.lower() in task_lower:
                return solution
        return None

# === SMART MEMORY SYSTEM ===

class BossMemorySystem:
    """Комплексная система памяти босса"""
    
    def __init__(self, model_client: OpenAIChatCompletionClient):
        self.model_client = model_client
        
        # Простая память как fallback
        self.simple_memory = SimpleMemory()
        
        # Task-Centric Memory Controller (если доступен)
        if MEMORY_AVAILABLE:
            try:
                os.makedirs("./pagelogs/boss", exist_ok=True)
                self.memory_controller = MemoryController(
                    reset=False,
                    client=model_client._impl,
                    logger=PageLogger(config={"level": "INFO", "path": "./pagelogs/boss"})
                )
                logger.info("Task-Centric Memory initialized")
            except Exception as e:
                logger.warning(f"Failed to init Task-Centric Memory: {e}")
                self.memory_controller = None
        else:
            self.memory_controller = None
        
        # Mem0 для долгосрочной памяти (если доступен)
        if MEM0_AVAILABLE:
            try:
                os.makedirs("./boss_mem0_storage", exist_ok=True)
                self.mem0_memory = Mem0Memory(
                    is_cloud=False,
                    config={"path": "./boss_mem0_storage"},
                    user_id="boss",
                    limit=10
                )
                logger.info("Mem0 Memory initialized")
            except Exception as e:
                logger.warning(f"Failed to init Mem0: {e}")
                self.mem0_memory = None
        else:
            self.mem0_memory = None
        
        # ChromaDB для векторного поиска (если доступен)
        if CHROMADB_AVAILABLE:
            try:
                os.makedirs("./boss_chroma_db", exist_ok=True)
                self.vector_memory = ChromaDBVectorMemory(
                    config=ChromaDBVectorMemoryConfig(
                        collection_name="boss_memories",
                        persist_directory="./boss_chroma_db",
                        embedding_function=SentenceTransformerEmbeddingFunctionConfig(
                            model_name="all-MiniLM-L6-v2"
                        )
                    )
                )
                logger.info("ChromaDB Vector Memory initialized")
            except Exception as e:
                logger.warning(f"Failed to init ChromaDB: {e}")
                self.vector_memory = None
        else:
            self.vector_memory = None
        
        # Инициализация базовых знаний
        asyncio.create_task(self._initialize_base_knowledge())
    
    async def _initialize_base_knowledge(self):
        """Загружает базовые знания о делегировании"""
        
        # Паттерны успешного делегирования
        delegation_patterns = [
            ("bug_fix", "1. Reproduce issue\n2. Identify root cause\n3. Fix\n4. Test\n5. Verify"),
            ("feature", "1. Design\n2. Implement\n3. Test\n4. Document\n5. PR"),
            ("review", "Focus on: Security, Performance, Quality, Best practices"),
            ("multi_agent", "1. Break down\n2. Create sub-issues\n3. Assign agents\n4. Monitor")
        ]
        
        for task_type, pattern in delegation_patterns:
            task = f"How to handle {task_type} tasks"
            
            # Сохраняем в простую память
            await self.simple_memory.add_task_solution(task, pattern)
            
            # Если доступен memory_controller
            if self.memory_controller:
                try:
                    await self.memory_controller.add_memo(
                        task=task,
                        insight=pattern
                    )
                except Exception as e:
                    logger.debug(f"Could not add memo: {e}")
        
        logger.info("Base knowledge initialized")
    
    async def remember_delegation(
        self,
        agent_id: str,
        task: str,
        result: Dict,
        success: bool
    ):
        """Запоминает результат делегирования"""
        
        content = f"Delegation {agent_id}: {task} - Success: {success}"
        metadata = {
            "agent_id": agent_id,
            "success": success,
            "timestamp": datetime.now().isoformat()
        }
        
        # Простая память
        await self.simple_memory.add(content, metadata)
        
        # Task-centric memory (если доступен)
        if self.memory_controller and success:
            try:
                await self.memory_controller.add_task_solution_pair_to_memory(
                    task=task,
                    solution=json.dumps(result)[:500]
                )
            except Exception as e:
                logger.debug(f"Could not add to memory controller: {e}")
        
        # Mem0 (если доступен)
        if self.mem0_memory:
            try:
                await self.mem0_memory.add(
                    MemoryContent(
                        content=content,
                        mime_type=MemoryMimeType.TEXT,
                        metadata=metadata
                    )
                )
            except Exception as e:
                logger.debug(f"Could not add to Mem0: {e}")
        
        # Vector memory (если доступен)
        if self.vector_memory:
            try:
                await self.vector_memory.add(
                    MemoryContent(
                        content=f"{task}\n{json.dumps(result)}",
                        mime_type=MemoryMimeType.TEXT,
                        metadata={"type": "delegation", "success": success}
                    )
                )
            except Exception as e:
                logger.debug(f"Could not add to vector memory: {e}")
    
    async def recall_best_approach(self, task: str) -> Optional[str]:
        """Вспоминает лучший подход для задачи"""
        
        # Простая память
        solution = await self.simple_memory.get_solution(task)
        if solution:
            return solution
        
        # Task-centric memory (если доступен)
        if self.memory_controller:
            try:
                memos = await self.memory_controller.retrieve_relevant_memos(task)
                if memos:
                    return memos[0].insight
            except Exception as e:
                logger.debug(f"Could not retrieve from memory controller: {e}")
        
        # Vector memory (если доступен)
        if self.vector_memory:
            try:
                results = await self.vector_memory.query(task)
                if results.results:
                    return results.results[0].content
            except Exception as e:
                logger.debug(f"Could not query vector memory: {e}")
        
        return None
    
    async def learn_from_failure(self, task: str, error: str):
        """Учится на ошибках"""
        
        # Простая память
        await self.simple_memory.add(
            f"Failed approach for {task}: {error}",
            {"type": "failure", "task": task}
        )
        
        # Memory controller (если доступен)
        if self.memory_controller:
            try:
                await self.memory_controller.add_memo(
                    task=task,
                    insight=f"Error encountered: {error}. Avoid this approach."
                )
            except Exception as e:
                logger.debug(f"Could not add failure memo: {e}")
        
        # Mem0 (если доступен)
        if self.mem0_memory:
            try:
                await self.mem0_memory.add(
                    MemoryContent(
                        content=f"Failed approach for {task}: {error}",
                        mime_type=MemoryMimeType.TEXT,
                        metadata={"type": "failure", "task": task}
                    )
                )
            except Exception as e:
                logger.debug(f"Could not add failure to Mem0: {e}")

# === MEMORY-ENABLED BOSS AGENT ===

class UltimateBossWithMemory(AssistantAgent):
    """Босс-агент с полной памятью и делегированием через Codegen"""
    
    def __init__(
        self,
        codegen_client: CodegenAPIClient,
        memory_system: BossMemorySystem,
        model_client: OpenAIChatCompletionClient,
        **kwargs
    ):
        super().__init__(
            name="UltimateBoss",
            model_client=model_client,
            system_message="""You are the ULTIMATE BOSS AGENT with PERFECT MEMORY who delegates ALL tasks through Codegen.

KEY PRINCIPLES:
1. You NEVER write code yourself - ONLY delegate through Codegen API
2. You REMEMBER everything - every delegation, result, and learning
3. You LEARN from past experiences to optimize future delegations
4. You COORDINATE multiple agents for complex tasks

YOUR MEMORY CAPABILITIES:
- Task-centric memory for proven solutions
- Long-term memory of all delegations
- Learning from failures and successes

DELEGATION STRATEGY:
1. Check memory for similar past tasks
2. Apply learned patterns and avoid past mistakes
3. Create optimized Codegen agents
4. Monitor and learn from results
5. Update memory with new insights

Always mention when using past experience: "Based on past experience with X..."
Never repeat past mistakes - always check what failed before.""",
            **kwargs
        )
        
        self.codegen = codegen_client
        self.memory_system = memory_system
        self.active_delegations = {}
    
    async def delegate_with_memory(
        self,
        task: str,
        task_type: str = "general"
    ) -> Dict:
        """Делегирует задачу, используя память"""
        
        # Проверяем память для похожих задач
        best_approach = await self.memory_system.recall_best_approach(task)
        
        # Формируем промпт с учетом памяти
        if best_approach:
            prompt = f"""Task: {task}

Based on past successful approaches:
{best_approach}

Apply these insights to complete the task efficiently."""
            logger.info(f"Using memory-informed approach for: {task}")
        else:
            prompt = f"Complete task: {task}"
            logger.info(f"No prior memory found for: {task}")
        
        # Создаем агента в Codegen
        result = await self.codegen.create_agent_run(prompt=prompt)
        agent_id = result["id"]
        
        # Сохраняем активное делегирование
        self.active_delegations[agent_id] = {
            "task": task,
            "type": task_type,
            "started_at": datetime.now(),
            "used_memory": bool(best_approach)
        }
        
        # Запускаем мониторинг
        asyncio.create_task(self._monitor_and_learn(agent_id))
        
        return {
            "agent_id": agent_id,
            "status": "delegated",
            "used_memory": bool(best_approach),
            "web_url": result.get("web_url")
        }
    
    async def _monitor_and_learn(self, agent_id: str):
        """Мониторит агента и учится на результатах"""
        
        max_checks = 60
        for _ in range(max_checks):
            try:
                # Получаем статус
                status = await self.codegen.get_agent_run(int(agent_id))
                
                if status["status"] in ["completed", "failed"]:
                    # Получаем детальные логи для анализа
                    try:
                        logs = await self.codegen.get_agent_logs(int(agent_id))
                    except:
                        logs = {"logs": []}
                    
                    # Анализируем результат
                    success = status["status"] == "completed"
                    task = self.active_delegations[agent_id]["task"]
                    
                    # Запоминаем результат
                    await self.memory_system.remember_delegation(
                        agent_id=agent_id,
                        task=task,
                        result=status.get("result", {}),
                        success=success
                    )
                    
                    # Если неудача - учимся
                    if not success:
                        error = self._extract_error_from_logs(logs)
                        await self.memory_system.learn_from_failure(task, error)
                    
                    logger.info(f"Delegation {agent_id} completed. Success: {success}")
                    break
                
                await asyncio.sleep(10)
                
            except Exception as e:
                logger.error(f"Error monitoring {agent_id}: {e}")
                break
    
    def _extract_error_from_logs(self, logs: Dict) -> str:
        """Извлекает ошибки из логов"""
        errors = []
        for log in logs.get("logs", []):
            if log.get("message_type") == "ERROR":
                errors.append(log.get("observation", "Unknown error"))
        
        return " | ".join(errors) if errors else "Unknown error"

# === TEAM OF MEMORY-ENABLED AGENTS ===

class MemoryEnabledTeam:
    """Команда агентов с общей памятью"""
    
    def __init__(
        self,
        codegen_client: CodegenAPIClient,
        model_client: OpenAIChatCompletionClient
    ):
        # Общая память для команды
        self.shared_memory = BossMemorySystem(model_client)
        
        # Босс с памятью
        self.boss = UltimateBossWithMemory(
            codegen_client=codegen_client,
            memory_system=self.shared_memory,
            model_client=model_client
        )
        
        # Аналитик
        self.analyst = AssistantAgent(
            name="Analyst",
            model_client=model_client,
            system_message="You analyze tasks and provide insights."
        )
        
        # Координатор
        self.coordinator = AssistantAgent(
            name="Coordinator",
            model_client=model_client,
            system_message="You coordinate between agents."
        )
        
        # Создаем команду
        self.team = RoundRobinGroupChat(
            participants=[self.boss, self.analyst, self.coordinator]
        )
    
    async def process_complex_task(self, task: str) -> Dict:
        """Обрабатывает сложную задачу командой"""
        
        # Босс делегирует через Codegen
        delegation = await self.boss.delegate_with_memory(
            task=task,
            task_type="complex"
        )
        
        return {
            "task": task,
            "delegation": delegation,
            "team": "boss + analyst + coordinator"
        }

# === MAIN ORCHESTRATOR ===

class UltimateMemoryOrchestrator:
    """Главный оркестратор с полной памятью"""
    
    def __init__(
        self,
        codegen_org_id: str,
        codegen_token: str,
        openai_key: str
    ):
        # Model client
        self.model_client = OpenAIChatCompletionClient(
            model="gpt-4-turbo-preview",
            api_key=openai_key
        )
        
        # Codegen client
        self.codegen = CodegenAPIClient(codegen_org_id, codegen_token)
        
        # Memory system
        self.memory = BossMemorySystem(self.model_client)
        
        # Boss agent
        self.boss = UltimateBossWithMemory(
            codegen_client=self.codegen,
            memory_system=self.memory,
            model_client=self.model_client
        )
        
        # Team для сложных задач
        self.team = MemoryEnabledTeam(
            codegen_client=self.codegen,
            model_client=self.model_client
        )
    
    async def process_request(
        self,
        request: str,
        mode: str = "auto"
    ) -> Dict:
        """Обрабатывает запрос с автоматическим выбором стратегии"""
        
        if mode == "auto":
            # Определяем сложность
            if "complex" in request.lower() or "multi" in request.lower():
                mode = "team"
            else:
                mode = "boss"
        
        if mode == "boss":
            # Простое делегирование через босса
            result = await self.boss.delegate_with_memory(request)
            
        elif mode == "team":
            # Сложная задача через команду
            result = await self.team.process_complex_task(request)
            
        elif mode == "learn":
            # Обучение через практику (с retry)
            result = await self.boss.delegate_with_memory(request)
        
        return result
    
    async def teach(self, lesson: str):
        """Обучает систему новому знанию"""
        await self.memory.simple_memory.add(
            f"User lesson: {lesson}",
            {"type": "teaching", "source": "user"}
        )
        return {"status": "learned", "lesson": lesson}
    
    async def demonstrate(self, task: str, solution: str):
        """Демонстрирует решение для обучения"""
        await self.memory.simple_memory.add_task_solution(task, solution)
        return {"status": "demonstrated", "task": task}

# === API SERVER ===

from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel

app = FastAPI(title="Ultimate Boss with Memory API")

orchestrator = None

@app.on_event("startup")
async def startup():
    global orchestrator
    orchestrator = UltimateMemoryOrchestrator(
        codegen_org_id=os.getenv("CODEGEN_ORG_ID", ""),
        codegen_token=os.getenv("CODEGEN_API_TOKEN", ""),
        openai_key=os.getenv("OPENAI_API_KEY", "")
    )

class TaskRequest(BaseModel):
    task: str
    mode: str = "auto"  # auto, boss, team, learn

class TeachRequest(BaseModel):
    lesson: str

class DemonstrateRequest(BaseModel):
    task: str
    solution: str

@app.post("/process")
async def process_task(request: TaskRequest):
    """Обрабатывает задачу с памятью"""
    result = await orchestrator.process_request(
        request.task,
        request.mode
    )
    return result

@app.post("/teach")
async def teach_boss(request: TeachRequest):
    """Обучает босса новому знанию"""
    result = await orchestrator.teach(request.lesson)
    return result

@app.post("/demonstrate")
async def demonstrate_solution(request: DemonstrateRequest):
    """Демонстрирует решение"""
    result = await orchestrator.demonstrate(
        request.task,
        request.solution
    )
    return result

@app.get("/memory/search")
async def search_memory(query: str):
    """Ищет в памяти босса"""
    results = await orchestrator.memory.simple_memory.query(query)
    return {"results": results}

@app.get("/memory/stats")
async def memory_stats():
    """Статистика памяти"""
    return {
        "total_memories": len(orchestrator.memory.simple_memory.memories),
        "total_solutions": len(orchestrator.memory.simple_memory.task_solutions),
        "active_delegations": len(orchestrator.boss.active_delegations),
        "memory_types": {
            "simple": True,
            "task_centric": orchestrator.memory.memory_controller is not None,
            "mem0": orchestrator.memory.mem0_memory is not None,
            "vector": orchestrator.memory.vector_memory is not None
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "components": {
            "codegen": bool(orchestrator.codegen.token),
            "memory": True,
            "model": bool(orchestrator.model_client)
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

