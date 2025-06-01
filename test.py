import os
import time
import tempfile
from pathlib import Path
import ctypes
import shutil

def clear_cache():
    try:
        print("Очистка кеша...")
        # В Windows нет прямого аналога sync и drop_caches
        # Используем альтернативные методы очистки кеша
        ctypes.windll.kernel32.SetSystemFileCacheSize(-1, -1, 0)
        time.sleep(2)
        print("очищено")
    except Exception as e:
        print(f"Ошибка при очистке кеша: {e}")

def measure_flash_speed(flash_path, file_size_mb=5):
    flash_path = Path(flash_path)
    test_file = flash_path / "speed_test.tmp"
    block_size = 1024 * 1024  # 1MB

    try:
        # 1. Тест записи
        print("Измерение скорости записи...")
        
        start_print_time = time.time()
        for i in range(file_size_mb):
            pass
        print_time = time.time() - start_print_time
        
        start_write = time.time()
        block = os.urandom(block_size)
        with open(test_file, 'wb', buffering=0) as f:
            for i in range(file_size_mb):
                f.write(block)
            f.flush()
            os.fsync(f.fileno())
        stop_write = time.time()
        write_speed = file_size_mb / (stop_write - start_write - print_time)
        print("Успешно")

        # 2. Подготовка 
        clear_cache()
        
        # 3. Тест чтения
        print("Измерение скорости чтения...")
        start_read = time.time()
        with open(test_file, 'rb', buffering=0) as f:
            while f.read(block_size):
                pass
        read_speed = file_size_mb / (time.time() - start_read - print_time)
        print("Успешно")
        
        print(f"write_speed({write_speed:.2f} MB/s); read_speed({read_speed:.2f} MB/s)")

        return {
            'status': 'success',
            'write_speed': write_speed,
            'read_speed': read_speed
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e),
            'write_speed': 0,
            'read_speed': 0
        }
    finally:
        # Удаление тестового файла
        if test_file.exists():
            try:
                test_file.unlink()
            except:
                pass


def measure_flash_speed_generate(flash_path, file_size_mb=5):
    print(f"flash_path {flash_path}; file_size_mb {file_size_mb}")
    print(f"Тестируем: {flash_path}")
    print("----------------------------------------")
    
    results = {
        'status': 'error',
        'message': 'Неизвестная ошибка',
        'write_speed': 0,
        'read_speed': 0
    }
        
    try:
        # Проверка доступности диска
        if not Path(flash_path).exists():
            raise Exception("Указанный путь не существует")
            
        # Проверка свободного места
        total, used, free = shutil.disk_usage(flash_path)
        if free < file_size_mb * 1024 * 1024:
            raise Exception(f"Недостаточно свободного места. Требуется: {file_size_mb}MB")
            
        results = measure_flash_speed(flash_path, file_size_mb)
        
        if results['status'] == 'success':
            print("\nРезультаты:")
            print(f"Скорость записи: {results['write_speed']:.2f} MB/s")
            print(f"Скорость чтения: {results['read_speed']:.2f} MB/s")
            
            # Анализ результатов
            if results['read_speed'] > 500:
                print("\nВНИМАНИЕ: Нереальная скорость чтения!")
                print("Рекомендации:")
                print("1. Проверьте подключение флешки")
                print("2. Попробуйте другой USB-порт")
                print("3. Проверьте флешку на другом компьютере")
        else:
            print(f"\nОшибка: {results['message']}")
            
    except KeyboardInterrupt:
        print("\nТест прерван пользователем")
        results['message'] = "Тест прерван пользователем"
    except Exception as e:
        print(f"\nКритическая ошибка: {str(e)}")
        results['message'] = str(e)
    finally:
        print("\nТестирование завершено")
    
    return [results["read_speed"], results["write_speed"]]


