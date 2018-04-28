import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
import json
from os import path

class Setting(Gtk.Window):
    def __init__(self):
        self.importObject()
        self.builder.connect_signals(self.signals())
        self.setValues(self.settingJson(self.defaultSetting()))
        self.lists = self.fetchSetting()["ddclientList"]
        self.ddclientListInit(self.lists)


    def importObject(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("gui/setting.glade")
        self.settingWindow = self.builder.get_object("settingWindow")

        self.settingCancel = self.builder.get_object("settingCancel")
        self.settingOk = self.builder.get_object("settingOk")

        self.startWithGemp = self.builder.get_object("startWithGemp")
        self.stopWithGemp = self.builder.get_object("stopWithGemp")
        self.atStartup = self.builder.get_object("atStartup")

        self.nginxPortEntry = self.builder.get_object("nginxPortEntry")
        self.mysqlPortEntry = self.builder.get_object("mysqlPortEntry")
        self.setDefaultPortButton = self.builder.get_object("setDefaultPortButton")

        self.ngIndexEntry = self.builder.get_object("ngIndexEntry")
        self.ngTryFileEntry = self.builder.get_object("ngTryFileEntry")
        self.ngCustomEntry = self.builder.get_object("ngCustomEntry")
        self.gzipCompression = self.builder.get_object("gzipCompression")
        self.wptweak = self.builder.get_object("wptweak")
        self.nginxlogs = self.builder.get_object("nginxlogs")
        self.ngFileSetDefault = self.builder.get_object("ngFileSetDefault")

        self.mysqlPort = self.builder.get_object("mysqlPort")
        self.mysqlChangePassButton = self.builder.get_object("mysqlChangePassButton")
        self.adminerButton = self.builder.get_object("adminerButton")
        self.adminerButton.set_label("Adminer")
        self.mysqlLogEntry = self.builder.get_object("mysqlLogEntry")
        self.mysqlDefaultLogButton = self.builder.get_object("mysqlDefaultLogButton")
        
        self.phpMaxUploadLimit = self.builder.get_object("phpMaxUploadLimit")
        self.phpMaxNo = self.builder.get_object("phpMaxNo")
        
        self.ddProtocolEntry = self.builder.get_object("ddProtocolEntry")
        self.ddServiceEntry = self.builder.get_object("ddServiceEntry")
        self.ddlogin = self.builder.get_object("ddlogin")
        self.ddPassword = self.builder.get_object("ddlogin")
        self.ddclientClient = self.builder.get_object("ddclientClient")
        self.ddclientAdd = self.builder.get_object("ddclientAdd")
        self.ddclientRemove = self.builder.get_object("ddcleintRemove")
        self.ddclientTreeBox = self.builder.get_object("ddclientTreeBox")
        self.ddclientList = []
        
        self.treeView()

    def onSelect(self, selection):
        model, iter = selection.get_selected()
        if iter is not None:
            self.ddclientSeleted = model[iter][0]

    def treeView(self):
        self.listStore = Gtk.ListStore(str)
        self.ddclientTreeView = Gtk.TreeView(model=self.listStore)
        self.selection = self.ddclientTreeView.get_selection()
        self.selection.connect("changed", self.onSelect)
        self.ddclientTreeBox.add(self.ddclientTreeView)
        render = Gtk.CellRendererText()
        treeViewColumn = Gtk.TreeViewColumn('Client', render, text=0)
        self.ddclientTreeView.append_column(treeViewColumn)

    def ddclientAddClicked(self, widget):
        if self.ddclientClient.get_text() != "" and not (self.ddclientClient.get_text() in self.ddclientList):
            self.ddclientList.append(self.ddclientClient.get_text())
            self.listStore.append([self.ddclientClient.get_text()])
    
    def ddclientListInit(self, List):
        for list in List:
            print(list)
            self.listStore.append([list])
            

    def signals(self):
        signals = {
            "delete-event": (self.quit, True),
            "okButtonPressed":self.okButtonPressed,
            "cancelButtonPressed": (self.quit),
            "setDefaultPortButtonPressed": self.setDefaultPortButtonPressed,
            "mysqlDefaultLogButtonClicked": self.mysqlDefaultLogButtonClicked,
            "ngFileSetDefaultClicked": self.ngFileSetDefaultClicked,
            "ddclientAddClicked": self.ddclientAddClicked,
            "ddclientRemoveClicked": self.ddclientRemoveClicked
        }
        return signals

    def setValues(self,setting):
        self.startWithGemp.set_active(setting['startWithGemp'])
        self.stopWithGemp.set_active(setting["stopWithGemp"])
        self.atStartup.set_active(setting["atStartup"])

        self.nginxPortEntry.set_text(str(setting["nginxPortEntry"]))
        self.mysqlPortEntry.set_text(str(setting["mysqlPortEntry"]))

        self.ngIndexEntry.set_text(setting["ngIndexEntry"])
        self.ngTryFileEntry.set_text(setting["ngTryFileEntry"])
        self.ngCustomEntry.set_text(setting["ngCustomEntry"])
        self.wptweak.set_active(setting["wptweak"])
        self.gzipCompression.set_active(setting["gzipCompression"])
        self.nginxlogs.set_text(setting["nginxlogs"])

        self.mysqlPort.set_text(str(setting["mysqlPort"]))
        self.mysqlLogEntry.set_text(setting["mysqlLogEntry"])

        self.phpMaxUploadLimit.set_text(str(setting["phpMaxUploadLimit"]))
        self.phpMaxNo.set_text(str(setting["phpMaxNo"]))
        
        self.ddProtocolEntry.set_text(setting["ddProtocolEntry"])
        self.ddServiceEntry.set_text(setting["ddServiceEntry"])
        self.ddlogin.set_text(setting["ddlogin"])
        self.ddPassword.set_text(setting["ddPassword"])
        self.ddclientList = setting["ddclientList"]
        

    def defaultSetting(self):
        defaultSetting = {
            "startWithGemp":True,
            "stopWithGemp": False,
            "atStartup": False,

            "nginxPortEntry":80,
            "mysqlPortEntry":3306,

            "ngIndexEntry":"index.php index.htm index.html",
            "ngTryFileEntry": "$uri $uri/ =404",
            "ngCustomEntry":" ",
            "gzipCompression": True,
            "wptweak": True,
            "nginxlogs": "/etc/nginx/error_logs.txt",

            "mysqlPort": 3306,
            "mysqlLogEntry": "/var/log/mysql/error.log",

            "phpMaxUploadLimit":120,
            "phpMaxNo": 20,

            "ddProtocolEntry": " ",
            "ddServiceEntry": " ",
            "ddlogin": " ",
            "ddPassword": " ",
            "ddclientList": []
                   }
        return defaultSetting

    def fetchSetting(self):
            return {
            "startWithGemp": self.startWithGemp.get_active(),
            "stopWithGemp": self.stopWithGemp.get_active(),
            "atStartup": self.atStartup.get_active(),

            "nginxPortEntry": int(self.nginxPortEntry.get_text()),
            "mysqlPortEntry": int(self.mysqlPortEntry.get_text()),

            "ngIndexEntry": self.ngIndexEntry.get_text(),
            "ngTryFileEntry": self.ngTryFileEntry.get_text(),
            "ngCustomEntry": self.ngCustomEntry.get_text(),
            "gzipCompression": self.gzipCompression.get_active(),
            "wptweak": self.wptweak.get_active(),
            "nginxlogs": self.nginxlogs.get_text(),

            "mysqlPort": self.mysqlPort.get_text(),
            "mysqlLogEntry": self.mysqlLogEntry.get_text(),

            "phpMaxUploadLimit": int(self.phpMaxUploadLimit.get_text()),
            "phpMaxNo": int(self.phpMaxNo.get_text()),

            "ddProtocolEntry": self.ddProtocolEntry.get_text(),
            "ddServiceEntry": self.ddServiceEntry.get_text(),
            "ddlogin":self.ddlogin.get_text(),
            "ddPassword":self.ddPassword.get_text(),
            "ddclientList": self.ddclientList
            
            }

    def writeJson(self, string):
        print(string)
        with open("setting.json", "w") as file:
            s = json.dumps(string)
            file.write(s)
            print("Writing Setting Done")


    def settingJson(self, setting):
        print("Checking File...!")
        if (path.isfile("setting.json")):
            print("File Exists")
            with open("setting.json", "r") as file:
                setting = json.load(file)
        else:
            print("File Not Found, Creating a new one.")
            with open("setting.json","w+") as file:
                setting = json.dumps(setting)
                file.write(setting)
                setting = json.loads(setting)
        return setting

    def nginxConfig(self, setting):
        string = """
        #GEMP Server Nginx Configuration File
        server {{
            listen {};
            server_name _;
            root {};
            index {};
            location / {{
                try_files {};
            }}
            access_log {};
        }}
        """.format(int(setting['nginxPortEntry']), "/var/www/html/", setting["ngIndexEntry"], "$uri $uri/ =404", setting["nginxlogs"])
        with open("/etc/nginx/sites-enabled/GEMP.conf", "w") as file:
            file.write(string)

    def mysqlConfig(self, setting):
        with open('mysqld.cnf.sample','r') as f:
            s = f.read().replace('{port}',str(setting['mysqlPortEntry']))
            s = s.replace('{log}',str(setting['mysqlLogEntry']))
        with open('/etc/mysql/mysql.conf.d/mysqld.cnf','w') as f:
            f.write(s)

    def phpConfig(self, setting):
        with open('php.ini.sample','r') as f:
            s = f.read().replace("{maxFileSize}", str(setting["phpMaxUploadLimit"]))
            s = s.replace("{maxFileNo}", str(setting["phpMaxNo"]))
        with open("/etc/php/7.1/fpm/php.ini","w") as f:
            f.write(s)

    def ddclient(self, setting):
        string = """
# Configuration file for ddclient generated by GEMP
#
# /etc/ddclient.conf

deamon=3600
protocol={}
server={}
login={}
password={}
client={}
        """.format(setting["ddProtocolEntry"], setting["ddServiceEntry"], setting["ddlogin"], setting["ddPassword"], ','.join(setting["ddclientList"]))
        with open("config/ddclient.conf","w") as f:
            f.write(string)
            
    def ddclientRemoveClicked(self, widget):
        self.ddclientList.remove(self.ddclientSeleted)
        self.listStore.clear()
        self.ddclientListInit(self.lists)

    def okButtonPressed(self, widget):
        self.writeJson(self.fetchSetting())
        
        self.nginxConfig(self.fetchSetting())
        
        self.mysqlConfig(self.fetchSetting())

        self.phpConfig(self.fetchSetting())

        self.ddclient(self.fetchSetting())

        self.quit(True)
        print("OK")


    def setDefaultPortButtonPressed(self, widget):
        self.nginxPortEntry.set_text("80")
        self.mysqlPortEntry.set_text("3306")

    def mysqlDefaultLogButtonClicked(self, widget):
        self.mysqlLogEntry.set_text(self.defaultSetting()["mysqlLogEntry"])
        print(self.defaultSetting()["mysqlLogEntry"])
    
    def ngFileSetDefaultClicked(self, widget):
        self.ngIndexEntry.set_text(self.defaultSetting()["ngIndexEntry"])
        self.ngTryFileEntry.set_text(self.defaultSetting()["ngTryFileEntry"])
        self.ngCustomEntry.set_text(self.defaultSetting()["ngCustomEntry"])
        self.wptweak.set_active(self.defaultSetting()["wptweak"])
        self.gzipCompression.set_active(self.defaultSetting()["gzipCompression"])
        self.nginxlogs.set_text(self.defaultSetting()["nginxlogs"])

    def main(self):
        self.settingWindow.show_all()

    def quit(self, widget):
        self.settingWindow.close()
