from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import requests

class DescargadorApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Campo de entrada para URL
        self.url_input = TextInput(hint_text="Ingresa la URL del video", multiline=False)
        layout.add_widget(self.url_input)

        # Botón para iniciar descarga
        download_button = Button(text="Descargar")
        download_button.bind(on_press=self.descargar_video)
        layout.add_widget(download_button)

        return layout

    def descargar_video(self, instance):
        url = self.url_input.text
        if not url:
            instance.text = "Por favor, ingresa una URL válida"
            return

        # Llama al backend
        response = requests.post("http://127.0.0.1:5000/download", json={"url": url})
        if response.status_code == 200:
            instance.text = "Descarga completada"
        else:
            instance.text = "Error en la descarga"

if __name__ == "__main__":
    DescargadorApp().run()