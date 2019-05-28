#!/usr/bin/python3
try:
    import getopt, sys, os.path
    import argparse
    from rsc.config import Util as config
    from rsc.color import Color as cor
    from bin.tools import Tools
except ImportError as err:
    print("Error: ", str(err))
    exit()

# Vars set
argv = sys.argv[1:]
#print('argv: ', argv)
target = ''
rport = ''
revIp = ''
lport = ''
assMode = False
turboMode = False

try:
    opts, args = getopt.getopt(argv, 't:r:hp:P:aTc', ['target=', 'reverse=', 'help', 'lport=', 'rport=', 'assistant', 'turbo'])
    # print('opts: ', opts)
except getopt.GetoptError as err:  # getopt.GetoptError as err:
    cor.pl("{G}Erro: {RL}"+str(err)+"{RL}")
    opts = []
    config.banner()
    sys.exit()
import time
# Tratativa padrão para a execução sem informar os devidos parametros
if len(opts) < 1:
    config.banner()
    config.dragonBanner(1)
    sys.exit()
else:
    # Parâmetros que possuem prioridade na execução ou que
    # desempenham tarefas simples e sem continuidade
    for opt, arg in opts:
        if opt == '-h':
            config.getHelp()
            sys.exit()
        elif opt == '-c':
            cor.pl("{G}Apps exploited by this tool{W}")
            Tools.checkApps()
            sys.exit()
    else:
        # Consulta os parametros passados e transfere os valores para variaveis
        for opt, arg in opts:
            if '-a' in opt or '--assistant' in opt:
                assMode = True
            elif opt == '-T' or '--turbo' in opt:
                turboMode = True
            elif opt == '-t' or opt == '--target=':
                target = str(arg[:15])
            elif opt == '-r' or opt == '--reverse=':
                revIp = str(arg[:15])
            elif opt == '-p' or opt == '--lport':
                lport = str(arg[:5])
            elif opt == '-P' or opt == '--rport=':
                rport = str(arg[:5])
        else:
            if target == '' or rport == '' or revIp == '' or lport == '':
                cor.pl("{C}Insert: {Y}target{C}, {Y}Rport{C}, {Y}revIP {C}AND {Y}Lport{C}. Try again.")
                config.banner()
                sys.exit()
            else:
                if assMode and turboMode:
                    cor.pl("{RL}Assistant mode{R} can't be set with {RL}turbo mode{R}. Please, choose {RL}JUST ONE.{W}")
                    sys.exit()
                elif assMode or turboMode:
                    target = config.checkIP(target)
                    rport = config.checkPort(rport)
                    if assMode:
                        Tools.assistantMode(target, rport, revIp,lport)
                    elif turboMode:
                        cor.pl("{G}turbo mode{Y} has been set.{W}")
                else:
                    cor.pl("{G}You need to do a choise, enter with {Y}-T{G} {BL}or{D} {Y}-a{G}.{W}")
                    sys.exit()

#bof = Tools.fuzzerBof('192.168.0.154', 21)