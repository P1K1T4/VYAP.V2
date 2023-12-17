from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.popup import Popup
import pandas as pd
import pickle

loaded_model = pickle.load(open('model.pkl', 'rb'))

Window.size = (1080, 720)


def on_dropdown_select(dropdown, text):
    print(f"Selected value: {text}")


def create_dropdown(values):
    dropdown = Spinner(
        values=values,
        size_hint=(None, None),
        size=(500, 40),
        pos_hint={"center_x": 0.5, "center_y": 0.5}
    )
    dropdown.bind(text=on_dropdown_select)
    return dropdown


def show_popup(message):
    popup = Popup(
        title="Ошибка",
        content=Label(text=message),
        size_hint=(None, None),
        size=(400, 200)
    )
    popup.open()


class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)

        self.cols = 2
        self.spacing = [10, 10]
        self.padding = [10, 10]

        self.fields = {
            'Этаж': None,  # Конкретный этаж
            'Кол-во этажей': None,  # Всего этажей
            'Кол-во комнат': None,  # Кол-во комнат
            'Площадь': None,  # Общая площадь
            'Площадь кухни': None,  # Площади кухни
            'Местоположение (Ширина)': None,  # Географическое положение(ширина)
            'Местоположение (Долгота)': None,  # Географическое положение(длина)
        }

        for field_name, _ in self.fields.items():
            self.add_widget(Label(text=field_name))
            self.fields[field_name] = TextInput(multiline=False)
            self.add_widget(self.fields[field_name])

        self.dropdown1 = create_dropdown(["0", "1", "2", "3"])
        self.add_widget(Label(text="Тип строения"))
        self.add_widget(self.dropdown1)

        self.dropdown2 = create_dropdown(["0", "1", "2"])
        self.add_widget(Label(text="Тип объекта"))
        self.add_widget(self.dropdown2)

        self.add_widget(Button(text="Рассчитать", on_release=self.calculate))

        self.result_label = Label(text="")
        self.add_widget(self.result_label)

    def on_textinput_enter(self, field_name, value):
        # Обработчик события при вводе значения в поле и нажатии Enter
        self.fields[field_name].text = value

    def calculate(self, instance):
        try:
            # Сбор данных из текстовых полей
            level = int(self.fields['Этаж'].text)
            levels = int(self.fields['Кол-во этажей'].text)
            rooms = int(self.fields['Кол-во комнат'].text)
            area = float(self.fields['Площадь'].text)
            kitchen_area = float(self.fields['Площадь кухни'].text)
            geo_lat = float(self.fields['Местоположение (Ширина)'].text)
            geo_lon = float(self.fields['Местоположение (Долгота)'].text)

            # Получение значения из выпадающих меню
            building_type = self.dropdown1.text
            object_type = self.dropdown2.text

            result = {
                'level': level,  # Конкретный этаж
                'levels': levels,  # Всего этажей
                'rooms': rooms,  # Кол-во комнат
                'area': area,  # Общая площадь
                'kitchen_area': kitchen_area,  # Площади кухни
                'geo_lat': geo_lat,  # Географическое положение(ширина)
                'geo_lon': geo_lon,  # Географическое положение(длина)
                'building_type': building_type,  # Тип строения
                'object_type': object_type,  # Какой-то тип объекта
            }

            random_flat_df = pd.DataFrame([result])

            predicted_price_base_model = loaded_model.predict(random_flat_df)[0]

            # Вывод результата
            self.result_label.text = f"Результат расчета: {predicted_price_base_model} рублей"
        except Exception as e:
            show_popup(str(e))


class RFMApp(App):
    def build(self):
        return MyGrid()


if __name__ == "__main__":
    RFMApp().run()
