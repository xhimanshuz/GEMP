import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
import subprocess

class ServiceIR(Gtk.Window):
    def __init__(self):
        # Gtk.Window.__init__(self):
        self.importObject()

    def importObject(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file('gui/serviceIR.glade')

        self.irWindow = self.builder.get_object('irWindow')
        self.irWindow.connect('delete-event',Gtk.main_quit)

        self.nginxInstallButton = self.builder.get_object('nginxInstallButton')
        self.phpInstallButton = self.builder.get_object('phpInstallButton')
        self.mysqlInstallButton = self.builder.get_object('mysqlInstallButton')

        self.nginxTick = self.builder.get_object('nginxTick')
        self.phpTick = self.builder.get_object('phpTick')
        self.mysqlTick = self.builder.get_object('mysqlTick')

        signal = {
            'nginxInstallButtonClicked' : self.nginxInstallButtonClicked,
            'phpInstallButtonClicked' : self.phpInstallButtonClicked,
            'mysqlInstallButtonClicked': self.mysqlInstallButtonClicked
        }
        self.builder.connect_signals(signal)

    def nginxInstallButtonClicked(self, widget):
        flag = subprocess.getstatusoutput('sudo apt install nginx -y')
        if flag[0]:
            print('Unalable to Install', flag)
            self.nginxTick.set_from_file('gui/cancel.png')
            
        else:
            print('Success Fully Install Nginx')
            self.nginxTick.set_from_file('gui/ok.png')

    def phpInstallButtonClicked(self, widget):
        flag = subprocess.getstatusoutput('sudo apt install php[5-9].[0-9]-fpm php[5-9].[0-9]-mysql  -y')
        if flag[0]:
            print("Error in Installing PHP")
            self.phpTick.set_from_file('gui/cancel.png')
        else:
            print('Successfully Install Php')
            self.phpTick.set_from_file('gui/ok.png')


    def mysqlInstallButtonClicked(self, widget):
        flag = subprocess.getstatusoutput('sudo apt install mysql-server mysql-client -y')
        if flag[0]:
            print('Error in Installing mysql')
            self.mysqlTick.set_from_file('gui/cancel.png')
        else:
            print('Successfully Install MySQL')
            self.mysqlTick.set_from_file('gui/ok.png')

    def run(self):
        self.irWindow.show_all()
            # Gtk.main()

# win = ServiceIR()
# win.run()
# Gtk.main()
