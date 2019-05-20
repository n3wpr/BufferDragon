#!/usr/bin/python3
# -*- coding: UTF-8 -*-
try:
    from .color import Color
    import platform
    import sys
    import os
except ImportError as err:
    print("Error: ", str(err))

class Util:
    version = '0.1.Alpha'

    @staticmethod
    def checkIP(target):
        check = target.split('.', 4)
        for oct in check:
            if not oct.isnumeric():
                Color.pl("{G}I can't do this right if you don't refer a valid IPv4 address -.-'{W}")
                sys.exit()
            else:
                if not int(oct) <= 255:
                    Color.pl("{G}Should an IPv4 address has anything above 255?{W}")
                    #Color.pl("Really bro, that's not for your use. Bye script kiddie õ/{W}")
                    sys.exit()
        else:
            return target

    @staticmethod
    def getHelp():
        Color.pl('''
                      {P}Overflow some shitty apps like a fuck*ng dragon blowing fire{W}
            {RL}__                  __                {P}|
           {RL}( _)                {RL}( _)               {P}| {G}-h{W}, {G}--help{GR} ={C} help
          {RL}/ / \\               {RL}/ /\\_\\_             {P}|{Y} This pretty useful help message for script kiddies
         {RL}/ /   \\             {RL}/ / | \\ \\            {P}|{W} 
        {RL}/ /     \\           {RL}/ /  |\\ \\ \\           {P}| {G}-t{W}, {G}--target {GR}={C} Target
       {RL}/  /   {G},  {RL}\\{G} ,       {RL}/ /   /|  \\ \\          {P}|{Y} IP address of target application
      {RL}/  /    {G}|\\_ /|      {RL}/ /   / \\   \\_\\         {P}|{W} 
     {RL}/  /  {G}|\\/ _ '_|{RL}\\    {RL}/ /   /   \\    \\\        {P}| {G}-r{W}, {G}--reverse {GR}={C} Reverse IP
    {RL}|  /   {G}|/  {BL}0{D}{G} \\{BL}0{D}{G}\\{RL} \\  {RL}/ |    |    \\    \\\       {P}|{Y} Yourself address for reverse shell connection
    {RL}|  | {G}|\\|      \\_\\_ {RL}/  /    |     \\    \\\      {P}|{W} 
    {RL}|  | {G}|/    \\.\\ o\\o)  {RL}/      \\     |    \\\     {P}| {G}-p{W}, {G}--port {GR}={C} Porta
    {RL}\\  | {G}|     /\\\`v-v  {RL}/        |    |     \\\    {P}|{Y} Port to complet socket object
     {RL}| \\{G}/    /_| \\\_|  {RL}/         |    | \\    \\\   {P}|{W}  
     {RL}| {G}|    /__/_     {RL}/{G}   _____{RL}  |    |  \\    \\\  {P}|{G} -h {GR}={C} help
     {RL}\\{G}|    [__]  \_/  |_________  {RL}\   |   \\    () {P}|{Y} Something random to complete this screen :D
      {G}/    [___] (    \         \ {RL} |\ |   |   //  {P}|{W}
     {G}|    [___]                  |{RL}\| \|   /  |/   {P}| {G}-T{W}, {G}--turbo {GR}={C} Turbo mode
    {G}/|    [____]                  \  {RL}|/\ / / ||   {P}|{Y} Set turbo mode to: {G}enable{Y} (fast BoF)
   {G}(  \\   [____ /     ) _\      \  \    {RL}\| | ||   {P}|{W}
    {G}\\  \\  [_____|    / /     __/    \  {RL} / / //    {P}| {G}-a{W}, {G}--assistant {GR}={C} Assistant mode
    {G}|   \\ [_____/   / /        \    | {RL}  \/ //     {P}|{Y} Set assistant mode to: {G}enable{Y} (BoF step-by-step)
    {G}|   /  '----|   /=\____   _/    | {RL}  / //      {P}|===============================================
 {G}__ /  /        |  /   ___/  _/\    \ {RL} | ||       {P}| {Y}...::Developed by::...
{G}(/-(/-\\)       /   \  (/\/\)/  {G}|    /{RL}  | /        {P}| {+} {RL}n3wpr
              {G}(/\\/\\)           {G}/   /{RL}   //         {P}| {+} {RL}Th3_Pr0f3ss0r
                     {G}_________/   /    {RL}/          {P}| {Y}...::Version::...
                    {G}\\____________/{RL}    (           {P}|  %s
          {W}''' % str(Util.version))

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
    
    {C}Informe {Y}-h{C} para identificar os parametros aceitos.{W}\n''')

    @staticmethod
    def checkSys():
        if (platform.system().lower() == 'linux'):
            print("Estamos em casa, seguiremos adiante.")
        else:
            print('''Recomenda-se o uso de uma distribuição Linux
                  Já com o set de ferramentas instalados, sendo:
                  - Metasploit (Ou ao menos o msfvenom funcional);
                  - Algumas libs que já são nativas no kali
                  - Utilitarios de sistema para agilizar o funcionamento da tool''')