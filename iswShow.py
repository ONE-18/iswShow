import subprocess
from time import sleep
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

contraseña = ""
manual = False

class MenuApp(Gtk.Application):
    def __init__(self):
        global contraseña
        super(MenuApp, self).__init__(application_id="org.example.menuapp")
        self.window = None
        self.label = Gtk.Label()
        self.label.set_text("Texto Inicial")

    def do_activate(self):
        if not self.window:
            self.window = Gtk.ApplicationWindow(application=self)
            self.window.set_title("ISW")
            self.window.set_default_size(300, 100)
            self.window.set_resizable(False)
            
            grid = Gtk.Grid()
            grid.set_row_spacing(5)
            grid.set_column_spacing(5)
            grid.get_style_context().add_class(Gtk.STYLE_CLASS_VIEW)
            self.window.add(grid)

            button1 = Gtk.Button(label="boost on")
            button1.connect("clicked", self.on_command1_clicked)
            grid.attach(button1, 0, 0, 1, 1)

            button2 = Gtk.Button(label="boost off")
            button2.connect("clicked", self.on_command2_clicked)
            grid.attach(button2, 1, 0, 1, 1)

            self.label = Gtk.Label()
            self.label.set_hexpand(True)
            self.label.set_vexpand(True)
            self.label.set_xalign(0)
            self.label.set_yalign(0.5)
            grid.attach(self.label, 0, 1, 2, 1)
            
            self.checkbox = Gtk.CheckButton(label="Auto")
            self.checkbox.connect("toggled", self.set_manual)
            grid.attach(self.checkbox, 0, 2, 1, 1)
            
            self.entry1 = Gtk.Entry()
            grid.attach(self.entry1, 1, 1, 1, 1)
            self.entry2 = Gtk.Entry()
            grid.attach(self.entry2, 1, 2, 1, 1)

            GLib.timeout_add_seconds(1, self.update_output, None)
            
            self.window.show_all()

    def on_command1_clicked(self, widget):
        global contraseña
        comando = "echo " + contraseña + " | sudo -S isw -b on"
        resultado = subprocess.run(comando, shell=True, stdout=subprocess.PIPE, text=True)
        self.update_output(resultado.stdout)

    def on_command2_clicked(self, widget):
        global contraseña
        comando = "echo " + contraseña + " | sudo -S isw -b off"
        resultado = subprocess.run(comando, shell=True, stdout=subprocess.PIPE, text=True)
        self.update_output(resultado.stdout)
        
    def autoFunction(self,temperature):
        if(temperature > 60):
            self.on_command1_clicked(None)
        if(temperature < 35):
            self.on_command2_clicked(None)
    
    def get_cpu_temperature(self):
        global auto
        try:
            # Obtener la temperatura del CPU (este comando puede variar según tu sistema)
            result = subprocess.run(["cat", "/sys/class/thermal/thermal_zone0/temp"], stdout=subprocess.PIPE, text=True)
            temperature = float(result.stdout.strip()) / 1000  # Convertir a grados Celsius
            if auto:
                self.autoFunction(temperature)
            return f"CPU: {temperature:.1f}°C"
        except Exception as e:
            return f"Error when obtaining temperature: {str(e)}"
        
    def update_output(self, output):
        if output == None:
            output = self.get_cpu_temperature()
        self.label.set_text(output)
        return True
    
    def set_manual(self, button):
        global auto
        if button.get_active():
            auto = True
        else:
            auto = False
        
if __name__ == "__main__":
    app = MenuApp()
    app.run(None)
