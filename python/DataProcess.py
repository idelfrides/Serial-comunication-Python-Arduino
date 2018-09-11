#!/usr/bin/python
# -*- coding: utf-8 -*-



import os
import time as t
import random as r
import json
import ModuloPyArduino as Mpa
import ModulePyCloudMongo as Mpcm


class DataProcess(object):
    mpao = Mpa.ModuloPyArduino()
    temperatura = -1
    tempoUser = 60  # o tempo eh dado em segundos: 60s = 1min

    def __init__(self):
        pass

    # mpao.appInfo()  # informacao da app

    # ---------------------------------------------------------------------------

    def validaTipoDado(self, d1, d2, d3):
        # d1 - valor temp | d2 - valor umid | d3 - valor umid solo
        if type(d1) != str and type(d2) != str and type(d3) != str:
            return 1  # leitura realizada com sucesso, dados numéricos
        else:
            return 0  # leitura realizada com falha

    # -----------------------------------------------------------------------------

    def serialLoopApp(self, condht, conumid, consoil, run):
        beforeState = 0    # estado anterior
        correntState = 0   # estado atual

        # creating object of DataProcess and ModulePyCloudMongo classes: dpo, mpcmo
        # dpo = Mdp.DataProcess()
        mpcmo = Mpcm.ModulePyCloudMongo()

        if run == 1:     # run = 1 (executar) | run = 0 (nao executar)

            # ------------------------------------------------------------
            #   Recuperando dados coletados pelo arduino
            # ------------------------------------------------------------
            datadht = self.mpao.get_data_arduino2py(condht)
            print "\n Arduino leu DHT11: ", datadht
            t.sleep(self.mpao.tempoEspera)
            dataumid = self.mpao.get_data_arduino2py(conumid)
            print "\n Arduino leu UMIDADE: ", dataumid
            t.sleep(self.mpao.tempoEspera)
            datasoil = self.mpao.get_data_arduino2py(consoil)
            print "\n Arduino leu SOIL: ", datasoil

            # verifica se os dados lidos são numéricos ou não
            checkData = self.validaTipoDado(datadht, dataumid, datasoil)

            # ------------------------------------------------------------------
            #  Verify and Management of the data obteined by arduino board
            # ------------------------------------------------------------------
            if checkData == 1:      # leitura bem sucedida
                datadht_verified = self.validate_sensor_data('temperatura', datadht)
                dataumid_verified = self.validate_sensor_data('umidade', dataumid)
                datasoil_verified = self.validate_sensor_data('umidade solo', datasoil)

                if datadht_verified != 'indefinido' and dataumid_verified != 'indefinido':

                    # ---------------------------------------------------------
                    # format json data files:
                    # 1 - numerical received data | 2 - virified data
                    # ---------------------------------------------------------
                    self.formataArquivo(datadht, dataumid, datasoil, 1)  # 1: dados numericos
                    self.formataArquivo(datadht_verified, dataumid_verified, datasoil_verified, 2)  # 2

                    # Recupera o estado atual da plantação por meio dos parâmetros -
                    # temperatura, umidade e umidade do solo
                    correntState = self.define_disease(datadht_verified, dataumid_verified, datasoil_verified)

                    if correntState != beforeState:
                        # update | change | state number
                        self.formataArquivoControle(1, 1, correntState)
                        beforeState = correntState
                        print("correntState =/= beforeState:  ", beforeState)
                    else:
                        self.formataArquivoControle(1, 0, beforeState)

                    # -------------------------------------------------------------
                    #   Call a method to send data to cloud mongoDB DB
                    # -------------------------------------------------------------
                    # opening a conection with a remote cloud mongo server
                    uri, port = mpcmo.configCloudMongoSC()

                    # insert data into collection dataNumSensores
                    mpcmo.handleCloudMongoData(uri, port, 'dataNumSensores.json', 1)

                    # insert data into collection dataNumSensores
                    mpcmo.handleCloudMongoData(uri, port, 'dataVerificSensores.json', 2)

                    # insert data into collection dataNumSensores
                    mpcmo.handleCloudMongoData(uri, port, 'controle.json', 3)

                    # Check and get the response time seted by user through web application
                    mpcmo.handleCloudMongoData(uri, port, 'controle.json', 4)

                    # verifica a compatibilidade dos tempos
                    if self.tempoUser != self.tempoPadrao:
                        self.tempoPadrao = self.tempoUser

                    # closing the conection with remote cloud mongo server
                    mpcmo.closeCMConection()
                else:
                    print('\n\n One or more values of parameter are invalid!!!\n\n')
            else:
                print("\n\n Falha de leitura do SENSOR DHT11 e/ou SOIL MISURE\n\n")
        else:
            print("\n\n RUN is zero \n\n")


    def validate_sensor_data(self, param, valor):
        refval_dht = 30     # referência, média de temperatura relativa
        refval_umi = 30     # referência, média de umidade relativa
        # refval_soil = 20  # referência, média de umidade solo

        if param == "temperatura":
            if valor > refval_dht:
                estado_param = "HIGH"
                return estado_param
            elif valor < refval_dht:
                estado_param = "LOW"
                return estado_param
            else:
                estado_param = "indefinido"
                return estado_param
        elif param == "umidade":
            if valor > refval_umi:
                estado_param = "HIGH"
                return estado_param
            elif valor < refval_umi:
                estado_param = "LOW"
                return estado_param
            else:
                estado_param = "indefinido"
                return estado_param
        elif param == "umidade solo":
            if valor <= 399:
                estado_param = "WET"  # molhado
                return estado_param
            elif valor >= 400 and valor <= 699:
                estado_param = "MOIST"  # umido
                return estado_param
            else:
                estado_param = "MODERATE"  # seco
                return estado_param
        else:
            print("\n\n WARNNING: The parameter given is not valid.\n\n The stage of this parameter can't be definided!!!")
            return 0


    def formataArquivo(self, d1, d2, d3, collec):
        d = json.dumps({'temperatura': d1, 'umidade': d2, 'umidade solo': d3}, sort_keys=True, indent=4, separators=(',', ':'))
        self.createColectionDataSensor(d, collec)


    def createColectionDataSensor(self, data, cod):
        if cod == 1:  # numeric data
            try:
                f = open('datanumsensor.json', 'w')
                f.write(data)
                f.close()
            except IOError:
                print("\n\n I/O Error: Can not open file datanumsensor.json")
                print "\n\n The application will be quited!!!\n\n\n"
                exit(0)
        elif cod == 2:  # dados em caracteres
            try:
                f = open('datacaracsensor.json', 'w')
                f.write(data)
                f.close()
            except IOError:
                print("\n\n I/O Error: Can not open file datacaracsensor.json")
                print "\n\n The application will be quited!!!\n\n\n"
                exit(0)


    def formataArquivoControle(self, update, change, sno):
        dj = json.dumps({'Update': update, 'Change': change, 'SNO': sno}, sort_keys=True, indent=4, separators=(',', ':'))
        self.createColectionControle(dj)


    def createColectionControle(self, data):
        try:
            f = open('controle.json', 'w')
            f.write(data)
            f.close()
        except IOError:
            print("\n\n I/O Error: Can not open file controle.json")
            print "\n\n The application will be quited!!!\n\n\n"
            exit(0)


    # *****************************************************************************

    # @staticmethod
    def define_disease(self, t, h, s):
        """ define a disease under the atributes (the parameters of method)
            t = temperatue, h = humidity, s = soil moisture
        """

        if t == "HIGH" and h == "HIGH" and s == "WET":
            return 1
            # self.show_disease(1)
        elif t == "LOW" and h == "HIGH" and s == "WET":
            return 2
            # self.show_disease(2)
        elif t == "LOW" and h == "HIGH" and s == "MODERATE":
            return 3
            # self.show_disease(3)
        elif t == "LOW" and h == "HIGH" and s == "WET":
            return 4
            # self.show_disease(4)
        elif t == "LOW" and h == "HIGH" and s == "MOIST":
            return 5
            # self.show_disease(5)
        elif t == "LOW" and h == "HIGH" and s == "MOIST":
            return 6
            # self.show_disease(6)
        elif t == "HIGH" and h == "HIGH" and s == "MOIST":
            return 7
            # self.show_disease(7)
        else:
            print("\n\n Combinação de parâmetros invalida. \n Aplicação será encerrada!!\n\n")
            return 0

    def define_disease_table_data(self, t, h, s):
        """ define a disease under the atributes
            t = temperatue, h = humidity, s = soil moisture
        """
        aux1 = r.randint(1, 2)
        aux2 = r.randint(5, 6)

        if t == 1 and h == 1 and s == 2:
            self.show_disease(1)
        elif t == 0 and h == 1 and s == 2 and aux1 == 1:
            self.show_disease(2)
        elif t == 0 and h == 1 and s == 3:
            self.show_disease(3)
        elif t == 0 and h == 1 and s == 2 and aux1 == 2:
            self.show_disease(4)
        elif t == 0 and h == 1 and s == 4 and aux2 == 5:
            self.show_disease(5)
        elif t == 0 and h == 1 and s == 4 and aux2 == 6:
            self.show_disease(6)
        elif t == 1 and h == 1 and s == 4:
            self.show_disease(7)
        else:
            print("\n\n Combinação de parâmetros invalida. \n Aplicação será encerrada!!\n\n")
            return 0

    # @staticmethod
    def show_disease(self, sno):
        """ print a disease corresponding the combination of atributes.
            there are 7 possibilities in this application
        """

        if sno == 1:
            print("\n\n DISEASE: XXXX - 1\n")
        elif sno == 2:
            print("\n\n DISEASE: XXXX - 2\n")
        elif sno == 3:
            print("\n\n DISEASE: XXXX - 3\n")
        elif sno == 4:
            print("\n\n DISEASE: XXXX - 4\n")
        elif sno == 5:
            print("\n\n DISEASE: XXXX - 5\n")
        elif sno == 6:
            print("\n\n DISEASE: XXXX - 6\n")
        else:
            print("\n\n DISEASE: XXXX - 7\n")



    # -----------------------------------------------------------------------------

    @staticmethod
    def send_data_py2cloud():
        f = open('controle.json', 'r')
        d = f.read()
        print(d)
        """ como eu mando dados para nuvem usando python ?"""


    def create_table_data(self, data):
        f = open('controle.json', 'w')
        f.write(data)
        f.close()

        f = open('controle.json', 'r')
        d = f.read()
        print(d)
        f.close()



    def data_in(self):
        print("\n\n " + self.info_data_in)
        what = True
        while what:
            # self.limpa_tela_win()
            # self.limpa_tela()
            self.menu('temperatura')
            temperatura = int(input("\n Informe a temperatura:  "))
            if temperatura != 1 and temperatura != 0:
                print("\n\n WARNNING: Invalid option!!")
            else:
                what = False

        what = True
        while what:
            # self.limpa_tela_win()
            # self.limpa_tela()
            self.menu("humidade")
            humidade = int(input("\n Informe a humidade:  "))
            if humidade != 1 and humidade != 0:
                print("\n\n WARNNING: Invalid option!!")
            else:
                what = False

        what = True
        while what:
            # self.limpa_tela_win()
            # self.limpa_tela()
            self.menu("umidade solo")
            umidade_solo = int(input("\n Informe a umidade:  "))
            if umidade_solo != 2 and umidade_solo != 3 and umidade_solo != 4:
                print("\n\n WARNNING: Invalid option!!")
            else:
                what = False

        return temperatura, humidade, umidade_solo

        # @staticmethod

    def limpa_tela_win(self):
        os.system('cls')


    # @staticmethod
    def limpa_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')


    def converterTempo(self, tempo):
        return 60 * tempo


    @staticmethod
    def menu(param):
        controller = 1
        while controller == 1:
            if param == "temperatura":
                print("\n\n  MENU DE OPÇÕES: Temperatura Ambiente\n\n 1 --> ALTA \n\n 0 --> BAIXA")
                controller = 0
            elif param == 'humidade':
                print("\n\n MENU DE OPÇÕES: Humidade Ambiente\n\n 1 --> ALTA \n\n 0 --> BAIXA")
                controller = 0
            elif param == 'umidade solo':
                print("\n\n MENU DE OPÇÕES: Humidade solo\n\n 2 --> Molhado \n\n 3 --> Moderado\n\n 4 --> Úmido")
                controller = 0
            else:
                controller = 1