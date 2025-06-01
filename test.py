import os
import time
from pathlib import Path

def clear_cache():
    try:
        print("Очистка кеша...")
        os.system("sudo sync")
        os.system("sudo sysctl vm.drop_caches=3")
        time.sleep(2) 
        print("очищено")

    except Exception as e:
        print(f"Ошибка при очистке кеша: {e}")

def measure_flash_speed(flash_path, file_size_mb = 5):
    
    flash_path = Path(flash_path)
    test_file = flash_path / "speed_test.tmp"
    block_size = 1024 * 1024

    try:
        # 1. Тест записи
        print("Измерение скорости записи...", )
        
        start_print_time = time.time() 
        for i in range(file_size_mb):
            pass
        print_time = time.time() - start_print_time # Счет и вывод вычитаются из скорости
        
        start_write = time.time()
        block = os.urandom(block_size)
        with open(test_file, 'wb', buffering=0) as f:
            for i in range(file_size_mb):
                f.write(block)
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
        
        print(f"write_speed({write_speed}); read_speed({read_speed})")

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
        #Pfrhsnbt
        if test_file.exists():
            test_file.unlink()
        os.sync()


def measure_flash_speed_generate(flash_path, file_size_mb = 5):
    print(f"flash_path {flash_path}; file_size_mb{file_size_mb}")
    print(f"Тестируем: {flash_path}")
    print("----------------------------------------")

        # Проверка прав
    if os.geteuid() != 0:
        print("\nОШИБКА: Скрипт требует root-прав для очистки кеша!")
        print("Запустите через sudo:")
        print("Запустите терминал (Ctrl+Alt+T) и вставьте команду:")
        print(f"sudo python3 {str(__file__)[0:-7]}"+"window.py")
        exit(1)
        
    try:
        results = measure_flash_speed(flash_path, 5)
        
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
    except Exception as e:
        print(f"\nКритическая ошибка: {str(e)}")
    finally:
        print("\nТестирование завершено")
    return [results["read_speed"], results["write_speed"]]





