import os

def find_flash_drive(user = "alexander_"):
    possible_locations = '/media/' + user
    print(possible_locations)
    flash_path = []
    if os.path.exists(possible_locations):
        for item in os.listdir(possible_locations):
            full_path = os.path.join(possible_locations, item)
            if os.path.ismount(full_path):
                print(f"Найдена флешка: {full_path}")
                flash_path.append(full_path)
    print(flash_path)
    return flash_path

def find_flash_drive_w(user = "alexander_"):
    possible_locations = '/media/' + user
    print(possible_locations)
    flash_path = []
    if os.path.exists(possible_locations):
        for item in os.listdir(possible_locations):
            full_path = os.path.join(possible_locations, item)
            if os.path.ismount(full_path):
                print(f"Найдена флешка: {full_path}")
                flash_path.append(full_path)
    print(flash_path)
    return flash_path
#flash_path = find_flash_drive()
