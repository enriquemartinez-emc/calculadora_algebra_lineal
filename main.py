from ttkbootstrap import Window
from ui.main_gui import LinearAlgebraCalculatorApp

if __name__ == "__main__":
    # Initialize ttkbootstrap Window
    app_window = Window(themename='solar')
    app_window.title("PySolve")
    app_window.state('zoomed')  # Maximize window

    # Create the main application GUI
    app = LinearAlgebraCalculatorApp(app_window)

    # Start the application
    app_window.mainloop()
