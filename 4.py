import os
import csv

class Entity:
    def __init__(self, entityType, value):
        setattr(self, 'entityType', entityType)
        setattr(self, 'value', value)

    def __str__(self):
        return 'Class name: ' + self.__class__.__name__ + '; Type: ' + self.entityType + '; Value: ' + self.value


class File(Entity):
    def __init__(self, value):
        setattr(self, 'entityType', 'File')
        setattr(self, 'value', value)


class Files:
    def __init__(self, dir_path):
        setattr(self, 'dir_path', dir_path)
        list_of_files = os.listdir(self.dir_path)
        files = []
        i = 0
        for filePath in list_of_files:
            files.append(File(filePath))

        setattr(self, 'files', files)
        setattr(self, 'n', 0)
        setattr(self, 'current', self.files[self.n])

        self.describe()
        
    def __iter__(self):
        return self

    def __next__(self):
        try:
            setattr(self, 'current', self.files[self.n])
        except IndexError:
            raise StopIteration
        
        setattr(self, 'n', self.n + 1)
        return self.current

    def __getitem__(self, item):
         return self.files[item]

    def generator(self, limit):
        i = 0
        while i < limit:
            yield self.files[i]
            i += 1

    def describe(self):
        for value in self.generator(len(self.files)):
            print(value)
    

class FileManager:
    def __init__(self, file_path):
        self.file_path = file_path

    @staticmethod
    def count_files(Files):
        print("Количество файлов в директории:", sum(1 for _ in Files))

    def read_data(self):
        with open(self.file_path, 'r') as file:
            reader = csv.DictReader(file)
            self.data_dict = {}

            i = 0
            for row in reader:
                self.data_dict[i] = row
                row['№'] = int(row['№'])
                i += 1
    
    def sort__by_gender(self):
        self.data_dict = dict(sorted(self.data_dict.items(), key=lambda x: x[1]['Пол']))

    def sort__by_number(self):
        self.data_dict = dict(sorted(self.data_dict.items(), key=lambda x: x[1]['№']))

    def filter_data(self):
        self.data_dict = {key: value for key, value in self.data_dict.items() if value.get('Пол') == 'M'}

    def print_data(self, text):
        print(text)
        for item in self.data_dict.items():
            print(item)
        print('\n')

    def add_record(self):
        with open(self.file_path, mode='a', newline='') as file_a:
            row = []
            print('Введите номер')
            row.append(input())
            print('Введите Дата и время')
            row.append(input())
            print('Введите Выход')
            row.append(input())
            print('Введите Пол')
            row.append(input())

            csv.writer(file_a).writerow(row)

        print('Новая строка успешно добавлена в CSV файл.')

    def ask(self):
        todo = int(input('Дальшейшие действия\n1 - добавить запись\n2 - Выход\n'))

        if todo == 1:
            self.add_record()
        elif todo == 2:
            exit()
        else:
            print('Выбрано неверное действие')
            exit()

files = Files("./folder/")
print(files[1])
FileManager.count_files(files)

file_manager = FileManager('data.csv')
file_manager.read_data()
file_manager.sort__by_gender()
file_manager.print_data('Сортировка по текстовому полю "Пол"')
file_manager.sort__by_number()
file_manager.print_data('Сортировка по числовому полю "Номер"')
file_manager.filter_data()
file_manager.print_data('Фильтр: только лица мужского пола')
file_manager.ask()
