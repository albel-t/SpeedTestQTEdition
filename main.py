import os
import path
import test
import random


if __name__ == "__main__":
    path_flsh = path.find_flash_drive()
    print(path_flsh)
    print("\n==== Tестирование скорости флешки ====\n")
    for path_for_test in path_flsh:
        print(f"Тестируем: {path_for_test}")
        print("----------------------------------------")
        
        # Проверка прав
        if os.geteuid() != 0:
            print("\nОШИБКА: Скрипт требует root-прав для очистки кеша!")
            print("Запустите через sudo:")
            print("Запустите терминал (Ctrl+Alt+T) и вставьте команду:")
            print(f"sudo python3 {__file__}")
            exit(1)
        
        try:
            results = test.measure_flash_speed(path_for_test, 5)
            
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
            
            
            
            
            
