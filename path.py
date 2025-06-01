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
    disks = [drive for drive in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(drive + ":\\")]
    great_disks = []
    for disk in disks:
        if disk != "C":
            try:
                files_and_folders = os.listdir(disk + ":\\")
                if len(files_and_folders) > 0:
                    print(f"Найдена флешка на диске {disk}:")
                    for item in files_and_folders:
                        great_disks.append(item)
                        print(item)
                else:
                    print(f"Диск {disk} пуст.")
            except Exception as e:
                print(f"Ошибка при работе с диском {disk}: {e}")
    return great_disks
