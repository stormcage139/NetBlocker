import sys, os
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHeaderView
from design_ui import Ui_MainWindow 
from PySide6.QtWidgets import QTableWidgetItem, QHeaderView, QFileIconProvider
from PySide6.QtCore import Qt, QFileInfo, QTimer
from main import check_block_status, get_all_processes, set_traffic_block, is_admin, get_all_blocked_rules




class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # Создаем экземпляр интерфейса
        self.ui = Ui_MainWindow()
        # Инициализируем его
        self.ui.setupUi(self)
        header = self.ui.processTable.horizontalHeader()

        # Колонки 0 (PID) и 1 (Имя) сжимаем по размеру текста
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)

 
        
        
        # Теперь все твои кнопки доступны через self.ui
        self.ui.ToggleButton.clicked.connect(self.handle_block)
        self.ui.ReloadButton.clicked.connect(self.handle_reload)
        self.processes = get_all_processes()
        self.fill_table(self.processes)
        self.blocked = set()
        
        print(self.processes,sep="\n")
        
    statuses = {} 
        
    def get_icon_from_exe(self, exe_path):
        if exe_path and os.path.exists(exe_path):
            file_info = QFileInfo(exe_path)
            icon_provider = QFileIconProvider()
            return icon_provider.icon(file_info)
        return QFileIconProvider().icon(QFileIconProvider.File) # Дефолтная иконка файла
        
    def handle_block(self):
        if not is_admin():
            print("Ошибка: Приложение запущено без прав администратора. Блокировка невозможна.")
            return
        
        row = self.ui.processTable.currentRow()
        if row >= 0:
            proc = self.processes[row]
            exe = proc['exe']
            rule_name = f"Block_{proc['name']}"
            currently_blocked = self.statuses.get(proc['exe'], False)
            print(f"Проверка статуса блокировки для {proc['name']}: {currently_blocked}")
            if currently_blocked:
                # Разблокировать
                success, message = set_traffic_block(exe, rule_name, block=False)
                action = "разблокирован"
            else:
                # Заблокировать
                success, message = set_traffic_block(exe, rule_name, block=True)
                action = "заблокирован"
            
            if success:
                print(f"Процесс {proc['name']} {action}")
                # Обновляем список заблокированных и таблицу
                # self.fill_table(self.processes)
                self.statuses[proc['exe']] = not currently_blocked  # Инвертируем статус
                self.fill_table(self.processes)
            else:
                print(f"Ошибка при {action[:-2]}ии процесса {proc['name']}: {message}")
        else:
            print("Кнопка Toggle нажата, но ни один процесс не выбран")
        
    def handle_reload(self):
        
        print("Перезагрузка данных...")
        self.ui.ReloadButton.setEnabled(False)
        self.processes = get_all_processes()
        self.fill_table(self.processes)
        row = self.ui.processTable.currentRow()
        if row >= 0:
            proc = self.processes[row]
            print(f"Кнопка Reload нажата и был выбран {proc['name']}")
        else:
            print("Кнопка Reload нажата, но ни один процесс не выбран")
        QTimer.singleShot(9, lambda: self.ui.ReloadButton.setEnabled(True))
        print(self.blocked)

    def fill_table(self, processes):
        # 1. Отключаем сортировку на время заполнения (чтобы данные не прыгали)
        self.ui.processTable.setSortingEnabled(False)
        
        # 2. Очищаем таблицу и задаем количество строк
        self.ui.processTable.setRowCount(len(processes))
        
        # 3. Получаем все заблокированные правила одним вызовом
        all_blocked = get_all_blocked_rules()
        icons = {}
        # 4. Заполняем ячейки
        for row, proc in enumerate(processes):
            # Создаем элементы для каждой колонки
            if proc['exe'] in icons:
                icon = icons[proc['exe']]
            else:
                icon = self.get_icon_from_exe(proc['exe'])
                icons[proc['exe']] = icon

            icon_item = QTableWidgetItem()
            icon_item.setIcon(icon)
            
            
            pid_item = QTableWidgetItem(str(proc['pid']))
            name_item = QTableWidgetItem(proc['name'])
            exe_item = QTableWidgetItem(proc['exe'])
            status_item = QTableWidgetItem()
            
            # Проверяем статус блокировки из общего списка правил
            rule_name = f"Block_{proc['name']}"
            blocked = rule_name in all_blocked
            self.statuses[proc['exe']] = blocked

            if blocked:
                status_item.setText("Заблокирован")
                status_item.setForeground(Qt.red) # Красный текст
            else:
                status_item.setText("Доступен")
                status_item.setForeground(Qt.green) # Зеленый текст

            # Можно сделать ячейки только для чтения
            pid_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            name_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            exe_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            status_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            
            # Вставляем в таблицу (строка, колонка, элемент)
            self.ui.processTable.setItem(row, 0, icon_item)
            self.ui.processTable.setItem(row, 1, pid_item)
            self.ui.processTable.setItem(row, 2, name_item)
            self.ui.processTable.setItem(row, 3, exe_item)
            self.ui.processTable.setItem(row, 4, status_item)
        # 4. Включаем сортировку обратно
        self.ui.processTable.setSortingEnabled(True)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())