# Claude-templates

Шаблоны правил (`CLAUDE.md`, `REVIEW.md`) для проектов на Claude и скрипт, который устанавливает их в проект.

Стеки: **C#**, **Unity** (подтягивает C#), **Node.js**, **TypeScript**, **React** (подтягивает TypeScript).
Области: `backend-api`, `web-frontend`, `game`, `desktop-app`, `library-cli`.

## Использование

Нужен Python 3.9+ (только стандартная библиотека).

```bash
python setup.py                       # интерактивно
python setup.py --target ../MyGame --stacks unity --area game --extras all --forge both --yes
python setup.py --target . --stacks react,nodejs --dry-run
```

| Флаг | Значение |
|---|---|
| `--target` | папка проекта |
| `--stacks` | `csharp,unity,nodejs,typescript,react` |
| `--area` | одна область или `none` |
| `--extras` | `settings,pr,commitlint,editorconfig,gitignore` / `all` / `none` |
| `--forge` | `github`, `gitea`, `both` (папка для шаблона PR) |
| `--dry-run` | только показать изменения |
| `--yes` | без вопросов |
| `--force` | перезаписать уже существующие дополнительные файлы |

## Что записывается

- `CLAUDE.md`, `REVIEW.md`: правила помещаются между маркерами `claude-templates:begin/end`. Повторный запуск обновляет только этот блок, ваш текст сохраняется.
- `settings`: `.claude/settings.json` вливается в существующий (без соавторства и подписи Claude, запрет force-push и `reset --hard`).
- `pr`: `pull_request_template.md` в `.github/` и/или `.gitea/`.
- `commitlint`: для Node-стеков ставятся commitlint + husky, для остальных — обычные `.githooks/` (формат коммита, только заголовок, без соавторства, имя ветки).
- `editorconfig`, `gitignore`: под выбранные стеки (`gitignore` — блок между маркерами).

Скрипт не запускает `npm` и `git`, а выводит команды для ручного запуска.

## Как добавить стек

Создайте `templates/stacks/<имя>/CLAUDE.md` и `REVIEW.md`, добавьте имя в `STACKS` (и в `IMPLIES`, если нужно) в `setup.py`. Один фрагмент держите в пределах ~60 строк.

## Тесты

```bash
python -m unittest discover tests
```

## Скачивание (клонировать не нужно)

Возьмите `claude-templates.py` из [последнего релиза](../../releases/latest) и запустите `python claude-templates.py`. Это один файл со всеми встроенными шаблонами. Собрать его самому: `python build.py` (результат: `dist/claude-templates.py`); пуш тега `v*` публикует релиз автоматически.
