# "requirements" — генерирует requirements.txt из pyproject.toml группы 'Docker'
requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

# "build" — сначала генерирует requirements.txt, затем собирает Docker-образы
build: requirements
	docker-compose build

# "up" — поднимает окружение
up:
	docker-compose up -d

# "down" — останавливает окружение
down:
	docker-compose down

# "restart" — перезапускает окружение
restart: down up

# "rebuild" — перезапускает окружение с пересборкой образов
rebuild: down requirements
	docker-compose up -d --build

# "logs" — показывает логи
logs:
	docker-compose logs -f

# "submit" — выполняет spark-submit на spark-master
submit:
	docker exec -it $(shell docker ps --filter "name=spark-master" --format "{{.Names}}") spark-submit --master spark://spark-master:7077 --deploy-mode client /opt/bitnami/spark/jobs/$(job)

# Цель по умолчанию — помощь
help:
	@echo "Использование: make [Цель]"
	@echo "Доступные цели:"
	@echo "  requirements    Генерирует requirements.txt из pyproject.toml"
	@echo "  build           Генерирует requirements.txt и затем собирает Docker образы"
	@echo "  up              Запускает окружение в фоне (docker-compose up -d)"
	@echo "  down            Останавливает и удаляет контейнеры (docker-compose down)"
	@echo "  restart         Перезапускает окружение"
	@echo "  rebuild         Перезапускает окружение с пересборкой образов"
	@echo "  logs            Показывает логи всех контейнеров"
	@echo "  submit          Выполняет spark-submit. Используйте job=путь_к_скрипту, например: make submit job=example_jobs.py"
