# QuickAppoint

### 1. Подготовка Docker контейнера с PostgreSQL
Выполните следующую команду для запуска PostgreSQL с указанными параметрами:

```bash
docker run --name fastapi-postgres \
  --env-file .env \
  -p 5432:5432 \
  -d postgres
```