#!/usr/bin/python
# -*- coding: utf-8 -*-
from mhlib import isnumeric

import serial as s
import DataProcess as Mdp
import time as t
import ModulePyCloudMongo as Mpcm


# ----------------------------------------------------------------------------------
class ModuloPyArduino(object):
    tempoAtual = 300  # o tempo é dado em segundos: 300s = 5min
    info = """
          Informação sobre app vai aqui
          ppppppppp sssss kkkk frrrr eee
          wwwww aaaa qqqqq zzzz xxxx rrrr
      """

    def __init__(self):
        pass

    # ------------------------------------------------------------------------------
    def appInfo(self):
        print("\n Eu sou appInfo() e vc eh \n Obama WM")
        print("\n\n ---------------------------------------------")
        print(self.info)
        print("\n ---------------------------------------------")

    # ------------------------------------------------------------------------------
    def config_arduino(self):
        print("\n Eu sou configuracao do arduino\n")
        # porta_s = 'COM7'
        # porta_soil = "COM3"
        porta_dht = 'COM6'
        # porta_umid = 'COM6'
        # porta_pista_led = 'COM3'
        speed = 9600
        # return porta_dht, porta_umid, porta_soil, speed
        return porta_dht, speed

    # ------------------------------------------------------------------------------
    def set_conection(self, p, v):
        ser = s.Serial(p, v)
        print"\n porta em uso antes de teste: ", ser.name

        if not ser.isOpen():
            return ser.open()
        else:
            print"\n porta em uso ? ", ser.isOpen()
            print"\n porta em uso: ", ser.name
            print"\n Dump de config: ", ser
            # ser.close()
            t.sleep(10)
            # ser2 = s.Serial(p, v)
            return ser

    # ------------------------------------------------------------------------------
    def set_conection2(self, p, v):
        try:
            ser = s.Serial(p, v)
        except IOError:
            print"\n Erro ao abrir a conexao. Porta já sem uso:  "
            print "\n\n The application will be quited in 5 s!!!\n\n\n"
            t.sleep(5)
            exit(0)
            # return 0

    # ------------------------------------------------------------------------------
    def menu(self):
        what = True
        while what:
            print("\n\n MENU OPCOES\n\n 1 -> Acender \n 0 -> Apagar \n 2 -> Sair")
            op = input('\n Faca sua escolha:  ')
            if op != 1 and op != 0 and op != 2:
                print("\n WARNNING: invalid option")
            else:
                what = False
        return op

    # -----------------------------------------------------------------------------
    def data_py2arduino(self, con, action):
        # con.write("Python escreve: ")
        con.write(action)

    # -----------------------------------------------------------------------------
    def get_data_arduino2py(self, con):
        return con.readline()

    # -----------------------------------------------------------------------------
    def serial_loop(self, conec):
        esc = 1
        while esc != 2:
            esc = self.menu()
            if esc != 2:
                self.data_py2arduino(conec, esc)
                leitura_serial = self.get_data_arduino2py(conec)
                print '\n Arduino diz \n ', leitura_serial
            else:
                print"\n\n Voce escolheu sair da aplicacao.\n Ate mais!!\n\n"

        return 0

    # -----------------------------------------------------------------------------
    def serialLoopApp(self, condht, conumid, consoil, run):
        beforeState = 0
        correntState = 0

        # creating object of DataProcess and ModulePyCloudMongo classes: dpo, mpcmo
        dpo = Mdp.DataProcess()
        mpcmo = Mpcm.ModulePyCloudMongo()

        while run == 1:

            t.sleep(dpo.tempoPadrao)  # dorme(espera) por tempo armazenado na variavel tempoPadra

            # ------------------------------------------------------------
            #   Recuperando dados coletados pelo arduino
            # ------------------------------------------------------------
            datadht = self.get_data_arduino2py(condht)
            t.sleep(2)
            dataumid = self.get_data_arduino2py(conumid)
            t.sleep(2)
            datasoil = self.get_data_arduino2py(consoil)

            # verifica se os dados lidos são numéricos ou não
            checkData = self.validaTipoDado(datadht, dataumid, datasoil)

            # ------------------------------------------------------------------
            #  Verify and Management of the data obteined by arduino board
            # ------------------------------------------------------------------
            if checkData == 1:
                datadht_verified = self.validate_sensor_data('temperatura', datadht)
                dataumid_verified = self.validate_sensor_data('umidade', dataumid)
                datasoil_verified = self.validate_sensor_data('umidade solo', datasoil)

                if datadht_verified != 'indefinido' and dataumid_verified != 'indefinido':

                    # ----------------------------------------------------------
                    # format json data files: 1 - numerical received data
                    #                         2 - virified data
                    # ----------------------------------------------------------
                    dpo.formataArquivo(datadht, dataumid, datasoil, 1)   #1: dados numericos
                    dpo.formataArquivo(datadht_verified, dataumid_verified, datasoil_verified, 2) #2

                    # Recupera o estado atual da plantação por meio dos parâmetros -
                    # temperatura, umidade e umidade do solo
                    correntState = dpo.define_disease(datadht_verified, dataumid_verified, datasoil_verified)

                    if correntState != beforeState:
                        dpo.formataArquivoControle(1, 1, correntState)
                        beforeState = correntState
                        print(beforeState)
                    else:
                        dpo.formataArquivoControle(1, 0, beforeState)

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
                    if self.tempoAtual != dpo.tempoPadrao:
                         dpo.tempoPadrao = self.tempoAtual

                    # closing the conection with remote cloud mongo server
                    mpcmo.closeCMConection()
                else:
                    print('\n\n One or more values of parameter are invalid!!!\n\n')
            else:
                print("\n\n Falha de leitura do SENSOR DHT11 e/ou SOIL MISURE\n\n")


    # -----------------------------------------------------------------------------
    def validaTipoDado(self, d1, d2, d3):
        if type(d1) != str and type(d2) != str and type(d3) != str:
            return 1  # leitura realizada com sucesso, dados numéricos
        else:
            return 0  # leitura realizada com falha

    # ------------------------------------------------------------------------------
    def validate_sensor_data(self, param, valor):
        refval_dht = 30       # referência, média de temperatura relativa
        refval_umi = 30       # referência, média de umidade relativa
        # refval_soil = 20    # referência, média de umidade solo

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
                estado_param = "WET"    # molhado
                return estado_param
            elif valor >= 400 and valor <= 699:
                estado_param = "MOIST"   # umido
                return estado_param
            else:
                estado_param = "MODERATE"  #seco
                return estado_param
        else:
            print("\n\n WARNNING: The parameter given is not valid.\n\n The stage of this parameter can't be definided!!!")
            return 0

    # ---------------------------------------------------------------------------
    @staticmethod
    def send_data_py2cloud():
        f = open('controle.json', 'r')
        d = f.read()
        print(d)
        """ como eu mando dados para nuvem usando python ?"""

    # ---------------------------------------------------------------------------
    def sinalizador(self):
        pass


    """-------------------------------------
         Testando o algoritmo
    -------------------------------------"""

# ob = ModuloPyArduino()
#
# ob.imprime()
# print(ob.menu())
# p1, p2, p3, p4, v = ob.config_arduino()
# print(p1,v)
# print(p2,v)
# print(p3,v)
# print(p4,v)
# print(ob.config_arduino())
# print(ob.validate_sensor_data('temperatura', 20))
# print(ob.validate_sensor_data('umidade', 20))
# print(ob.validate_sensor_data('umidade solo', 20))
