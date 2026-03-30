#!/usr/bin/env python3.12
import requests
import json
import time
import sys

BASE_URL = "http://localhost:8000"

def test_create_task():

    print("\n" "1. Создание задачи")
    task_data = {
        "title": "Понять смысл жизни",
        "description": "Смириться со смертью",
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
    print("Тестирование TASK MANAGEMENT API")
        
    if not test_health():
        print("\n API не запущено. Запустите сервер:")
        print("   uvicorn app.main:app --reload")
        return
    
    task = test_create_task()
    if task:
        time.sleep(1)
        
        test_get_all_tasks()
        
        time.sleep(1)
        
        print(f"\n Удаление задачи {task['id'][:8]}...")
        try:
            response = requests.delete(f"{BASE_URL}/tasks/{task['id']}")
            print(f"Статус: {response.status_code}")
        except:
            print(" Ошибка при удалении")
    
    print(" ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
   

if __name__ == "__main__":
    main()
