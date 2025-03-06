## Тестирование

Для тестирования был реализован отдельный контейнер со всеми зависимостями для простоты использования.
Всё, что нужно сейчас - это запустить контейнер одной из нескольких команд.

```bash
cd ./solution
```
Обязательно перейти в папку `./solution` для запуска через docker-compose

### Все тесты одновременно
```bash
# Запустить тесты (с постфиксом [e2e, unit, all])
docker-compose run testing-service all
```

### e2e Tests
```bash
# Запустить тесты (с постфиксом [e2e, unit, all])
docker-compose run testing-service e2e
```

### Unit Tests
```bash
# Запустить тесты (с постфиксом [e2e, unit, all])
docker-compose run testing-service unit
```