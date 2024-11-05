import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import requests

class ESP32App(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Only message input field and send button
        self.message_input = TextInput(hint_text='Message to send')
        
        send_button = Button(text='Send Message')
        send_button.bind(on_press=self.send_message)

        layout.add_widget(self.message_input)
        layout.add_widget(send_button)
        
        return layout

    # Move the send_message method inside the ESP32App class
    def send_message(self, instance):
        message = self.message_input.text
        url = "http://192.168.4.1/message"
        
        try:
            # Send the message with a Content-Type header
            headers = {'Content-Type': 'text/plain'}
            response = requests.post(url, data=message, headers=headers)
            
            print("Response from ESP32:", response.text)
        except Exception as e:
            print("Error:", e)

if __name__ == '__main__':
    ESP32App().run()
