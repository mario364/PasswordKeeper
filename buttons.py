# Файл с кнопками программы
import flet as ft
from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from random import choices, choice, shuffle
from func import *
from pyperclip import copy
from controls import PasswordCopyLine


class GeneratePasswordButton(ft.UserControl):
    """
    Это класс кнопки "Сгенерировать пароль"
    """

    def __init__(self, choose: dict, name: ft.TextField, length: ft.TextField, password_place: ft.TextField):
        """

        :param choose: словарь на основе выбора пользователя символов
        :param name: название сайта, для которого пароль
        :param length: Введенная длина пароля
        """
        super().__init__()
        self.choose = choose
        self.length = length
        self.name = name
        self.user = None
        self.user_password = None
        self.password_place = password_place

    def build(self):
        """
        Это служебный метод библиотеки flet (читать документацию flet)
        :return: создает в окне приложения колонну с кнопкой
        """
        button = ft.ElevatedButton(text="Сгенерировать пароль", on_click=self.on_click, width=150)
        return ft.Column(controls=[button])

    def alert_error(self):
        """
        Метод создания диалога, при отсутствии выбора символов
        :return:
        """
        dlg = ft.AlertDialog(title=ft.Text("Невозможно создать пустой пароль"))

        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def on_click(self, e):
        """
        События происходящие при нажатии на кнопку
        :param e: служебный параметр, обязательный для запуска (читать документацию flet)
        :return:
        """
        # Проверяем выбрал ли пользователь хотя бы один набор символов
        if not any(self.choose.values()):
            # Если выбор не сделан, вызываем диалог ошибки
            self.alert_error()
            return
        # Иначе генерируем пароль
        self.generate_password()

    def generate_password(self):
        """
        Алгоритм генерации пароля, на основе введенной длины, выборе символов и названии сайта
        :return:
        """
        length = int(self.length.value)  # Длинна приходит в str. Поэтому обязательно делаем int
        symbols = ''  # Создаем строку, в которую будем класть нужные символы
        password = []  # Создаем список, в который кладем случайный символ из symbols
        kirill_up = ''.join(chr(i) for i in range(ord('А'), ord('Я') + 1))  # Кириллица в верхнем регистре
        kirill_low = ''.join(chr(i) for i in range(ord('а'), ord('я') + 1))  # Кириллица в нижнем регистре
        # Символьный словарь
        symbols_dict = {"kirill_low": kirill_low,
                        "kirill_up": kirill_up,
                        "latin_low": ascii_lowercase,
                        "latin_up": ascii_uppercase,
                        "digits": digits,
                        "special": punctuation}
        # Генерируем последовательность для пароля. Учитывая, чтобы из выбранных коллекций был хотя бы один символ
        for symbolsset in self.choose:
            if self.choose[symbolsset]:  # Проверяем выбрана ли последовательность символов
                password.append(choice(symbols_dict[symbolsset]))  # Добавляем случайный из последовательности.
                # Здесь и учитывается наличие хоть бы одного символа
                symbols += symbols_dict[symbolsset]  # Добавляем последовательность

        password.extend(choices(symbols, k=length - len(password)))  # Оставляем выбранные символы в случайном порядке
        # длинной self.length
        shuffle(password)  # Перемешиваем
        password = "".join(password)  # Делаем пароль строкой

        # self.save_password(password, self.name.value)
        #
        self.password_place.value = password
        self.password_place.update()

    # def save_password(self, password, name):
    #     data = read_toml_file()
    #     # print(Crypto.encrypt(password, self.user_password))
    #     data["passwords"][self.user][name] = Crypto.encrypt(password, self.user_password)
    #     write_toml_file(data)
    #     # print(data["passwords"][self.user][name])


class ShowPasswordButton(ft.UserControl):
    """
     Класс кнопки "Показать пароли"

    """

    def __init__(self):
        super().__init__()
        self.user = None
        self.user_password = None

    def build(self):
        """
        Служебный метод библиотеки flet (читать документацию flet)
        :return: создает в окне приложения колонну с кнопкой
        """
        button = ft.ElevatedButton(text="Показать пароли", on_click=self.on_click, width=450)
        return ft.Column(controls=[button])

    def on_click(self, e):
        """
        Событие, происходящие при нажатии на кнопку
        :param e: служебный параметр (читать документацию flet)
        :return:
        """
        # Проверяем, есть ли у пользователя пароли

        if not self.check_passwords():
            # Если нет - вызываем диалог с ошибкой
            dlg = ft.AlertDialog(title=ft.Text(value="У вас еще нет паролей"))
            self.page.dialog = dlg
            dlg.open = True
            self.page.update()
            # Иначе показываем пароли
        else:
            self.show_password()

    def show_password(self):
        """
        Метод показывающий окно с паролями и возможностью их скопировать
        :return:
        """
        contents = []  # Созадаем список, куда кладем пароли
        passwords = read_toml_file()['passwords'][self.user]

        for name, password in passwords.items():
            # Заполняем окно с паролями
            contents.append(PasswordCopyLine(ft.Text(value=f"{name} - {Crypto.decrypt(password, self.user_password)}")))

        # Создаем диалог
        dlg = ft.AlertDialog(title=ft.Text(value="Сохраненные пароли:"),
                             content=ft.Text(value="Посмотрите и скопируйте свои пароли"),
                             actions=[i for i in contents])
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def check_passwords(self):
        passwords = read_toml_file()["passwords"][self.user]
        if passwords:
            return True
        return False


class CopyButton(ft.UserControl):
    """
    То же самое, что прошлый класс, но только кнопка
    """

    def __init__(self, password):
        super().__init__()
        self.password = password

    def build(self):
        return ft.Row(
            controls=[ft.ElevatedButton(text="Скопировать!", icon=ft.icons.CONTENT_COPY, on_click=self.on_click)])

    def on_click(self, e):
        copy(self.password)


class SaveButton(ft.UserControl):
    def __init__(self, password_place: ft.TextField, name: ft.TextField):
        super().__init__()
        self.password_place = password_place
        self.name = name
        self.user = None
        self.user_password = None

    def build(self):
        button = ft.ElevatedButton(text="Сохранить", width=143, on_click=self.on_click)

        return ft.Column(controls=[button])

    def on_click(self, e):
        data = read_toml_file()
        encrypt_password = Crypto.encrypt(self.password_place.value, self.user_password)
        # print(encrypt_password)
        data["passwords"][self.user][self.name.value] = encrypt_password
        write_toml_file(data)

        self.dialog()

        self.password_place.value = ""
        self.password_place.update()

    def dialog(self):
        dlg = ft.AlertDialog(title=ft.Text("Пароль успешно сохранен!"),
                             content=ft.Text("Не желаете скопировать пароль?"),
                             actions=[PasswordCopyLine(ft.Text(f"{self.name.value} - {self.password_place.value}"))])
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()



class ShowParameters(ft.UserControl):

    def __init__(self, check_box):
        super().__init__()
        self.check_box = check_box

    def build(self):
        text = "Показать параметры"

        button = ft.ElevatedButton(text=text, on_click=self.on_click, width=480)

        return ft.Column(controls=[button])

    def on_click(self, e):
        button = e.control
        if not self.check_box.visible:
            self.check_box.visible = True
            button.text = "Скрыть параметры"
            self.check_box.update()
            button.update()
        else:
            self.check_box.visible = False
            button.text = "Показать параметры"
            self.check_box.update()
            button.update()
