"""Pytest plugin для расчёта метрик покрытия API тестами."""
import json
import os
import re
from collections import defaultdict
from pathlib import Path


class APICoveragePlugin:
    """Плагин для сбора метрик покрытия API."""

    def __init__(self):
        self.endpoints_tested = defaultdict(lambda: {
            'methods': set(),
            'status_codes': set(),
            'assertions': 0,
            'tests_count': 0
        })
        self.total_assertions = 0
        self.spec_endpoints = {}

    def pytest_configure(self, config):
        """Инициализация плагина."""
        # Загружаем api_spec.json для подсчёта всех endpoints
        spec_path = Path(config.rootdir) / "api_spec.json"
        if spec_path.exists():
            with open(spec_path, 'r') as f:
                spec_data = json.load(f)
                self.spec_endpoints = self._parse_spec(spec_data)

    def _parse_spec(self, spec_data):
        """Парсинг api_spec.json для получения всех endpoints."""
        endpoints = {}
        if 'paths' in spec_data:
            for path, methods in spec_data['paths'].items():
                for method in methods.keys():
                    key = f"{method.upper()} {path}"
                    endpoints[key] = {'path': path, 'method': method.upper()}
        return endpoints

    def pytest_runtest_call(self, item):
        """Сбор информации о тесте во время выполнения."""
        # Извлекаем endpoint из имени теста или docstring
        endpoint = self._extract_endpoint(item)
        if endpoint:
            # Считаем assertions в тесте
            test_func = item.obj
            source = self._get_source_code(test_func)
            assertions_count = source.count('assert')
            
            self.endpoints_tested[endpoint]['assertions'] += assertions_count
            self.endpoints_tested[endpoint]['tests_count'] += 1
            self.total_assertions += assertions_count

    def pytest_runtest_makereport(self, item, call):
        """Сбор информации после выполнения теста."""
        if call.when == 'call':
            endpoint = self._extract_endpoint(item)
            if endpoint:
                # Извлекаем HTTP метод и статус код из теста
                method = self._extract_http_method(item)
                status_code = self._extract_status_code(item)
                
                if method:
                    self.endpoints_tested[endpoint]['methods'].add(method)
                if status_code:
                    self.endpoints_tested[endpoint]['status_codes'].add(status_code)

    def pytest_terminal_summary(self, terminalreporter, exitstatus, config):
        """Вывод отчёта в консоль после завершения тестов."""
        terminalreporter.write_sep("=", "API Coverage Report", cyan=True)
        
        # Подсчёт покрытия endpoints
        total_spec_endpoints = len(self.spec_endpoints) if self.spec_endpoints else 35  # default
        tested_endpoints = len(self.endpoints_tested)
        endpoint_coverage = (tested_endpoints / total_spec_endpoints * 100) if total_spec_endpoints > 0 else 0
        
        # Подсчёт покрытия HTTP методов
        all_methods = set()
        for data in self.endpoints_tested.values():
            all_methods.update(data['methods'])
        methods_coverage = (len(all_methods) / 4 * 100)  # GET, POST, PUT, DELETE
        
        # Подсчёт покрытия статус кодов
        all_status_codes = set()
        for data in self.endpoints_tested.values():
            all_status_codes.update(data['status_codes'])
        status_codes_coverage = (len(all_status_codes) / 5 * 100)  # 200, 400, 401, 404, 500
        
        # Вывод метрик
        terminalreporter.write_line(f"📊 Endpoints coverage: {endpoint_coverage:.1f}% ({tested_endpoints}/{total_spec_endpoints})")
        terminalreporter.write_line(f"🔧 HTTP methods coverage: {methods_coverage:.1f}% ({len(all_methods)}/4)")
        terminalreporter.write_line(f"📡 Status codes coverage: {status_codes_coverage:.1f}% ({len(all_status_codes)}/5)")
        terminalreporter.write_line(f"✅ Total assertions: {self.total_assertions}")
        terminalreporter.write_line("")
        
        # Детали по endpoints
        terminalreporter.write_line("📋 Tested Endpoints:")
        for endpoint, data in sorted(self.endpoints_tested.items()):
            methods_str = ', '.join(sorted(data['methods'])) if data['methods'] else 'N/A'
            status_str = ', '.join(str(s) for s in sorted(data['status_codes'])) if data['status_codes'] else 'N/A'
            terminalreporter.write_line(
                f"  • {endpoint}: {data['tests_count']} tests, {data['assertions']} asserts, "
                f"methods [{methods_str}], status [{status_str}]"
            )
        
        # Сохранение в JSON
        self._save_json_report(config.rootdir)

    def _save_json_report(self, rootdir):
        """Сохранение отчёта в JSON файл."""
        report_data = {
            'endpoints': {},
            'summary': {
                'total_endpoints_tested': len(self.endpoints_tested),
                'total_assertions': self.total_assertions,
                'http_methods_used': [],
                'status_codes_tested': []
            }
        }
        
        all_methods = set()
        all_status_codes = set()
        
        for endpoint, data in self.endpoints_tested.items():
            report_data['endpoints'][endpoint] = {
                'tests_count': data['tests_count'],
                'assertions': data['assertions'],
                'methods': list(data['methods']),
                'status_codes': list(data['status_codes'])
            }
            all_methods.update(data['methods'])
            all_status_codes.update(data['status_codes'])
        
        report_data['summary']['http_methods_used'] = sorted(all_methods)
        report_data['summary']['status_codes_tested'] = sorted(all_status_codes)
        
        reports_dir = Path(rootdir) / "reports"
        reports_dir.mkdir(exist_ok=True)
        
        report_file = reports_dir / "api_coverage.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)

    def _extract_endpoint(self, item):
        """Извлечение endpoint из теста."""
        # Пытаемся определить endpoint из пути к файлу
        test_path = str(item.fspath)
        
        # Извлекаем имя эндпоинта из пути (например, tests/endpoints/tasks/test_tasks_create.py -> tasks)
        match = re.search(r'endpoints/([^/]+)/', test_path)
        if match:
            endpoint_name = match.group(1)
            # Извлекаем метод из имени функции (например, test_create_task_success -> create)
            test_name = item.name
            if 'create' in test_name or 'add' in test_name:
                return f"/{endpoint_name}"
            elif 'update' in test_name or 'put' in test_name:
                return f"/{endpoint_name}"
            elif 'delete' in test_name:
                return f"/{endpoint_name}"
            elif 'get' in test_name or 'list' in test_name:
                return f"/{endpoint_name}"
            return f"/{endpoint_name}"
        return None

    def _extract_http_method(self, item):
        """Извлечение HTTP метода из теста."""
        test_name = item.name.lower()
        if 'create' in test_name or 'add' in test_name or '_post' in test_name:
            return 'POST'
        elif 'update' in test_name or '_put' in test_name:
            return 'PUT'
        elif 'delete' in test_name:
            return 'DELETE'
        elif 'get' in test_name or 'list' in test_name:
            return 'GET'
        return None

    def _extract_status_code(self, item):
        """Извлечение ожидаемого статус кода из теста."""
        # Анализируем исходный код теста для поиска assert_status_code
        test_func = item.obj
        source = self._get_source_code(test_func)
        
        # Ищем паттерны assert_status_code(response, XXX)
        status_matches = re.findall(r'assert_status_code\([^,]+,\s*(\d+)\)', source)
        if status_matches:
            return int(status_matches[0])
        
        # Ищем паттерны с 200, 400, 401, 404
        if '200' in source:
            return 200
        elif '401' in source:
            return 401
        elif '400' in source:
            return 400
        elif '404' in source:
            return 404
        return None

    def _get_source_code(self, func):
        """Получение исходного кода функции."""
        try:
            import inspect
            return inspect.getsource(func)
        except Exception:
            return ""


def pytest_configure(config):
    """Регистрация плагина в pytest."""
    config.pluginmanager.register(APICoveragePlugin(), "api_coverage")
