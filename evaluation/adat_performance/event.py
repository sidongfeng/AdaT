class Event():
    def __init__(self, adb, 
                       action=None, 
                       coord_1=None, 
                       coord_2=None, 
                       duration=None, 
                       commands=None, 
                       text=None):
        self.adb = adb

        self.action = action
        self.coord_1 = coord_1
        self.coord_2 = coord_2
        self.duration = duration
        self.commands = commands
        self.text = text
    
    def tap(self):
        string = f'input tap {str(self.coord_1[0])} {str(self.coord_1[1])}'.split(' ')
        self.adb.shell(string)
    
    def swipe(self):
        string = f'input swipe {str(self.coord_1[0])} {str(self.coord_1[1])} {str(self.coord_2[0])} {str(self.coord_2[1])} {str(self.duration)}'.split(' ')
        self.adb.shell(string)

    def intent(self):
        string = self.commands.replace('adb shell', '').split(' ')
        self.adb.shell(string)

    def input_text(self):
        string = f'input text "{str(self.text)}"'.split(' ')
        self.adb.shell(string)
    
    def double_tap(self):
        string = f'"input tap {str(self.coord_1[0])} {str(self.coord_1[1])}& sleep {str(self.duration)}; input tap {str(self.coord_1[0])} {str(self.coord_1[1])}"'.split(' ')
        self.adb.shell(string)

    def send_keyevent(self):
        string = f'input keyevent "{str(self.commands)}"'.split(' ')
        self.adb.shell(string)

    def before_launch(self):
        string = self.commands.replace('adb', '').split(' ')
        self.adb.run_cmd(string)