import psutil
import wmi
import platform

def get_pc_info():
    try:
        c = wmi.WMI()
        system_info = {}

        # 1. Процессор
        system_info['Процессор'] = platform.processor()

        # 2. Оперативная память (Объем и Частота)
        memory = psutil.virtual_memory()
        system_info['ОЗУ (Всего)'] = f"{round(memory.total / (1024**3), 2)} GB"
        
        # Получаем частоту каждой плашки памяти
        sticks = c.Win32_PhysicalMemory()
        freqs = [f"{m.Speed} MHz" for m in sticks]
        system_info['ОЗУ (Частота)'] = ", ".join(freqs)

        # 3. Видеокарта
        gpus = c.Win32_VideoController()
        gpu_list = [gpu.Name for gpu in gpus]
        system_info['Видеокарта'] = ", ".join(gpu_list)

        # 4. Материнская плата
        boards = c.Win32_BaseBoard()
        if boards:
            board = boards[0]
            system_info['Материнская плата'] = f"{board.Manufacturer} {board.Product}"
        else:
            system_info['Материнская плата'] = "Не определена"

        return system_info
    except Exception as e:
        return {"Ошибка": str(e)}

if __name__ == "__main__":
    # Твоя фирменная подпись
    author = "by warpolska"
    
    print("=" * 40)
    print(f"{'СВЕДЕНИЯ О СИСТЕМЕ':^40}")
    print(f"{author:^40}")
    print("=" * 40)
    
    # Сбор данных
    info = get_pc_info()
    
    # Вывод данных в консоль
    for key, value in info.items():
        print(f"{key:<20}: {value}")
        
    print("=" * 40)
    
    # Важная строка, чтобы EXE не закрывался сам:
    print("\nРабота скрипта завершена.")
    input("Нажми Enter, чтобы выйти из программы...")
