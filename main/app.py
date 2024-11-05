import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import requests

class ESP32App(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Integer input field with hint text
        self.message_input = TextInput(hint_text='Enter an integer', input_filter='int')
        
        send_button = Button(text='Send Integer')
        send_button.bind(on_press=self.send_message)

        layout.add_widget(self.message_input)
        layout.add_widget(send_button)
        
        return layout

    def send_message(self, instance):
        try:
            # Convert input to an integer
            message = int(self.message_input.text)
            url = "http://192.168.4.1/message"
            
            # Send the integer as plain text
            headers = {'Content-Type': 'text/plain'}
            response = requests.post(url, data=str(message), headers=headers)
            
            print("Response from ESP32:", response.text)
        except ValueError:
            print("Please enter a valid integer.")
        except Exception as e:
            print("Error:", e)

if __name__ == '__main__':
    ESP32App().run()
