from samplebase import SampleBase
from rgbmatrix import graphics
import time
import socket
import subprocess
import sys

#import RPi.GPIO as gpio
#gpio.setmode(gpio.BCM)
#gpio.setup(6, gpio.OUT)
#gpio.output(6, gpio.HIGH)
#time.sleep(1)
#gpio.output(6, gpio.LOW)
#time.sleep(1)
#gpio.output(6, gpio.HIGH)
#time.sleep(1)
#gpio.output(6, gpio.LOW)


#TODO: create log file

class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.textColor = [graphics.Color(255,255,0),graphics.Color(255,0,0),graphics.Color(0,255,0),graphics.Color(25,25,255),graphics.Color(255,255,255)] # yellow,red,green,blue,white
        self.font = graphics.Font()
        self.font.LoadFont("/home/pi/mainBoard/fonts/mainBoardFonts/timeNumbersSeven.bdf")
        self.font2 = graphics.Font()
        self.font2.LoadFont("/home/pi/mainBoard/fonts/mainBoardFonts/colon.bdf")
        self.font1 = graphics.Font()
        self.font1.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/6x12.bdf")
        self.font3 = graphics.Font()
        self.font3.LoadFont("/home/pi/mainBoard/fonts/mainBoardFonts/timeNumbersColon.bdf")


    def run(self):
        cmd       = "hciconfig"
        device_id = "hci0"
        status, output = subprocess.getstatusoutput(cmd)
        bt_mac = output.split("{}:".format(device_id))[1].split("BD Address: ")[1].split(" ")[0].strip()
        hostMACAddress = bt_mac
        print(bt_mac)
        port    = 1
        backlog = 1
        size    = 1024
        s       = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        s.bind((hostMACAddress,port))
        s.listen(backlog)

        print("wait for bluetooth connection")
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        offscreen_canvas.Clear()
        graphics.DrawText(offscreen_canvas, self.font1, 2, 31, self.textColor[0], "wait for connection")
        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

        client, address = s.accept()
        print("bluetooth connected")

        player_blue = [{"X":194,"Y":8,"T":"1:","A":0},{"X":194,"Y":15,"T":"2:","A":0},{"X":194,"Y":23,"T":"3:","A":0},{"X":194,"Y":31,"T":"4:","A":0}
                      ,{"X":2,"Y":7,"T":"5:","A":0},{"X":2,"Y":15,"T":"6:","A":0},{"X":2,"Y":23,"T":"7:","A":0},{"X":2,"Y":31,"T":"8:","A":0}
                      ,{"X":221,"Y":8,"T":" 9:","A":0},{"X":221,"Y":15,"T":"10:","A":0},{"X":221,"Y":23,"T":"11:","A":0},{"X":221,"Y":31,"T":"12:","A":0}
                     ,{"X":29,"Y":7,"T":"13:","A":0}]

        player_white = [{"X":322,"Y":8,"T":"1:","A":0},{"X":322,"Y":15,"T":"2:","A":0},{"X":322,"Y":23,"T":"3:","A":0},{"X":322,"Y":31,"T":"4:","A":0}
                       ,{"X":130,"Y":7,"T":"5:","A":0},{"X":130,"Y":15,"T":"6:","A":0},{"X":130,"Y":23,"T":"7:","A":0},{"X":130,"Y":31,"T":"8:","A":0}
                       ,{"X":349,"Y":8,"T":" 9:","A":0},{"X":349,"Y":15,"T":"10:","A":0},{"X":349,"Y":23,"T":"11:","A":0},{"X":349,"Y":31,"T":"12:","A":0}
                       ,{"X":157,"Y":7,"T":"13:","A":0}]

        print("Draw!")
        textTimeGame    = "-:--"
        textColon       = ":"
        timeColor       = self.textColor[0]
        textResultBlue  = "--"
        textResultWhite = "--"
        textTeamBlue    = "---"
        textTeamWhite   = "---"
        textGameSection = "1"
        cool = True

        while True:
            if cool:
       	        offscreen_canvas.Clear()
                i=0
                for player in player_blue:
                    graphics.DrawText(offscreen_canvas, self.font1, player["X"], player["Y"], self.textColor[3] if player["A"]<3 else self.textColor[1], player["T"])
                    if player["A"] > 0:
                        graphics.DrawText(offscreen_canvas, self.font1, player["X"] + (10 if int(player["T"].strip(":"))<9 else 16), player["Y"], self.textColor[1], ("*" if player["A"]==1 else ("**" if player["A"]==2 else "***")))
                    i=i+1

                i=0
                for player in player_white:
                    graphics.DrawText(offscreen_canvas, self.font1, player["X"], player["Y"], self.textColor[4] if player["A"]<3 else self.textColor[1], player["T"])
                    if player["A"] > 0:
                        graphics.DrawText(offscreen_canvas, self.font1, player["X"]+ (10 if int(player["T"].strip(":"))<9 else 16), player["Y"], self.textColor[1], ("*" if player["A"]==1 else ("**" if player["A"]==2 else "***")))
                    i=i+1

                graphics.DrawText(offscreen_canvas, self.font , 262, 32, timeColor, textTimeGame.split(":")[0])
                graphics.DrawText(offscreen_canvas, self.font3 , 278, 32, timeColor, ":")
                graphics.DrawText(offscreen_canvas, self.font , 284, 32, timeColor, textTimeGame.split(":")[1])
#                graphics.DrawText(offscreen_canvas, font , 262, 31, timeColor, textTimeMin)
#                graphics.DrawText(offscreen_canvas, font2, 278, 25, timeColor, textColon)
#                graphics.DrawText(offscreen_canvas, font , 285, 31, timeColor, textTimeSec)
                graphics.DrawText(offscreen_canvas, self.font1, 278,  8, timeColor, textGameSection)

                if (textResultBlue != "--") and (int(textResultBlue) > 9):
                    xBlue  = 55
                    xColon = xBlue+32
                    xWhite = xColon+7
                else:
                    xBlue  = 70
                    xColon = xBlue+16
                    xWhite = xColon+7
                graphics.DrawText(offscreen_canvas, self.font , xBlue , 31, self.textColor[0], textResultBlue)
                graphics.DrawText(offscreen_canvas, self.font2, xColon, 25, self.textColor[0], textColon)
                graphics.DrawText(offscreen_canvas, self.font , xWhite, 31, self.textColor[0], textResultWhite)

                graphics.DrawText(offscreen_canvas, self.font1, 30,  29, self.textColor[0], textTeamBlue)
                graphics.DrawText(offscreen_canvas, self.font1, 162, 29, self.textColor[0], textTeamWhite)

                offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
                cool = False

            try:
                data = client.recv(size)
            except:
                print("lost connection.")
                offscreen_canvas.Clear()
                graphics.DrawText(offscreen_canvas, self.font1, 2, 31, self.textColor[0], "lost connection")
                offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
                s.close()
                time.sleep(1)
                s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
                s.bind((hostMACAddress,port))
                s.listen(backlog)
                print("Wait for reconnect")
                client, address = s.accept()

            if data:
                cool = True
                recText = str(data).split("'")[1].strip("'")
                print(recText)
                recText = recText.split("#")
                try:
                    for text in recText:
                        print("text: "+text)
                        tempText = text.split("%")
                        if tempText[0] == "timeGame":
                            textTimeGame = tempText[1]
                            if len(tempText)>2:
                                if tempText[2] == "default":
                                    timeColor = textColor[0]
                                elif tempText[2] == "red":
                                    timeColor = textColor[1]
                                elif tempText[2] == "green":
                                    timeColor = textColor[2]
                                elif tempText[2] == "blue":
                                    timeColor = textColor[3]
                                elif tempText[2] == "white":
                                    timeColor = textColor[4]
                                elif tempText[2] == "rgb":
                                    color =tempText[3].split[","]
                                    timeColor = graphics.Color(color[0],color[1],color[2])
                                print("timeColor: "+tempText[2])
                        elif tempText[0] == "result":
                            if len(tempText) > 1:
                                tempTextResult = tempText[1].split(":")
                                if tempTextResult[0].isdigit():
                                    textResultBlue = tempTextResult[0]
                                if len(tempTextResult) > 1 and tempTextResult[1].isdigit():
                                    textResultWhite = tempTextResult[1]
                                print("result: "+textResultBlue)
                                print("result: "+textResultWhite)
                        elif tempText[0] == "player":
                            if tempText[1].lower() == "blue":
                                player_blue[int(tempText[2])-1]["A"] = int(tempText[3])
                            else:
                                player_white[int(tempText[2])-1]["A"] = int(tempText[3])
                        elif tempText[0] == "brightness":
                            if len(tempText) > 1:
                                if tempText[1].isdigit():
                                    if int(tempText[1]) > 0 and int(tempText[1]) <= 100:
                                        print("brightness: "+tempText[1])
                                        try:
                                            self.matrix.brightness = int(tempText[1])
                                        except:
                                            print("could not set brightness")
                        elif tempText[0] == "teamBlue":
                            textTeamBlue = tempText[1]
                            print("yes blue")
                        elif tempText[0] == "teamWhite":
                            textTeamWhite = tempText[1]
                            print("yes white")
                        elif tempText[0] == "gameSection":
                            textGameSection = tempText[1]
                        elif tempText[0] == "exclusion1Blue":
                            textE1Blue = tempText[1]
                        elif tempText[0] == "exclusion2Blue":
                            textE2Blue = tempText[1]
                        elif tempText[0] == "exclusion1Blue":
                            textE1White = tempText[1]
                        elif tempText[0] == "exclusion2Blue":
                            textE2White = tempText[1]
                except:
                    print("could not process message")


if __name__=="__main__":
    print("Start shotclock")
    run_text = RunText()
    if (not run_text.process()):
            run_text.print_help()
