import json


class OfficeEquipment:
    def __init__(self, name, color, price):
        self.name = name
        self.color = color
        self.price = price

    def get_params(self):
        return {"название": self.name, "цвет": self.color, "цена": self.price}


class Equipment(OfficeEquipment):
    def __init__(self, name, color, price, special_characteristics):
        super().__init__(name, color, price)
        self.special_characteristics = special_characteristics

    def get_params(self):
        params = super().get_params()
        params["особые характеристики"] = self.special_characteristics
        return params


class Printer(OfficeEquipment):
    def __init__(self, name, color, price, is_color):
        super().__init__(name, color, price)
        self.is_color = is_color

    def get_params(self):
        params = super().get_params()
        params["цветной"] = "да" if self.is_color else "нет"
        return params


class Xerox(OfficeEquipment):
    def __init__(self, name, color, price, speed):
        super().__init__(name, color, price)
        self.speed = speed

    def get_params(self):
        params = super().get_params()
        params["скорость копирования"] = self.speed
        return params


class Scanner(OfficeEquipment):
    def __init__(self, name, color, price, resolution):
        super().__init__(name, color, price)
        self.resolution = resolution

    def get_params(self):
        params = super().get_params()
        params["разрешение"] = self.resolution
        return params


class Warehouse:
    def __init__(self):
        self.stock = {}
        self.departments = {}

    def add_item(self, item, department):
        if isinstance(item, OfficeEquipment):
            if department in self.departments:
                self.departments[department].append(item)
            else:
                choice = input(
                    f"Отдел '{department}' не существует. Если хотите создать новый отдел под названием '{department}' напишите 'да', а если хотите ввести другое название нажмите 'Enter': ")
                if choice.lower() == "да":
                    self.departments[department] = [item]
                else:
                    department = input("Введите название нового отдела: ")
                    self.departments[department] = [item]
            print(f"{item.name} добавлен на склад в отдел {department}")
        else:
            print(f"{item} не является техникой")

    def list_items(self):
        if not self.departments:
            print("Склад пуст")
        else:
            print("Список оборудования на складе:")
            for department, items in self.departments.items():
                print(f"Отдел: {department}")
                for i, item in enumerate(items):
                    print(f"{i}. {item.name}")
                    params = item.get_params()
                    for key, value in params.items():
                        print(f"{key}: {value}")
                    print()

    def move_item(self, item_number, source_department, destination_department):
        if source_department in self.departments and destination_department in self.departments:
            if item_number < len(self.departments[source_department]):
                item = self.departments[source_department].pop(item_number)
                self.departments[destination_department].append(item)
                print(f"{item.name} перемещен из отдела {source_department} в отдел {destination_department}")
            else:
                print("Неверный номер оборудования")
        else:
            print("Неверное название отдела")

    def serialize_item(self, item):
        if isinstance(item, Equipment):
            return {"название": item.name, "цвет": item.color, "цена": item.price,
                    "особые характеристики": item.special_characteristics}
        if isinstance(item, Printer):
            return {"название": item.name, "цвет": item.color, "цена": item.price,
                    "цветной": item.is_color}
        if isinstance(item, Xerox):
            return {"название": item.name, "цвет": item.color, "цена": item.price,
                    "скорость копирования": item.speed}
        if isinstance(item, Scanner):
            return {"название": item.name, "цвет": item.color, "цена": item.price,
                    "разрешение": item.resolution}
        return item

    def deserialize_item(self, item):
        if "особые характеристики" in item:
            return Equipment(item["название"], item["цвет"], item["цена"], item["особые характеристики"])
        if "цветной " in item:
            return Printer(item["название"], item["цвет"], item["цена"], item["цветной"])
        if "скорость копирования" in item:
            return Xerox(item["название"], item["цвет"], item["цена"], item["скорость копирования"])
        if "разрешение" in item:
            return Scanner(item["название"], item["цвет"], item["цена"], item["разрешение"])
        return item

    def save_to_file(self, filename):
        try:
            data = {"stock": self.stock, "departments": self.departments}
            with open(filename, "w") as file:
                json.dump(data, file, default=self.serialize_item, indent=4)
            print(f"Данные склада сохранены в файл {filename}")
        except FileExistsError as e:
            print(e)

    def load_from_file(self, filename):
        try:
            with open(filename, "r") as file:
                data = json.load(file, object_hook=self.deserialize_item)
                self.stock = data.get("stock", {})
                self.departments = data.get("departments", {})
            print(f"Данные склада загружены из файла {filename}")
        except FileNotFoundError:
            print(f"Файл {filename} не найден")

    def export_to_json(self, filename):
        try:
            data = {"stock": self.stock, "departments": self.departments}
            with open(filename, "w") as file:
                json.dump(data, file, default=self.serialize_item, indent=4)
            print(f"Данные склада сохранены в файл json {filename}")
        except FileExistsError as e:
            print(e)

    def import_from_json(self, filename):
        try:
            with open(filename, "r") as file:
                data = json.load(file, object_hook=self.deserialize_item)
                self.stock = data.get("stock", {})
                self.departments = data.get("departments", {})
            print(f"Данные склада загружены из файла json {filename}")
        except FileNotFoundError:
            print(f"Файл {filename} не найден")

    def sell_item(self, department, item_number):
        if department in self.departments:
            items = self.departments[department]
            if item_number < len(items):
                item = items.pop(item_number)
                print(f"Оборудование {item.name} продано из отдела {department}")
            else:
                print("Неверный порядковый номер оборудования")
        else:
            print("Отдел не найден")

    def clear_stock(self):
        self.stock = {}
        self.departments = {}
        print("Склад очищен")


def print_menu():
    print("Меню:")
    print("1. Посмотреть оборудование на складе")
    print("2. Добавить новое оборудование")
    print("3. Перенести оборудование")
    print("4. Загрузить из файла")
    print("5. Сохранить в файл список оборудования на складе")
    print("6. Экспорт в JSON оборудование на складе")
    print("7. Импорт из JSON")
    print("8. Продать оборудование")
    print("9. Очистить склад")
    print("0. Выход")


def main():
    warehouse = Warehouse()
    while True:
        print_menu()
        choice = input("Выберите действие: ")
        try:
            if choice == "1":
                warehouse.list_items()
            if choice == "2":
                choice_item = input(
                    "Напишите 1 для добавления принетра \nНапишите 2 для добавления ксерокса \nНапишите 3 для добавления сканера \nНапишите 4 для добавления иного типа оборудования \nВведите число: ")
                name = input("Введите название оборудования: ")
                color = input("Введите цвет оборудования: ")
                price = float(input("Введите цену оборудования: "))
                if choice_item == "1":
                    special_characteristics = input("Является ли принтер цветным 'да', 'нет': ")
                    department = input("Введите название отдела: ")
                    equipment = Printer(name, color, price, special_characteristics)
                    warehouse.add_item(equipment, department)
                elif choice_item == "2":
                    special_characteristics = input("скорость копирования: ")
                    department = input("Введите название отдела: ")
                    equipment = Xerox(name, color, price, special_characteristics)
                    warehouse.add_item(equipment, department)
                elif choice_item == "3":
                    special_characteristics = input("разрешение: ")
                    department = input("Введите название отдела: ")
                    equipment = Scanner(name, color, price, special_characteristics)
                    warehouse.add_item(equipment, department)
                elif choice_item == "4":
                    special_characteristics = input("Введите особые характеристики: ")
                    department = input("Введите название отдела: ")
                    equipment = Equipment(name, color, price, special_characteristics)
                    warehouse.add_item(equipment, department)
                else:
                    print("Ошибка! Попробуйте снова")
            elif choice == "3":
                warehouse.list_items()
                item_number = int(input("Введите номер оборудования: "))
                source_department = input("Введите название отдела, из которого перемещается оборудование: ")
                destination_department = input("Введите название отдела, в который перемещается оборудование: ")
                warehouse.move_item(item_number, source_department, destination_department)
            elif choice == "4":
                filename = input("Введите название файла: ")
                warehouse.load_from_file(filename)
            elif choice == "5":
                filename = input("Введите название файла: ")
                warehouse.save_to_file(filename)
            elif choice == "6":
                filename = input("Введите название файла: ")
                warehouse.export_to_json(filename)
            elif choice == "7":
                filename = input("Введите название файла: ")
                warehouse.import_from_json(filename)
            elif choice == "8":
                department = input("Введите название отдела: ")
                item_number = int(input("Введите порядковый номер оборудования: "))
                warehouse.sell_item(department, item_number)
            elif choice == "9":
                warehouse.clear_stock()
            elif choice == "0":
                break
            else:
                print("Неверный ввод, попробуйте снова")
        except ValueError:
            print("Ошибка! Попробуйте снова")


if __name__ == "__main__":
    main()
