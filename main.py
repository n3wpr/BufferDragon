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
revIp = ''
assMode = False
turboMode = False

try:
    opts, args = getopt.getopt(argv, 't:r:haT', ['target=', 'reverse=', 'help', 'assistant', 'turbo'])
    # print('opts: ', opts)
except getopt.GetoptError as err:  # getopt.GetoptError as err:
    cor.pl("{G}Erro: {RL}"+str(err)+"{RL}")
    opts = []
    config.banner()
    sys.exit()

if len(opts) < 1:
    config.banner()
    config.getHelp()
    sys.exit()
else:
    for opt, arg in opts:
        if '-h' in opt:
            config.getHelp()
            sys.exit()
    else:
        # Trata os parametros possíveis e transfere os argumentos para variaveis
        for opt, arg in opts:
            if '-a' in opt or '--assistant' in opt:
                assMode = True
            elif opt == '-T' or '--turbo' in opt:
                turboMode = True
            elif opts == '-t':
                target = str(arg)
            elif opts == '-r':
                revIp = str(arg)
        else:
            for opt, arg in opts:
                if assMode and turboMode:
                    cor.pl("{RL}Assistant mode can't be set with turbo mode. Please, choose just one.{W}")
                    sys.exit()
                elif assMode or turboMode:# or turboMode:
                    if assMode:
                        cor.pl("{G}Assistant mode{Y} has been set.{W}")
                        Tools.fuzzerBof(target, 21)
                    elif turboMode:
                        cor.pl("{G}turbo mode{Y} has been set.{W}")

                    break
                else:
                    cor.pl("{G}You need to do a choise, enter with {Y}-T{G} {BL}or{D} {Y}-a{G}.{W}")
                    sys.exit()


#print("Passou o loop e não encerrou a execução")
#bof = Tools.fuzzerBof('192.168.0.154', 21)