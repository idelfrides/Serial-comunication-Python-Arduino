#!/usr/bin/python
# -*- coding: utf-8 -*-


from mhlib import isnumeric

import time as t
import serial


# ----------------------------------------------------------------------------------
class ModuloPyArduino(object):
    tempoPadrao = 5  # o tempo eh dado em segundos: 300s = 5min
    tempoEspera = 3  # tempoEspera eh dado em segundos

    info = """
          Informação sobre app vai aqui.
          ...
          ...
          ...          
      """

    # construtor
    def __init__(self):
        pass


    # ------------------------------------------------------------------------------
    def appInfo(self):
        print("\n ---------------------------------------------")
        print(self.info)
        print("\n ---------------------------------------------")


    # ------------------------------------------------------------------------------
    def config_arduino(self):
        print("\n This is Arduino configuration...\n")
        porta_dht = 'COM6'
        speed = 9600

        """ return porta_dht que é igual para porta_umid e porta_soil
            speed - velocidade de transmissão"""
        return porta_dht, speed


    # ------------------------------------------------------------------------------
    def set_conection(self, p, v):
        # p - port
        # v - velocity
        seri = serial.Serial(p, v)

        print"\n porta em uso antes de teste: ", seri.name

        if not seri.isOpen():
            return seri.open()
        else:
            print"\n porta em uso ? ", seri.isOpen()
            print"\n porta em uso: ", seri.name
            print"\n Dump de config: ", seri
            # ser.close()
            t.sleep(10)
            # ser2 = s.Serial(p, v)
            return seri


    # ------------------------------------------------------------------------------
    # setting conectiong with exception Input/output error
    def set_conection_exception(self, p, v):
        try:
            ser = serial.Serial(p, v)
        except IOError:
            print"\n Erro ao abrir a conexao. Porta já em uso:  ", ser.name
            print "\n\n The application will be quited in 5s!!!\n\n\n"
            t.sleep(5)
            exit(0)
        else:
            return ser


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
    def get_data_arduino2py(self, con):
        return con.readline()


    # -----------------------------------------------------------------------------
    def data_py2arduino(self, con, action):
        con.write(action)

