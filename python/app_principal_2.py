#!/usr/bin/python
# -*- coding: utf-8 -*-


# ---------------------------------------------------------------
#      Importing classes to help the main method of this app
# ---------------------------------------------------------------
import ModuloPyArduino as Mpa


# ---------------------------------------------------------------
#   Main application witch controll the application
# ---------------------------------------------------------------
def main_aplication(loop):

    print("\n\n Eu sou principal")

    # -----------------------------------------------------------
    #       Instanciando objeto da classe ModuloPyArduino
    # -----------------------------------------------------------
    p_a = Mpa.ModuloPyArduino()

    # -----------------------------------------------------------
    #       Exibe informação sobre App
    # -----------------------------------------------------------
    p_a.appInfo()

    # -----------------------------------------------------------
    #       Configurção do arduino: portas e velocidade
    # -----------------------------------------------------------

    # pdht, pumid, psoil, v = p_a.config_arduino()
    pdht, v = p_a.config_arduino()

    # -----------------------------------------------------------
    #           Conexão com arduino
    # -----------------------------------------------------------
    # con_s = p_a.set_conection(ps, v)
    con_dht = p_a.set_conection(pdht, v)
    # con_umid = p_a.set_conection(pumid, v)
    # con_soil = p_a.set_conection(psoil, v)

    # -----------------------------------------------------------
    # Calling the loop method to read data form arduino,
    # setting up it and send it to the cloud mongoDB
    #------------------------------------------------------------
    p_a.serialLoopApp(con_dht, con_umid, con_soil, loop)

    close_all_conection()
    print("\n\n Apliacacao ENCERRADA")


def close_all_conection():
    global con_s
    global con_dht
    global con_umid
    global con_soil

    con_s.close()
    con_dht.close()
    con_soil.close()
    con_umid.close()


# ---------------------------------------------------------
#  This is the method which start running tha application
# ---------------------------------------------------------
def run_application(rodar):

    while rodar == 1:
        print("\n\n Apliacacao em execucao...\n\n ")
        main_aplication(rodar)
        close_all_conection()

    print("\n\n Apliacacao ENCERRADA")


# ---------------------------------------------------------
#  Calling de main method to start the application
#  1 ->  executando
#  0 ->  parado
# ---------------------------------------------------------

if __name__ == '__main__':

    main_aplication(1)
