# 🚀 Quick Reference Guide

> Шпаргалка для повседневной работы с Git Flow

## 🎯 Общие команды

### Начать новую фичу
```bash
git checkout dev
git pull origin dev
git checkout -b feature/название-фичи
```

### Коммит изменений
```bash
git add .
git commit -m "feat: описание фичи"
git push origin feature/название-фичи
```

### Создать PR
1. Открыть GitHub
2. New Pull Request
3. Выбрать: `feature/название-фичи` → `dev`
4. Заполнить PR template
5. Submit

## 🔧 Dev Environment

### Проверить статус
```bash
git checkout dev
git pull origin dev
git log --oneline -5
```

### Обновить свою feature branch
```bash
git checkout feature/моя-фича
git merge dev
git push origin feature/моя-фича
```

## 🎭 Staging Promotion

### Промоутить dev в stage
```bash
git checkout stage
git pull origin stage
git checkout -b promote/dev-to-stage-$(date +%Y%m%d)
git merge dev
git push origin promote/dev-to-stage-$(date +%Y%m%d)
```

Затем создать PR: `promote/dev-to-stage-*` → `stage`

## 🚀 Production Release

### Создать релиз
```bash
git checkout prod
git pull origin prod
git checkout -b release/v1.2.3
git merge stage
git push origin release/v1.2.3
```

Затем создать PR: `release/v1.2.3` → `prod`

**⚠️ Требуется 2+ аппрува!**

## 🔥 Hotfix (Emergency)

### Создать hotfix
```bash
git checkout prod
git pull origin prod
git checkout -b hotfix/критичный-баг
# Исправить баг
git add .
git commit -m "fix: критичный баг в продакшене"
git push origin hotfix/критичный-баг
```

### После мерджа в prod - backport
```bash
# Обновить stage
git checkout stage
git merge prod
git push origin stage

# Обновить dev
git checkout dev
git merge stage
git push origin dev
```

## 📋 Conventional Commits

```bash
feat:     новая фича
fix:      исправление бага
docs:     документация
style:    форматирование
refactor: рефакторинг
test:     тесты
chore:    рутинные задачи
```

### Примеры
```bash
git commit -m "feat: add user authentication"
git commit -m "fix: resolve login bug"
git commit -m "docs: update API documentation"
git commit -m "refactor: improve code structure"
```

## 🔍 Проверка статуса

### Локальный статус
```bash
git status
git log --oneline -5
git branch -a
```

### Удаленный статус
```bash
gh workflow list
gh run list --limit 5
gh pr list
```

### Проверить workflows
```bash
# Список workflows
gh workflow list

# Последние запуски
gh run list --branch dev --limit 3
gh run list --branch stage --limit 3
gh run list --branch prod --limit 3
```

## 🌐 URLs

### Сайт
- Production: https://evgenygurin.github.io/agent-boss/

### GitHub
- Repo: https://github.com/evgenygurin/agent-boss
- Actions: https://github.com/evgenygurin/agent-boss/actions
- PRs: https://github.com/evgenygurin/agent-boss/pulls

## 🆘 Быстрые решения

### Откатить последний коммит (локально)
```bash
git reset HEAD~1
```

### Отменить изменения в файле
```bash
git checkout -- имя-файла
```

### Синхронизировать с upstream
```bash
git fetch origin
git rebase origin/dev
```

### Удалить feature branch после мерджа
```bash
git branch -d feature/название-фичи
git push origin --delete feature/название-фичи
```

### Посмотреть diff перед коммитом
```bash
git diff
git diff --staged
```

## 📊 Workflow Decision Tree

```
Что делаю?
│
├─ Новая фича → feature/* → dev
│
├─ Готов к тестированию → dev → stage
│
├─ Готов к продакшену → stage → prod
│
└─ Срочный фикс → hotfix/* → prod → backport
```

## ⚡ Горячие клавиши (GitHub)

- `t` - поиск файлов
- `b` - blame view
- `y` - получить permalink
- `.` - открыть в github.dev
- `g` + `i` - перейти к issues
- `g` + `p` - перейти к PRs

## 🎓 Best Practices

✅ **ДЕЛАТЬ:**
- Коммитить часто
- Писать понятные commit messages
- Тестировать перед push
- Заполнять PR templates
- Ждать CI/CD checks

❌ **НЕ ДЕЛАТЬ:**
- Пушить в protected branches
- Пропускать тесты
- Игнорировать code review
- Мерджить без аппрувов
- Коммитить секреты/токены

## 🔗 Полная документация

- [WORKFLOW.md](./WORKFLOW.md) - Детальное руководство
- [SETUP.md](./SETUP.md) - Настройка проекта
- [BRANCHING_STRATEGY.md](./BRANCHING_STRATEGY.md) - Стратегия веток

---

**Сохраните этот файл в закладки!** 🔖
