
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
import requests
import matplotlib.pyplot as plt
from kivy_garden.matplotlib import FigureCanvasKivyAgg


class KADAM(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        
        # Initialize the graph plot
        self.fig, self.ax = plt.subplots()
        self.ax.set_title('ESP32 Data Plot')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Random Number')
        self.plot_data = []
        
        # Create a canvas for the graph and add it to the layout
        self.canvas = FigureCanvasKivyAgg(self.fig)
        layout.add_widget(self.canvas)
        
        # Integer input field with hint text
        self.message_input = TextInput(hint_text='Enter an integer', input_filter='int')
        
        send_button = Button(text='Send Integer')
        send_button.bind(on_press=self.send_message)
        
        layout.add_widget(self.message_input)
        layout.add_widget(send_button)
        
        # Schedule to update the plot every second
        Clock.schedule_interval(self.update_plot, 1)
        
        return layout

    def send_message(self, instance):
        try:
            # Convert input to an integer
            message = int(self.message_input.text)
            url = "http://192.168.4.1/message"  # Replace with ESP32 IP address
            
            # Send the integer as plain text
            headers = {'Content-Type': 'text/plain'}
            response = requests.post(url, data=str(message), headers=headers)
            
            print("Response from KADAM:", response.text)
        except ValueError:
            print("Please enter a valid integer.")
        except Exception as e:
            print("Error:", e)
    
    def update_plot(self, dt):
        try:
            # Request the random number from the ESP32
            url = "http://192.168.4.1/random"  # Endpoint for random number
            response = requests.get(url)
            if response.status_code == 200:
                random_number = int(response.text)  # Convert response to integer
                
                # Append the new number and trim the plot_data list to a max length
                self.plot_data.append(random_number)
                if len(self.plot_data) > 20:  # Keep the last 20 points
                    self.plot_data.pop(0)
                
                # Clear and update the plot
                self.ax.clear()
                self.ax.plot(self.plot_data, label="ESP32 Data")
                self.ax.legend(loc='upper left')
                self.canvas.draw()
            else:
                print("Failed to retrieve data from ESP32")
                
        except Exception as e:
            print("Error updating plot:", e)

if __name__ == '__main__':
    KADAM().run()
