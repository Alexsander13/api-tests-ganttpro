"""Pytest хук для автоматической генерации Allure HTML отчёта после тестов."""
import subprocess
import sys
import os
import platform
from pathlib import Path


def pytest_sessionfinish(session, exitstatus):
    """Вызывается после завершения всех тестов."""
    # Проверяем, есть ли результаты Allure
    allure_results = Path(session.config.rootdir) / "reports" / "allure-results"
    
    if not allure_results.exists() or not list(allure_results.glob("*-result.json")):
        # Нет результатов Allure, пропускаем
        return
    
    # Генерируем HTML отчёт
    allure_report = Path(session.config.rootdir) / "reports" / "allure-report"
    
    try:
        print("\n" + "="*70)
        print("📊 Generating Allure HTML report...")
        print("="*70)
        
        # Set PATH explicitly to include Homebrew binaries
        env = os.environ.copy()
        env['PATH'] = f"/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:{env.get('PATH', '')}"
        
        # Команда генерации отчёта
        cmd = [
            "allure", "generate",
            str(allure_results),
            "-o", str(allure_report),
            "--clean"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, env=env)
        
        if result.returncode == 0:
            index_html = allure_report / "index.html"
            
            print(f"✅ Allure report generated successfully!")
            print(f"")
            print(f"📁 Агрегированный отчёт находится здесь:")
            print(f"   {allure_report}")
            print(f"")
            print(f"🌐 Открыть отчёт:")
            print(f"   open {index_html}")
            print(f"")
            print(f"💡 Или запустите интерактивный сервер:")
            print(f"   allure open {allure_report}")
            print(f"")
            
            # Автоматически открываем отчёт в браузере
            if platform.system() == "Darwin":  # macOS
                try:
                    subprocess.run(["open", str(index_html)], check=False)
                    print(f"✨ Отчёт открыт в браузере!")
                except Exception:
                    pass
            
        else:
            print(f"⚠️  Allure report generation failed: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("⚠️  Allure report generation timed out")
    except FileNotFoundError:
        print("⚠️  Allure command not found. Install it with: brew install allure")
    except Exception as e:
        print(f"⚠️  Error generating Allure report: {e}")
    
    print("="*70 + "\n")
