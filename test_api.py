#!/usr/bin/env python3.12
import requests
import json
import time
import sys

BASE_URL = "http://localhost:8000"

def test_create_task():
    """Тест создания задачи"""
    print("\n" "1. Создание задачи")
    task_data = {
        "title": "Изучить Python 3.12",
        "description": "Освоить новые возможности Python 3.12",
        "priority": "high"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/tasks/", json=task_data)
        print(f"Статус: {response.status_code}")
        
        if response.status_code == 201:
            task = response.json()
            print(f"Задача создана:")
            print(f"   ID: {task['id']}")
            print(f"   Название: {task['title']}")
            print(f"   Приоритет: {task['priority']}")
            return task
        else:
            print(f"Ошибка: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        print(f"Ошибка: Не удалось подключиться к {BASE_URL}")
        print("   Убедитесь, что сервер запущен")
        return None

def test_get_all_tasks():
    """Тест получения всех задач"""
    print("\n 2. ПОЛУЧЕНИЕ ВСЕХ ЗАДАЧ")
    try:
        response = requests.get(f"{BASE_URL}/tasks/")
        print(f"Статус: {response.status_code}")
        
        tasks = response.json()
        print(f"Всего задач: {len(tasks)}")
        return tasks
    except requests.exceptions.ConnectionError:
        print(f"Ошибка подключения")
        return []

def test_health():
    """Тест проверки здоровья API"""
    print("\n Проверка здоровья API")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Статус: {response.status_code}")
        
        if response.status_code == 200:
            health = response.json()
            print(f"API работает:")
            print(f"   Статус: {health['status']}")
            print(f"   Python: {health['python_version']}")
            return True
    except:
        print(f"АPI не доступно")
        return False

def main():
    print_separator()
    print("ТЕСТИРОВАНИЕ TASK MANAGEMENT API")
    print_separator()
    
    # Сначала проверим здоровье API
    if not test_health():
        print("\n API не запущено. Запустите сервер:")
        print("   uvicorn app.main:app --reload")
        return
    
    # Создание задачи
    task = test_create_task()
    if task:
        time.sleep(1)
        
        # Получение всех задач
        test_get_all_tasks()
        
        time.sleep(1)
        
        # Проверка удаления
        print(f"\n Удаление задачи {task['id'][:8]}...")
        try:
            response = requests.delete(f"{BASE_URL}/tasks/{task['id']}")
            print(f"Статус: {response.status_code}")
        except:
            print(" Ошибка при удалении")
    
    print(" ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
   

if __name__ == "__main__":
    main()
