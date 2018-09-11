#!/usr/bin/python
# -*- coding: utf-8 -*-

# Date: 10/11/2017

__author__ = 'IDELFRIDES JORGE'
# Copyright (c) 2017 Engineer IDELFRIDES JORGE

# Written with python 2.7.14 | pyserial 2.6 | mongoDB-3.4.10 | pymongo-3.6
# A python script connecting to a MongoDB given a MongoDB Connection URI.


# ---------------------------------------------------------------
#      Importing classes to help the main method of this app
# ---------------------------------------------------------------
import DataProcess as Dp
import ModuloPyArduino as Mpa
import time as t

# ---------------------------------------------------------------
#   Main application witch controll the application
# ---------------------------------------------------------------
def main_aplication(run):

    print("\n\n\n\n Principal 1: TEST")

    # -----------------------------------------------------------
    #       Instanciando objeto da classe ModuloPyArduino: p_a
    # -----------------------------------------------------------
    p_a = Mpa.ModuloPyArduino()
    dpo = Dp.DataProcess()

    # -----------------------------------------------------------
    #       Exibe informação sobre App
    # -----------------------------------------------------------
    p_a.appInfo()

    # -----------------------------------------------------------
    #       Configurção do arduino: porta e velocidade
    # -----------------------------------------------------------

    pdht, v = p_a.config_arduino()
    pumid = pdht
    psoil = pdht

    # -----------------------------------------------------------
    #       Conexão com arduino: with exception
    # -----------------------------------------------------------
    con_dht = p_a.set_conection_exception(pdht, v)
    # con_umid = p_a.set_conection_exception(pumid, v)
    # con_soil = p_a.set_conection_exception(psoil, v)

    con_umid = con_dht
    con_soil = con_dht

    # runAppTest(con_dht, run)  # call the runAppTest method to test the application.

    # -----------------------------------------------------------
    # Calling the loop method to read data form arduino,
    # setting up it and send it to the cloud mongoDB
    # -----------------------------------------------------------
    if run == 1:
         print("\n\n\n Apliacacao em execucao...\n\n ")
         while run == 1:
             dpo.serialLoopApp(con_dht, con_umid, con_soil, run)
             t.sleep(p_a.tempoPadrao)  # dorme(espera) por tempo armazenado na variavel tempoPadra
         close_all_conection()
         print("\n\n ==> Apliacacao ENCERRADA")
         print("\n\t --------------------------")
         print("\n\t @UTHOR: IDELFRIDES JORGE \n\t idelfridesjorgeCopyright2018 | All Rights Resered. \n\n\t---------------------------")
         exit(0)
    else:
         print("\n\n ==> Apliacacao NAO EXECUTADA")
         print("\n\t ---------------------")
         exit(0)

    # ----------------------------------------------------------


# runAppTest - the method whitch test the application
# without calling outhers modules
def runAppTest(con_dht, run):
    print("\n\n You are welcome !\n EU SOU RUN APP TEST\n\n")
    p_a = Mpa.ModuloPyArduino()

    if run == 1:
        print("\n\n\n Apliacacao em execucao...\n\n ")
        while run == 1:
             print("\n\t ------")
             data_arduino = con_dht.readline()
             print "\n Arduino leu TEMP -->", data_arduino
             t.sleep(p_a.tempoEspera)

             data_arduino = con_dht.readline()
             print "\n Arduino leu UMID -->", data_arduino
             t.sleep(p_a.tempoEspera)

             data_arduino = con_dht.readline()
             print "\n Arduino leu SOIL -->", data_arduino
             t.sleep(p_a.tempoEspera)
             # run += 1
             t.sleep(p_a.tempoPadrao)  # dorme(espera) por tempo armazenado na variavel tempoPadra

        close_one_conection(con_dht)
        # close_all_conection()
        print("\n\n ==> Apliacacao ENCERRADA")
        print("\n\t --------------------------")
        print("\n\t @UTHOR: IDELFRIDES JORGE \n\t idelfridesjorgeCopyright2018 | All Rights Resered. \n\n\t---------------------------")
        exit(0)
    else:
        print("\n\n ==> Apliacacao NAO EXECUTADA")
        print("\n\t --------------------------")
        print("\n\t @UTHOR: IDELFRIDES JORGE \n\t idelfridesjorgeCopyright2018 | All Rights Resered. \n\n\t---------------------------")
        exit(0)



# ----------------------------------------------------------------
#  This is the method which close one of Arduino board conection
# ----------------------------------------------------------------
def close_one_conection(con):
    con.close()


# ----------------------------------------------------------------
#  This is the method which close all Arduino board conections
# ----------------------------------------------------------------
def close_all_conection():
    global con_dht
    global con_umid
    global con_soil

    con_dht.close()
    con_soil.close()
    con_umid.close()


# --------------------------------------------------------------
#  This is the method starts running the application
# --------------------------------------------------------------
def run_application(rodar):
    #dpo = Dp.DataProcess()

    p_a = Mpa.ModuloPyArduino()
    print"\n\n eu sou run application...\n\n"

    if rodar == 1:
        controle = 1
        print("\n\n\n Apliacacao em execucao...\n\n ")
        while rodar == 1:
            main_aplication(rodar, controle)
            t.sleep(p_a.tempoPadrao)  # dorme(espera) por tempo armazenado na variavel tempoPadra
            controle += 1

        close_one_conection(con_dht)
        # close_all_conection()
    else:
        print("\n\n ==> Apliacacao NAO EXECUTADA")
        print("\n\t ---------------------")
        exit(0)




# ---------------------------------------------------------
#  Calling de main method to start the application
#  1 ->  the app is running
#  0 ->  the is stopped/quited
# ---------------------------------------------------------

if __name__ == '__main__':
    main_aplication(1)
