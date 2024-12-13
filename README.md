# Prometheus Exporter

## Описание
Это приложение-экспортёр на языке Python, которое собирает системные метрики (использование CPU, памяти и дисков) и предоставляет их в формате, совместимом с Prometheus. Экспортёр позволяет отслеживать состояние системы в реальном времени.

---

## Установка и запуск

### Требования
- Python 3.7 или выше
- Установленные библиотеки `psutil` и `python-dotenv`
- Prometheus и Grafana для сбора и визуализации метрик

### Установка
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/AnnaKob03/prometheus-exporter
   cd prometheus-exporter
   ```
2. Установите зависимости:
 ```bash
   pip install -r requirements.txt
   ```
3. Создайте файл .env в корне проекта и укажите переменные окружения:
   EXPORTER_HOST
   EXPORTER_PORT

### Запуск
1. Запустите экспортёр:
 ```bash
   python exporter.py
   ```
2. Приложение запустится на указанном хосте и порту (по умолчанию http://0.0.0.0:8081).

## Метрики
Экспортёр предоставляет следующие метрики:

### CPU
- cpu_usage: Общее использование процессора в процентах.
- cpu_core_usage{core="<номер ядра>"}: Использование каждого ядра процессора в процентах.

### Память
- memory_total: Общий объём оперативной памяти в байтах.
- memory_used: Используемая оперативная память в байтах.

### Диски
- disk_total: Общий объём дискового пространства в байтах.
- disk_used: Используемое дисковое пространство в байтах.

## Примеры запросов на PromQL

### Использование процессоров
- Общее использование CPU:
 ```promql
   cpu_usage
   ```
- Использование каждого ядра процессора:
 ```promql
   cpu_core_usage
   ```
### Память
- Общий объём оперативной памяти:
 ```promql
   memory_total
   ```
- Используемая оперативная память:
 ```promql
   memory_used
   ```
### Диски
- Общий объём дискового пространства:
 ```promql
   disk_total
   ```
- Используемое дисковое пространство:
 ```promql
   disk_used
   ```

## Интеграция с Prometheus
1. Добавьте экспортёр в файл конфигурации Prometheus (prometheus.yml):
 ```yaml
  scrape_configs:
  - job_name: "custom_exporter"
    metrics_path: "/"  # Укажите путь к метрикам
    static_configs:
      - targets: ["localhost:8081"]
   ```
2. Перезапустите Prometheus:
 ```bash
   ./prometheus --config.file=prometheus.yml
   ```
3. Проверьте статус в Prometheus:
 ```bash
   http://localhost:9090/targets
   ```