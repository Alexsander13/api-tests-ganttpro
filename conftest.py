"""Конфигурация pytest для подключения плагина API Coverage и Allure."""
import pytest

# Импортируем и регистрируем плагины
pytest_plugins = [
    'tests.api_coverage_plugin',
    'tests.allure_autogen_plugin'
]


def pytest_configure(config):
    """Конфигурация pytest при запуске."""
    # Добавляем маркеры
    config.addinivalue_line(
        "markers", "api_endpoint(name): Mark test with API endpoint name"
    )
    config.addinivalue_line(
        "markers", "http_method(method): Mark test with HTTP method (GET, POST, PUT, DELETE)"
    )
    config.addinivalue_line(
        "markers", "status_code(code): Mark test with expected status code"
    )


def pytest_html_report_title(report):
    """Установка заголовка HTML отчёта."""
    report.title = "GanttPRO API Test Report"


def pytest_html_results_summary(prefix, summary, postfix):
    """Добавление секции с метриками API в HTML отчёт."""
    import json
    import os
    from pathlib import Path
    
    # Загружаем данные о покрытии API
    coverage_file = Path("reports/api_coverage.json")
    allure_index = Path("reports/allure-report/index.html")
    
    # Добавляем красивую секцию с ссылкой на Allure
    prefix.extend([
        "<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; margin: 20px 0; color: white;'>",
        "<h2 style='margin-top: 0; color: white;'>📊 Test Reports & Metrics</h2>",
        "<div style='display: flex; gap: 20px; margin-top: 15px;'>",
        "<div style='background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; flex: 1;'>",
        "<h3 style='margin-top: 0; color: white;'>📈 Allure Report</h3>",
    ])
    
    if allure_index.exists():
        # Относительный путь от report.html до allure-report/index.html
        prefix.append(
            "<p><a href='allure-report/index.html' target='_blank' style='color: #ffd700; font-weight: bold; font-size: 16px;'>"
            "🚀 Open Interactive Allure Report</a></p>"
            "<p style='font-size: 12px; opacity: 0.9;'>Detailed test execution with graphs, timelines, and history</p>"
        )
    else:
        prefix.append(
            "<p style='opacity: 0.7;'>⚠️ Allure report not generated</p>"
            "<p style='font-size: 12px;'>Run: <code>allure serve reports/allure-results</code></p>"
        )
    
    prefix.extend([
        "</div>",
        "<div style='background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; flex: 1;'>",
        "<h3 style='margin-top: 0; color: white;'>📁 JSON Reports</h3>",
        "<p><a href='api_coverage.json' target='_blank' style='color: #ffd700; font-weight: bold;'>API Coverage JSON</a></p>",
        "<p><a href='junit.xml' target='_blank' style='color: #ffd700; font-weight: bold;'>JUnit XML</a></p>",
        "</div>",
        "</div>",
        "</div>"
    ])
    
    if coverage_file.exists():
        with open(coverage_file, 'r', encoding='utf-8') as f:
            coverage_data = json.load(f)
        
        # Расчёт процентов покрытия
        total_api_endpoints = 35  # Общее количество эндпоинтов в GanttPRO API
        tested_endpoints = coverage_data['summary']['total_endpoints_tested']
        coverage_percent = (tested_endpoints / total_api_endpoints * 100) if total_api_endpoints > 0 else 0
        
        total_http_methods = 4  # GET, POST, PUT, DELETE
        tested_methods = len(coverage_data['summary']['http_methods_used'])
        methods_percent = (tested_methods / total_http_methods * 100) if total_http_methods > 0 else 0
        
        # Красивая таблица с метриками
        prefix.extend([
            "<div style='background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;'>",
            "<h2 style='color: #333; margin-top: 0;'>📊 API Coverage Metrics</h2>",
            
            # Большие карточки с процентами
            "<div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 20px;'>",
            
            # Endpoints Coverage
            "<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 8px; color: white; text-align: center;'>",
            f"<div style='font-size: 48px; font-weight: bold; margin-bottom: 10px;'>{coverage_percent:.1f}%</div>",
            f"<div style='font-size: 14px; opacity: 0.9;'>Endpoints Coverage</div>",
            f"<div style='font-size: 20px; margin-top: 10px; font-weight: bold;'>{tested_endpoints} / {total_api_endpoints}</div>",
            "</div>",
            
            # HTTP Methods Coverage
            "<div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 20px; border-radius: 8px; color: white; text-align: center;'>",
            f"<div style='font-size: 48px; font-weight: bold; margin-bottom: 10px;'>{methods_percent:.0f}%</div>",
            f"<div style='font-size: 14px; opacity: 0.9;'>HTTP Methods</div>",
            f"<div style='font-size: 20px; margin-top: 10px; font-weight: bold;'>{tested_methods} / {total_http_methods}</div>",
            "</div>",
            
            # Total Assertions
            "<div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 20px; border-radius: 8px; color: white; text-align: center;'>",
            f"<div style='font-size: 48px; font-weight: bold; margin-bottom: 10px;'>{coverage_data['summary']['total_assertions']}</div>",
            "<div style='font-size: 14px; opacity: 0.9;'>Total Assertions</div>",
            f"<div style='font-size: 16px; margin-top: 10px; opacity: 0.9;'>Across all tests</div>",
            "</div>",
            
            "</div>",
            
            # Детальная таблица
            "<table style='width: 100%; border-collapse: collapse; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>",
            "<thead style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;'>",
            "<tr><th style='padding: 15px; text-align: left;'>Metric</th><th style='padding: 15px; text-align: left;'>Value</th></tr>",
            "</thead>",
            "<tbody>",
            f"<tr style='border-bottom: 1px solid #e0e0e0;'><td style='padding: 12px;'><b>🎯 Endpoints Coverage</b></td><td style='padding: 12px; font-size: 16px; color: #667eea;'><b>{tested_endpoints}/{total_api_endpoints} ({coverage_percent:.1f}%)</b></td></tr>",
            f"<tr style='border-bottom: 1px solid #e0e0e0;'><td style='padding: 12px;'><b>🔧 HTTP Methods Coverage</b></td><td style='padding: 12px; font-size: 16px; color: #f5576c;'><b>{tested_methods}/{total_http_methods} ({methods_percent:.0f}%)</b> - {', '.join(sorted(coverage_data['summary']['http_methods_used']))}</td></tr>",
            f"<tr style='border-bottom: 1px solid #e0e0e0;'><td style='padding: 12px;'><b>✅ Total Assertions</b></td><td style='padding: 12px; font-size: 18px; color: #28a745;'><b>{coverage_data['summary']['total_assertions']}</b></td></tr>",
            f"<tr><td style='padding: 12px;'><b>📡 Status Codes Tested</b></td><td style='padding: 12px;'>{', '.join(map(str, sorted(coverage_data['summary']['status_codes_tested'])))}</td></tr>",
            "</tbody>",
            "</table>",
            "</div>",
            
            "<div style='background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;'>",
            "<h3 style='color: #333; margin-top: 0;'>📋 Endpoint Details</h3>",
            "<table style='width: 100%; border-collapse: collapse; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>",
            "<thead style='background: #667eea; color: white;'>",
            "<tr>",
            "<th style='padding: 12px; text-align: left;'>Endpoint</th>",
            "<th style='padding: 12px; text-align: center;'>Tests</th>",
            "<th style='padding: 12px; text-align: center;'>Assertions</th>",
            "<th style='padding: 12px; text-align: left;'>Methods</th>",
            "<th style='padding: 12px; text-align: left;'>Status Codes</th>",
            "</tr>",
            "</thead>",
            "<tbody>"
        ])
        
        for i, (endpoint, data) in enumerate(sorted(coverage_data['endpoints'].items())):
            methods_str = ', '.join(sorted(data['methods'])) if data['methods'] else 'N/A'
            status_str = ', '.join(map(str, sorted(data['status_codes']))) if data['status_codes'] else 'N/A'
            row_color = '#f9f9f9' if i % 2 == 0 else 'white'
            prefix.append(
                f"<tr style='background: {row_color}; border-bottom: 1px solid #e0e0e0;'>"
                f"<td style='padding: 10px; font-weight: bold; color: #667eea;'>{endpoint}</td>"
                f"<td style='padding: 10px; text-align: center;'>{data['tests_count']}</td>"
                f"<td style='padding: 10px; text-align: center;'>{data['assertions']}</td>"
                f"<td style='padding: 10px;'><span style='background: #e3f2fd; padding: 4px 8px; border-radius: 4px; font-size: 11px;'>{methods_str}</span></td>"
                f"<td style='padding: 10px;'><span style='background: #fff3e0; padding: 4px 8px; border-radius: 4px; font-size: 11px;'>{status_str}</span></td>"
                f"</tr>"
            )
        
        prefix.extend([
            "</tbody>",
            "</table>",
            "</div>"
        ])


# Поддержка Allure (опционально)
try:
    import allure
    
    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(item, call):
        """Добавление информации о request/response в Allure отчёт."""
        outcome = yield
        report = outcome.get_result()
        
        if report.when == 'call':
            # Добавляем информацию о тесте в Allure
            if hasattr(item, 'funcargs'):
                # Пытаемся получить информацию о последнем HTTP запросе
                if 'client' in item.funcargs:
                    client = item.funcargs['client']
                    if hasattr(client, 'last_response') and client.last_response:
                        # Добавляем request
                        request_info = f"Method: {client.last_response.request.method}\n"
                        request_info += f"URL: {client.last_response.request.url}\n"
                        if client.last_response.request.body:
                            request_info += f"Body: {client.last_response.request.body}\n"
                        allure.attach(request_info, name="HTTP Request", attachment_type=allure.attachment_type.TEXT)
                        
                        # Добавляем response
                        response_info = f"Status: {client.last_response.status_code}\n"
                        response_info += f"Body: {client.last_response.text}\n"
                        allure.attach(response_info, name="HTTP Response", attachment_type=allure.attachment_type.TEXT)

except ImportError:
    # Allure не установлен, пропускаем
    pass
