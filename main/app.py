import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
import requests
from kivy_garden.graph import Graph, LinePlot

class KADAM(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        
        # Create a graph widget with ymin and ymax set to -99 and 99
        self.graph = Graph(
            xlabel='Time',
            ylabel='Random Number',
            x_ticks_minor=5,
            x_ticks_major=1,
            y_ticks_major=10,
            y_grid_label=True,
            x_grid_label=True,
            padding=5,
            x_grid=True,
            y_grid=True,
            xmin=0,
            xmax=20,
            ymin=-99,  # Set the minimum y-axis value to -99
            ymax=99    # Set the maximum y-axis value to 99
        )
        
        # Create a LinePlot instance
        self.plot = LinePlot(line_width=1.5, color=[1, 0, 0, 1])  # Red color plot
        self.plot.points = []
        self.graph.add_plot(self.plot)
        
        # Add the graph widget to the layout
        layout.add_widget(self.graph)
        
        # Integer input field with hint text
        self.message_input = TextInput(hint_text='Enter an integer', input_filter='int')
        
        send_button = Button(text='Send Integer')
        send_button.bind(on_press=self.send_message)
        
        layout.add_widget(self.message_input)
        layout.add_widget(send_button)
        
        # Initialize time counter
        self.time = 0
        
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
                
                # Update the plot with the new point
                if len(self.plot.points) > 20:  # Keep the last 20 points
                    self.plot.points.pop(0)
                
                # Append new point with time increment (self.time, random_number)
                self.plot.points.append((self.time, random_number))
                self.time += 1  # Increment the time for the next point
                
                # Adjust x-axis to move with new points after 20 points
                if self.time > 20:
                    self.graph.xmin = self.time - 20
                    self.graph.xmax = self.time

            else:
                print("Failed to retrieve data from ESP32")
                
        except Exception as e:
            print("Error updating plot:", e)

if __name__ == '__main__':
    KADAM().run()
