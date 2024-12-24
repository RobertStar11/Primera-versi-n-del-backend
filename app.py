from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import requests
from flask_cors import CORS



class DescargadorApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Campo de entrada para URL
        self.url_input = TextInput(hint_text="Ingresa la URL del video", multiline=False)
        layout.add_widget(self.url_input)

        # Botón para iniciar descarga
        self.download_button = Button(text="Descargar")
        self.download_button.bind(on_press=self.descargar_video)
        layout.add_widget(self.download_button)

        return layout

    def descargar_video(self, instance):
        url = self.url_input.text
        if not url:
            self.download_button.text = "Por favor, ingresa una URL válida"
            return

        # Llama al backend
        try:
            response = requests.post("http://35.160.120.126/download", json={"url": url})
            if response.status_code == 200:
                self.download_button.text = "Descarga completada"
            else:
                error_message = response.json().get("error", "Error en la descarga")
                self.download_button.text = f"Error: {error_message}"
        except Exception as e:
            self.download_button.text = f"Error de conexión: {str(e)}"

app = Flask(__name__)
CORS(app)  # Permite todas las conexiones de origen cruzado (CORS)

if __name__ == "__main__":
    DescargadorApp().run()