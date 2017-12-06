#!/usr/bin/python
# -*- coding: utf-8 -*-

import serial as s
import DataProcess as Mdp

import time as t


class ModuloPyArduino(object):


    info = """
          Informação sobre app vai aqui
          ppppppppp sssss kkkk frrrr eee
          wwwww aaaa qqqqq zzzz xxxx rrrr
      """

    def __init__(self):
        pass

    def appInfo(self):
        print("\n Eu sou appInfo() e vc eh \n Obama WM")
        print("\n\n ---------------------------------------------")
        print(self.info)
        print("\n ---------------------------------------------")

    def config_arduino(self):
        print("\n Eu sou configuracao do arduino\n")
        # porta_s = 'COM7'
        porta_soil = "COM3"
        porta_dht = 'COM2'
        porta_umid = 'COM5'
        # porta_pista_led = 'COM3'
        speed = 9600
        return porta_dht, porta_umid, porta_soil, speed

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

    def set_conection2(self, p, v):
        try:
            ser = s.Serial(p, v)
        except AttributeError:
            print"\n porta já sem uso: ", ser.name



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

    def data_py2arduino(self, con, action):
        # con.write("Python escreve: ")
        con.write(action)

    def get_data_arduino2py(self, con):
        return con.readline()

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

    def serialLoopApp(self, condht, conumid, consoil, run):
        beforeState = 0
        correntState = 0

        dpo = Mdp.DataProcess()

        while run == 1:

            # ------------------------------------------------------------
            #      Recuperando dados coletados pelo arduino
            # ------------------------------------------------------------
            datadht = self.get_data_arduino2py(condht)
            dataumid = self.get_data_arduino2py(conumid)
            datasoil = self.get_data_arduino2py(consoil)

            # ------------------------------------------------------------------
            #  Verify and Management  of the data obteined by arduino board
            # ------------------------------------------------------------------
            datadht_verified = self.validate_sensor_data('temperatura', datadht)
            dataumid_verified = self.validate_sensor_data('umidade', dataumid)
            datasoil_verified = self.validate_sensor_data('umidade solo', datasoil)

            if datadht_verified != 'indefinido' and dataumid_verified != 'indefinido':

                # Numerical data
                dpo.formataArquivo(datadht_verified, dataumid_verified, datasoil_verified)

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
                self.send_data_py2cloud()
                t.sleep(10) # dorme(espera) por 10 segundos

            else:
                print('\n\n One or more values of parameter are invalid!!!\n\n')
                t.sleep(10) # dorme(espera) por 10 segundos


    def validate_sensor_data(self, param, valor):
        refval_dht = 30     # referência, média de temperatura relativa
        refval_umi = 30     # referência, média de umidade relativa
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


    @staticmethod
    def send_data_py2cloud():
        f = open('controle.json', 'r')
        d = f.read()
        print(d)
        """ como eu mando dados para nuvem usando python ?"""


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
