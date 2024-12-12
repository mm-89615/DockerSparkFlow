### Подготовка
Перед запуском проекта необходимо установить **[Poetry](https://python-poetry.org/docs/#installation)** 
и **[Make](https://www.gnu.org/software/make/)** для запуска Makefile'ов.

### Настройка .env 
Внесите нужные переменные окружения в файл `.env`, либо используйте `.env.docker`, предварительно переименовав.

Файл `.env` может содержать следующие переменные окружения для настройки Docker:
```dotenv
# Ports
POSTGRES_PORT # default: 6432 
AIRFLOW_WEB_PORT # default: 8080
SPARK_MASTER_WEBUI_PORT # default: 9090

# Limits
POSTGRES_CPU # default: 1
POSTGRES_MEMORY # default: 2GB
AIRFLOW_WEBSERVER_CPU # default: 1
AIRFLOW_WEBSERVER_MEMORY # default: 2G
AIRFLOW_SCHEDULER_CPU # default: 1
AIRFLOW_SCHEDULER_MEMORY # default: 2G
SPARK_MASTER_CORES # default: 1
SPARK_MASTER_MEMORY # default: 2G
SPARK_WORKER_CORES # default: 1
SPARK_WORKER_MEMORY # default: 2G

# PostgreSQL
POSTGRES_USER # default: airflow
POSTGRES_PASSWORD # default: airflow
POSTGRES_DB # default: airflow

# Airflow
AIRFLOW_LOAD_EXAMPLES # default: False
AIRFLOW_TEST_CONNECTION # default: Enabled
AIRFLOW_LOAD_DEFAULT_CONNECTIONS # default: False
AIRFLOW_LOGGING_LEVEL # default: INFO
AIRFLOW_EXPOSE_CONFIG # default: True
```
### Настройка Airflow connections
В файле по пути `docker/airflow/add_connections.py`находится скрипт для добавления 
соединений в Airflow при запуске контейнера.

При запуске добавляется `spark_conn` и `postgres_conn`. 

Можно удалить или добавить свои в переменную `connections`.

> `postgres_conn` подключается к тому же Postgres, что и Airflow, 
> только в другую базу данных (`postgres` вместо `airflow`).

### Возможности Makefile
Доступные в Makefile'е команды можно посмотреть с помощью команды `make help`:

```
Использование: make [Цель]

Доступные цели:
- requirements    Генерирует requirements.txt из pyproject.toml 
- build           Генерирует requirements.txt и затем собирает Docker образы
- up              Запускает окружение в фоне (docker-compose up -d)
- down            Останавливает и удаляет контейнеры (docker-compose down)
- restart         Перезапускает окружение
- rebuild         Перезапускает окружение с пересборкой образов
- logs            Показывает логи всех контейнеров
- submit          Выполняет spark-submit. Используйте job=путь_к_скрипту, например: make submit job=example_jobs.py
```
### Запуск Docker
Внутри контейнера зависимости устанавливаются из файла `requirements.txt`, который
генерируется автоматически при использовании команд Makefile.

Для установки необходимо выполнить команду:
```
make build
make up
```
### Доступные сервисы
Aiflow запускается по адресу: http://localhost:8080/

Spark UI запускается по адресу: http://localhost:9090/

### Использование Airflow и Spark
После запуска можно запускать DAG's с использованием `spark_conn` и `SparkSubmitOperator`.
Путь к скриптам DAG'ов находится в папке `jobs`. Например:
```python
spark_submit_task = SparkSubmitOperator(task_id='spark_submit_job',
    application='jobs/example_jobs.py',
    conn_id='spark_conn')
```

Также можно запускать Spark приложения на кластере без использования Airflow 
используя `make submit`с указанием пути к скрипту (в папке `jobs`). Например:
```
make submit job=example_jobs.py
```
### Установка пакетов и драйверов
Необходимые пакеты можно добавлять с помощью:
```
poetry add <package_name>
```
После добавления пакета необходимо выполнить команду:
```
make rebuild
```
Для установки драйверов для Spark, нужно указывать их в Dockerfile. Например:
```
RUN curl -o /opt/bitnami/spark/jars/postgresql-42.5.0.jar \
    https://repo1.maven.org/maven2/org/postgresql/postgresql/42.5.0/postgresql-42.5.0.jar
```
Если запускать скрипты в кластере Spark, то драйверы определяются автоматически.

Если запускать через Airflow, то нужно указывать пакеты в переменную 
`packages` или `conf` в `SparkSubmitOperator`. Например:
```python
spark_submit_task = SparkSubmitOperator(task_id='spark_submit_job',
    application='jobs/example_jobs.py',
    conn_id='spark_conn',
    packages='org.postgresql:postgresql:42.5.0')
```
