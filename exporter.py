import os
from dotenv import load_dotenv
import psutil
from http.server import HTTPServer, BaseHTTPRequestHandler

# Загрузка переменных окружения
load_dotenv()

EXPORTER_HOST = os.environ.get('EXPORTER_HOST', '0.0.0.0')
EXPORTER_PORT = int(os.environ.get('EXPORTER_PORT', '8081'))


def format_metrics(cpu_usage, cpu_per_core, memory_total, memory_used, disk_total, disk_used):
    """Формирование строки метрик для Prometheus."""
    core_metrics = "\n".join([
        f"# HELP cpu_core_usage CPU usage for core {i}\n"
        f"# TYPE cpu_core_usage gauge\n"
        f"cpu_core_usage{{core=\"{i}\"}} {usage}"
        for i, usage in enumerate(cpu_per_core)
    ])
    return f"""
{core_metrics}

# HELP cpu_usage CPU usage percentage
# TYPE cpu_usage gauge
cpu_usage {cpu_usage}

# HELP memory_total Total system memory in bytes
# TYPE memory_total gauge
memory_total {memory_total}

# HELP memory_used Used system memory in bytes
# TYPE memory_used gauge
memory_used {memory_used}

# HELP disk_total Total disk space in bytes
# TYPE disk_total gauge
disk_total {disk_total}

# HELP disk_used Used disk space in bytes
# TYPE disk_used gauge
disk_used {disk_used}
"""


class MetricsHandler(BaseHTTPRequestHandler):
    """HTTP обработчик для предоставления метрик."""

    def do_GET(self):
        # Обработка запроса на метрики
        if self.path == '/':
            # Сбор системных данных
            cpu_usage = psutil.cpu_percent()
            cpu_per_core = psutil.cpu_percent(percpu=True)
            mem_info = psutil.virtual_memory()
            disk_info = psutil.disk_usage('/')

            # Формирование метрик
            metrics = format_metrics(
                cpu_usage=cpu_usage,
                cpu_per_core=cpu_per_core,
                memory_total=mem_info.total,
                memory_used=mem_info.total - mem_info.available,
                disk_total=disk_info.total,
                disk_used=disk_info.used
            )

            # Отправка ответа
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; version=0.0.4')
            self.end_headers()
            self.wfile.write(metrics.encode('utf-8'))
        else:
            # Обработка 404
            self.send_response(404)
            self.end_headers()


if __name__ == '__main__':
    print(f"Starting exporter on {EXPORTER_HOST}:{EXPORTER_PORT}")
    server = HTTPServer((EXPORTER_HOST, EXPORTER_PORT), MetricsHandler)
    print(f"Exporter running on http://{EXPORTER_HOST}:{EXPORTER_PORT}/")
    server.serve_forever()