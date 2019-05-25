#!/usr/bin/python3
# -*- coding: UTF-8 -*-
try:
    from .color import Color
    import platform
    import sys
    import os
    import select
    #from msvcrt import getch
    import getch
    import keyboard
except ImportError as err:
    print("Error: ", str(err))

class Util:
    version = '0.1.Alpha'

    @staticmethod
    def clearScr():
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
        except OSError as err:
            Color.pl("{G}Error: {RL}" + str(err))
            sys.exit()

    @staticmethod
    def checkIP(target):
        check = target.split('.', 4)
        if len(check) == 4:
            for oct in check:
                if not oct.isnumeric():
                    Color.pl("{G}I can't do this right if you don't input a valid IPv4 address -.-'{W}")
                    sys.exit()
                else:
                    if not int(oct) <= 255:
                        Color.pl("{G}Should an IPv4 address has anything above 255?{W}")
                        #Color.pl("Really bro, that's not for your use. Bye script kiddie õ/{W}")
                        sys.exit()
            else:
                return target
        else:
            Color.pl("{G}I can't do this right if you don't input a valid IPv4 address -.-'{W}")
            sys.exit()

    @staticmethod
    def checkPort(port):
        if (port.isnumeric() and (int(port) > 0 and int(port) < 65535)):
            return int(port)
        else:
            Color.pl("{G}I can't do this right if you don't refer a valid port -.-'{W}")
            Color.pl("{G}Really bro, that's not for your use. Bye {Y}script kiddie {G}õ/{W}")
            sys.exit()

    @staticmethod
    def dragonBanner(escolha):
        if escolha == 1:
            Color.pl('''
                      {P}Overflow some shitty apps like a fuck*ng dragon blowing fire{W}
            {RL}__                  __                {P}|{W}
           {RL}( _)                {RL}( _)               {P}| {G}-h{W}, {G}--help{GR} ={C} help
          {RL}/ / \\    Help - 1   {RL}/ /\\_\\_             {P}|{Y} This pretty useful help message for script kiddies
         {RL}/ /   \\             {RL}/ / | \\ \\            {P}|{W} 
        {RL}/ /     \\           {RL}/ /  |\\ \\ \\           {P}| {G}-t{W}, {G}--target {GR}={C} Target
       {RL}/  /   {G},  {RL}\\{G} ,       {RL}/ /   /|  \\ \\          {P}|{Y} IP address of target application
      {RL}/  /    {G}|\\_ /|      {RL}/ /   / \\   \\_\\         {P}|{W} 
     {RL}/  /  {G}|\\/ _ '_|{RL}\\    {RL}/ /   /   \\    \\\        {P}| {G}-r{W}, {G}--reverse {GR}={C} Reverse IP
    {RL}|  /   {G}|/  {BL}0{D}{G} \\{BL}0{D}{G}\\{RL} \\  {RL}/ |    |    \\    \\\       {P}|{Y} Yourself address for reverse shell connection
    {RL}|  | {G}|\\|      \\_\\_ {RL}/  /    |     \\    \\\      {P}|{W} 
    {RL}|  | {G}|/    \\.\\ o\\o)  {RL}/      \\     |    \\\     {P}| {G}-P{W}, {G}--rport {GR}={C} Remote port
    {RL}\\  | {G}|     /\\\`v-v  {RL}/        |    |     \\\    {P}|{Y} Port of application to connect and exploit
     {RL}| \\{G}/    /_| \\\_|  {RL}/         |    | \\    \\\   {P}|{W}  
     {RL}| {G}|    /__/_     {RL}/{G}   _____{RL}  |    |  \\    \\\  {P}| {G}-p{W}, {G}--lport {GR}={C} Local port
     {RL}\\{G}|    [__]  \_/  |_________  {RL}\   |   \\    () {P}| {G}YOUR{Y} port to receive the reverse connection
      {G}/    [___] (    \         \ {RL} |\ |   |   //  {P}|================================================={W}
     {G}|    [___]                  |{RL}\| \|   /  |/   {P}| {G}-T{W}, {G}--turbo {GR}={C} Turbo mode
    {G}/|    [____]                  \  {RL}|/\ / / ||   {P}|{Y} Set turbo mode to: {G}enable{Y} (fast BoF)
   {G}(  \\   [____ /     ) _\      \  \    {RL}\| | ||   {P}|{W}
    {G}\\  \\  [_____|    / /     __/    \  {RL} / / //    {P}| {G}-a{W}, {G}--assistant {GR}={C} Assistant mode
    {G}|   \\ [_____/   / /        \    | {RL}  \/ //     {P}|{Y} Set assistant mode to: {G}enable{Y} (BoF step-by-step)
    {G}|   /  '----|   /=\____   _/    | {RL}  / //      {P}|================================================={W}
 {G}__ /  /        |  /   ___/  _/\    \ {RL} | ||       {P}| {Y}...::Developed by::...     {P}| {W}
{G}(/-(/-\\)       /   \  (/\/\)/  {G}|    /{RL}  | /        {P}| {+} {RL}n3wpr                 {P}|    {G}Press {Y}'ESC'{W}
              {G}(/\\/\\)           {G}/   /{RL}   //         {P}| {+} {RL}Th3_Pr0f3ss0r         {P}|   {G}three times to{W}
                     {G}_________/   /    {RL}/          {P}| {Y}...::Version::...          {P}|  {G} exit help mode{W}
                    {G}\\____________/{RL}    (           {P}|  %s                 {P}| {W}
          {W}''' % str(Util.version))
        elif escolha == 2:
            Color.pl('''
                      {P}Overflow some shitty apps like a fuck*ng dragon blowing fire{W}
            {RL}__                  __                {P}|
           {RL}( _)                {RL}( _)               {P}| {G}-c{W}, {G}--check{GR} ={C} Check list
          {RL}/ / \\    Help - 2   {RL}/ /\\_\\_             {P}|{Y} Get a list of avaiable apps to exploit
         {RL}/ /   \\             {RL}/ / | \\ \\            {P}|{W} 
        {RL}/ /     \\           {RL}/ /  |\\ \\ \\           {P}| {G}-t{W}, {G}--target {GR}={C} Target
       {RL}/  /   {G},  {RL}\\{G} ,       {RL}/ /   /|  \\ \\          {P}|{Y} XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
      {RL}/  /    {G}|\\_ /|      {RL}/ /   / \\   \\_\\         {P}|{W} 
     {RL}/  /  {G}|\\/ _ '_|{RL}\\    {RL}/ /   /   \\    \\\        {P}| {G}-r{W}, {G}--reverse {GR}={C} Reverse IP
    {RL}|  /   {G}|/  {BL}0{D}{G} \\{BL}0{D}{G}\\{RL} \\  {RL}/ |    |    \\    \\\       {P}|{Y} XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    {RL}|  | {G}|\\|      \\_\\_ {RL}/  /    |     \\    \\\      {P}|{W} 
    {RL}|  | {G}|/    \\.\\ o\\o)  {RL}/      \\     |    \\\     {P}| {G}-P{W}, {G}--rport {GR}={C} Remote port
    {RL}\\  | {G}|     /\\\`v-v  {RL}/        |    |     \\\    {P}|{Y} XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
     {RL}| \\{G}/    /_| \\\_|  {RL}/         |    | \\    \\\   {P}|{W}  
     {RL}| {G}|    /__/_     {RL}/{G}   _____{RL}  |    |  \\    \\\  {P}| {G}-p{W}, {G}--lport {GR}={C} Local port
     {RL}\\{G}|    [__]  \_/  |_________  {RL}\   |   \\    () {P}| {Y}XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
      {G}/    [___] (    \         \ {RL} |\ |   |   //  {P}|{W}
     {G}|    [___]                  |{RL}\| \|   /  |/   {P}| {G}-T{W}, {G}--turbo {GR}={C} Turbo mode
    {G}/|    [____]                  \  {RL}|/\ / / ||   {P}|{Y} XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   {G}(  \\   [____ /     ) _\      \  \    {RL}\| | ||   {P}|{W}
    {G}\\  \\  [_____|    / /     __/    \  {RL} / / //    {P}| {G}-a{W}, {G}--assistant {GR}={C} Assistant mode
    {G}|   \\ [_____/   / /        \    | {RL}  \/ //     {P}|{Y} XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    {G}|   /  '----|   /=\____   _/    | {RL}  / //      {P}|=================================================
 {G}__ /  /        |  /   ___/  _/\    \ {RL} | ||       {P}| {Y}...::Developed by::...     {P}| {W}
{G}(/-(/-\\)       /   \  (/\/\)/  {G}|    /{RL}  | /        {P}| {+} {RL}n3wpr                 {P}|    {G}Press {Y}'ESC' {W}
              {G}(/\\/\\)           {G}/   /{RL}   //         {P}| {+} {RL}Th3_Pr0f3ss0r         {P}|   {G}three times to{W}
                     {G}_________/   /    {RL}/          {P}| {Y}...::Version::...          {P}|  {G} exit help mode{W}
                    {G}\\____________/{RL}    (           {P}|  %s                 {P}| {W}
          {W}''' % str(Util.version))

# Press 'ESC' three times to exit help mode
    @staticmethod
    def getHelp():
        Util.dragonBanner(1)
        '''try:
            if keyboard.is_pressed('left'):
                Util.dragonBanner(1)
            if keyboard.is_pressed('right'):
                Util.dragonBanner(2)
            if keyboard.is_pressed('Esc'):
                print("\nyou pressed Esc, so exiting...")
                sys.exit(0)
        except Exception as err:
            print(err)'''

        #char = ord(getch.getch())
        char = []
        try:
            while True:  # not char == 27:
                # char = ord(getch.getch())
                for x in range(3):
                    char.append(str(ord(getch.getch())))
                if char == ['27', '91', '67'] or char == ['27', '91', '66']:  # Right key pressed - (27 and 91 and 67):  # '\x1b[C': #str(27) in str(char):
                    Util.clearScr()
                    Util.dragonBanner(2)
                    char = []
                elif char == ['27', '91', '68'] or char == ['27', '91', '65']:  # Left key pressed - (27 and 91 and 68):  # '\x1b[D':
                    Util.clearScr()
                    Util.dragonBanner(1)
                    char = []
                else:
                    sys.exit()
        except OverflowError or KeyboardInterrupt as err:
            Color.pl("{G}Error: {RL}" + str(err))
            sys.exit()

    @staticmethod
    def banner():
        Color.pl('''
                        {Y}({W}                              
    {RL}   (        (      )\ )                           
    {Y} ( )\       )\ )  (()/(  (      ) (  (            
    {RL} )((_)   ( (()/(   /(_)) )(  ( /( )\))( (   (     
    {Y}((_)_    )\ /(_)) (_))_ (()\ )(_)|(_))\ )\  )\ )  
    {RL} | _ )  ((_|_) _|  |   \ ((_|(_)_ (()(_|(_)_(_/(  
     {O}| _ \_/ _ \|  _|  | |) | '_/ _` / _` / _ \ ' \)) 
     |___(_)___/|_|    |___/|_| \__,_\__, \___/_||_|  
                                     |___/{W}
    
        {C}Type {Y}-h{C} to view how this tool works fine.{W}\n''')

    @staticmethod
    def checkSys():
        check = os.name()
        if check == 'nt':
            print("Recomenda-se o uso de uma distribuição Linux")
            print("Já com o set de ferramentas instalados, sendo:")
            print("- Metasploit (Ou ao menos o msfvenom funcional);")
            print("- Algumas libs que já são nativas no kali")
            print("- Utilitarios de sistema para agilizar o funcionamento da tool")
            sys.exit()
        else:
            print("Estamos em casa, seguiremos adiante.")