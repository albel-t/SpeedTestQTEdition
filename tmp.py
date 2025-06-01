import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
import matplotlib
matplotlib.use('GTK3Agg')
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import test
import path

class GraphWindow(Gtk.Window):
    def __init__(self, input_text, selected_gadget):
        Gtk.Window.__init__(self, title="График скорости флешки")
        self.set_default_size(800, 600)
        self.selected_gadget = selected_gadget
        
        # Инициализация данных для графиков
        self.time_points = np.array([0])  # Ось времени (секунды)
        self.read_speeds = np.array([0])  # Скорости чтения
        self.write_speeds = np.array([0])  # Скорости записи
        
        # Основной контейнер
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)
        
        # Информационная панель
        self.info_label = Gtk.Label()
        self.update_info_label()
        vbox.pack_start(self.info_label, False, False, 0)
        
        # Создание графика
        self.fig = Figure(figsize=(8, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        # Инициализация линий графика
        self.line_read, = self.ax.plot(
            self.time_points, 
            self.read_speeds, 
            'b-', 
            linewidth=2, 
            label='Скорость чтения'
        )
        self.line_write, = self.ax.plot(
            self.time_points, 
            self.write_speeds, 
            'r-', 
            linewidth=2, 
            label='Скорость записи'
        )
        
        # Настройка графика
        self.ax.grid(True)
        self.ax.legend()
        self.ax.set_xlabel('Время (секунды)')
        self.ax.set_ylabel('Скорость (MB/s)')
        self.ax.set_title('Мониторинг скорости флешки')
        
        # Холст для графика
        self.canvas = FigureCanvas(self.fig)
        vbox.pack_start(self.canvas, True, True, 0)
        
        # Запуск периодического обновления
        self.timeout_id = GLib.timeout_add_seconds(3, self.update_lines_with_speed)
    
    def update_info_label(self):
        self.info_label.set_markup(
            f"<b>Пользователь:</b> {self.user_name}\n"
            f"<b>Устройство:</b> {self.selected_gadget}\n"
            f"<b>Измерений:</b> {len(self.time_points)-1}\n"
            f"<b>Последнее чтение:</b> {self.read_speeds[-1]:.2f} MB/s\n"
            f"<b>Последняя запись:</b> {self.write_speeds[-1]:.2f} MB/s"
        )
    
    def update_lines_with_speed(self):
        try:
            # Получаем новые данные скорости
            read_speed, write_speed = test.measure_flash_speed_generate(self.selected_gadget)
            
            # Обновляем данные
            new_time = self.time_points[-1] + 3
            self.time_points = np.append(self.time_points, new_time)
            self.read_speeds = np.append(self.read_speeds, read_speed)
            self.write_speeds = np.append(self.write_speeds, write_speed)
            
            # Обновляем график
            self.line_read.set_data(self.time_points, self.read_speeds)
            self.line_write.set_data(self.time_points, self.write_speeds)
            
            # Автомасштабирование
            self.ax.relim()
            self.ax.autoscale_view()
            self.canvas.draw()
            
            # Обновляем информацию
            self.update_info_label()
            
        except Exception as e:
            print(f"Ошибка при обновлении: {e}")
        
        # Возвращаем True для продолжения таймера
        return True

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Тестирование скорости флешки")
        self.set_default_size(400, 300)
        
        # Основной контейнер
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.vbox)
        
        # Поле ввода имени пользователя
        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Введите имя пользователя")
        self.vbox.pack_start(self.entry, False, False, 5)
        
        # Выпадающий список устройств
        self.combo = Gtk.ComboBoxText()
        self.vbox.pack_start(self.combo, False, False, 5)
        
        # Кнопка обновления списка устройств
        self.btn_refresh = Gtk.Button(label="Обновить список устройств")
        self.btn_refresh.connect("clicked", self.update_device_list)
        self.vbox.pack_start(self.btn_refresh, False, False, 5)
        
        # Кнопка запуска мониторинга
        self.btn_start = Gtk.Button(label="Начать мониторинг")
        self.btn_start.connect("clicked", self.start_monitoring)
        self.vbox.pack_start(self.btn_start, False, False, 10)
    
    def update_device_list(self, widget):
        # Очищаем список
        self.combo.remove_all()
        
        # Получаем имя пользователя
        user_name = self.entry.get_text().strip()
        if not user_name:
            self.show_warning("Введите имя пользователя")
            return
        
        # Получаем список устройств
        devices = path.find_flash_drive(user_name)
        if not devices:
            self.show_warning("Устройства не найдены")
            return
        
        # Заполняем выпадающий список
        for device in devices:
            self.combo.append_text(device)
        self.combo.set_active(0)
    
    def start_monitoring(self, widget):
        user_name = self.entry.get_text().strip()
        if not user_name:
            self.show_warning("Введите имя пользователя")
            return
        
        selected_device = self.combo.get_active_text()
        if not selected_device:
            self.show_warning("Выберите устройство")
            return
        
        # Создаем окно мониторинга
        monitor_win = GraphWindow(user_name, selected_device)
        monitor_win.show_all()
    
    def show_warning(self, message):
        dialog = Gtk.MessageDialog(
            parent=self,
            flags=0,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.OK,
            text=message
        )
        dialog.run()
        dialog.destroy()

if __name__ == "__main__":
    win = MainWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()