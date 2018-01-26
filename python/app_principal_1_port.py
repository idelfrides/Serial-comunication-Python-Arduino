#!/usr/bin/python
# -*- coding: utf-8 -*-

# date: 10/11/2017

__author__ = 'IDELFRIDES JORGE'
# Copyright (c) 2017 Engineer IDELFRIDES JORGE

# Written with python 2.7.14 | mongoDB-3.4.10 | pymongo-3.6
# A python script connecting to a MongoDB given a MongoDB Connection URI.

# ---------------------------------------------------------------
#      Importing classes to help the main method of this app
# ---------------------------------------------------------------
import ModuloPyArduino as Mpa
import time as t


# ---------------------------------------------------------------
#   Main application witch controll the application
# ---------------------------------------------------------------
def main_aplication_1p(loop):

    print("\n\n Eu sou principal kkkkkkkkkkkkkkkkk")

    # -----------------------------------------------------------
    #       Instanciando objeto da classe ModuloPyArduino: p_a
    # -----------------------------------------------------------
    p_a = Mpa.ModuloPyArduino()

    # -----------------------------------------------------------
    #       Exibe informação sobre App
    # -----------------------------------------------------------
    p_a.appInfo()

    # -----------------------------------------------------------
    #       Configurção do arduino: portas e velocidade
    # -----------------------------------------------------------

    pdht, v = p_a.config_arduino()

    # -----------------------------------------------------------
    #           Conexão com arduino: 1 or 2
    # -----------------------------------------------------------
    con_dht = p_a.set_conection2(pdht, v)
    # con_umid = p_a.set_conection2(pumid, v)
    # con_soil = p_a.set_conection2(psoil, v)

    # -----------------------------------------------------------
    # Calling the loop method to read data form arduino,
    # setting up it and send it to the cloud mongoDB
    #------------------------------------------------------------
    # p_a.serialLoopApp(con_dht, con_umid, con_soil, loop)

    i = 0
    while i < loop:
        dataArd = p_a.get_data_arduino2py(con_dht)
        print "\n\n Arduino leu:  ", dataArd
        i += 1
        t.sleep(2)

    con_dht.close()
    print("\n\n Apliacacao ENCERRADA")
    exit(0)

    # close_all_conection()
    # print("\n\n Apliacacao ENCERRADA")



# ----------------------------------------------------------------
#  This is the method which close all Arduino board conections
# ----------------------------------------------------------------
def close_all_conection():
    global con_s
    global con_dht
    global con_umid
    global con_soil

    con_s.close()
    con_dht.close()
    con_soil.close()
    con_umid.close()


# -----------------------------------------------------------
#  This is the method which start running tha application
# -----------------------------------------------------------
def run_application(rodar):

    while rodar == 1:
        print("\n\n Apliacacao em execucao...\n\n ")
        main_aplication_1p(rodar)
        close_all_conection()

    print("\n\n Apliacacao ENCERRADA")  


# ---------------------------------------------------------
#  Calling de main method to start the application
#  1 ->  the app is running
#  0 ->  the is stoped
# ---------------------------------------------------------

# if __name__ == '__main__':
main_aplication_1p(5)