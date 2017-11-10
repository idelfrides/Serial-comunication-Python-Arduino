# -*- coding: utf-8 -*-

import serial
import json
# import time as t


class ModuloPyArduino(object):
    info = """
          Informação sobre app vai aqui
          ppppppppp sssss kkkk frrrr eee
          wwwww aaaa qqqqq zzzz xxxx rrrr
      """

    def __init__(self):
        pass

    def imprime(self):
        print("\n Eu sou imprime() e vc eh \n Obama WM")
        print("\n\n ---------------------------------------------")
        print(self.info)
        print("\n ---------------------------------------------")

    def config_arduino(self):
        print("\n Eu sou configuracao do arduino\n")
        porta_s = 'COM7'
        porta_soil = 'COM3'
        porta_dht = 'COM2'
        porta_umid = 'COM5'
        speed = 9600
        return porta_s, porta_soil, porta_dht, porta_umid, speed

    def set_conection(self, p, v):
        return serial.Serial(p, v)

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
        con.write(action)

    def data_arduino2py(self, con):
        return con.readline()

    def serial_loop(self, conec):
        esc = 1
        while esc != 2:
            esc = self.menu()
            if esc != 2:
                self.data_py2arduino(conec, esc)
                leitura_serial = self.data_arduino2py(conec)
                print '\n Arduino diz \n ', leitura_serial
            else:
                print"\n\n Voce escolheu sair da aplicacao.\n Ate mais!!\n\n"

        return 0

    def get_serial_data(self, conec):
        return self.data_arduino2py(conec)

    def validate_sensor_data(self, param, valor):
        refval_dht = 40
        refval_umi = 30
        refval_soil = 25

        if param == "temperatura":
            if valor > refval_dht:
                estado_param = "HIGH"
                return estado_param
            elif valor < refval_dht:
                estado_param = "LOW"
                return estado_param
            else:
                estado_param = "indefinida"
                return estado_param
        elif param == "umidade":
            if valor > refval_umi:
                estado_param = "HIGH"
                return estado_param
            elif valor < refval_umi:
                estado_param = "LOW"
                return estado_param
            else:
                estado_param = "indefinida"
                return estado_param
        elif param == "umidade solo":
            if valor > refval_soil:
                estado_param = "WET"
                return estado_param
            elif valor < refval_soil:
                estado_param = "MOIST"
                return estado_param
            else:
                estado_param = "MODERATE"
                return estado_param
        else:
            print("\n\n WARNNING: The parameter given is not valid\n\n The stage of this parameter can't be definided!!!")
            # estado_param = "Parâmetro indefinido"
            # return  restado_param
            return 0

    def sendind_data_py2cloud(self, d1, d2, d3):
        print (d1, d2, d3)
        """ como eu mando dados para nuvel usando python ?"""

    def sinalizador(self):
        pass

    def create_table_data(self, data):
        f = open('tabela.jason', 'w')
        f.write(data)
        f.close()

        f = open('tabela.jason', 'r')
        d = f.read()
        print(d)
        f.close()

    def formata_arquivo(self, d1, d2, d3):
        d = json.dumps({'temperatura': d1, 'umidade': d2, 'umidade solo': d3}, sort_keys=True, indent=4, separators=(',', ':'))
        self.create_table_data(d)


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
