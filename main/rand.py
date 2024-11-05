# import random
# import matplotlib.pyplot as plt
# from kivy.app import App
# from kivy.uix.boxlayout import BoxLayout
# from kivy.clock import Clock
# from kivy_garden.matplotlib import FigureCanvasKivyAgg

# class LivePlotApp(App):
#     def build(self):
#         # Main layout
#         layout = BoxLayout(orientation='vertical')

#         # Set up matplotlib figure and axis
#         self.fig, self.ax = plt.subplots()
#         self.line, = self.ax.plot([], [], lw=2)

#         # Set up plot properties
#         self.ax.set_xlim(0, 20)  # Display last 20 points
#         self.ax.set_ylim(0, 100)
#         self.ax.set_title("Live Random Number Plot")
#         self.ax.set_xlabel("Time")
#         self.ax.set_ylabel("Random Number")

#         # Add the matplotlib figure to the Kivy layout
#         self.canvas = FigureCanvasKivyAgg(self.fig)
#         layout.add_widget(self.canvas)

#         # Initialize data lists
#         self.x_data = []
#         self.y_data = []

#         # Schedule regular updates
#         Clock.schedule_interval(self.update_plot, 0.5)

#         return layout

#     def update_plot(self, dt):
#         # Generate a new random number
#         random_number = random.randint(0, 99)

#         # Update data lists
#         if len(self.x_data) >= 20:  # Keep only the last 20 points
#             self.x_data.pop(0)
#             self.y_data.pop(0)

#         self.x_data.append(len(self.x_data))
#         self.y_data.append(random_number)

#         # Update line data
#         self.line.set_data(self.x_data, self.y_data)

#         # Redraw plot
#         self.ax.relim()
#         self.ax.autoscale_view()
#         self.canvas.draw()

# if __name__ == "__main__":
#     LivePlotApp().run()




import random
import matplotlib.pyplot as plt
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy_garden.matplotlib import FigureCanvasKivyAgg

class LivePlotApp(App):
    def build(self):
        # Main layout
        layout = BoxLayout(orientation='vertical')

        # Set up matplotlib figure and axis
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], lw=2)

        # Set up plot properties
        self.ax.set_xlim(0, 20)  # Initial x-axis range for 20 points
        self.ax.set_ylim(0, 100)
        self.ax.set_title("Live Random Number Plot")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Random Number")

        # Add the matplotlib figure to the Kivy layout
        self.canvas = FigureCanvasKivyAgg(self.fig)
        layout.add_widget(self.canvas)

        # Initialize data lists and counter
        self.x_data = []
        self.y_data = []
        self.x_counter = 0  # To track time points

        # Schedule regular updates
        Clock.schedule_interval(self.update_plot, 0.5)

        return layout

    def update_plot(self, dt):
        # Generate a new random number
        random_number = random.randint(0, 99)

        # Update data lists
        self.x_data.append(self.x_counter)
        self.y_data.append(random_number)
        self.x_counter += 1  # Increment time counter

        # Keep only the last 20 points
        if len(self.x_data) > 20:
            self.x_data.pop(0)
            self.y_data.pop(0)

        # Update line data
        self.line.set_data(self.x_data, self.y_data)

        # Adjust x-axis limits to scroll with new data
        self.ax.set_xlim(self.x_counter - 20, self.x_counter)

        # Redraw plot
        self.canvas.draw()

if __name__ == "__main__":
    LivePlotApp().run()
