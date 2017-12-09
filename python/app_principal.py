#!/usr/bin/python
# -*- coding: utf-8 -*-


# ---------------------------------------------------------------
#      Importing classes to help the main method of this app
# ---------------------------------------------------------------
import ModuloPyArduino as mpa
import DataProcess as dp
import time as t


# ---------------------------------------------------------------
#   Main application witch controll the application
# ---------------------------------------------------------------
# def main_aplication(loop):
def main_aplication():
    beforeState = 0
    correntState = 0

    print("\n\n Eu sou principal")

    # -----------------------------------------------------------
    #       Instanciando objetos das classes ModuloPyArduino
    #       e DataProcess
    # -----------------------------------------------------------
    p_a = mpa.ModuloPyArduino()
    dpo = dp.DataProcess()

    # -----------------------------------------------------------
    #       Exibe informação da App
    # -----------------------------------------------------------
    p_a.appInfo()

    # -----------------------------------------------------------
    #       Configurçaão do arduino: portas velocidade
    # -----------------------------------------------------------
    # psoil, v = p_a.config_arduino()
    pdht, pumid, psoil, v = p_a.config_arduino()

    # -----------------------------------------------------------
    #           Conexoa com arduino
    # -----------------------------------------------------------
    # con_s = p_a.set_conection(ps, v)
    con_dht = p_a.set_conection(pdht, v)
    con_umid = p_a.set_conection(pumid, v)
    con_soil = p_a.set_conection(psoil, v)

    # p_a.serial_loop_app(con_soil, loop)

    # con_soil.close()

    # ------------------------------------------------------------
    #      Recuperando dados coletados pelo arduino
    # ------------------------------------------------------------
    datadht = p_a.get_data_arduino2py(con_dht)
    dataumid = p_a.get_data_arduino2py(con_umid)
    datasoil = p_a.get_data_arduino2py(con_soil)

    # print('\n\n Deu certo\n\n valores nao verificados')
    # print(datasoil)

    close_all_conection()
    t.sleep(2)

    # ------------------------------------------------------------------
    #  Verify and Management  of the data obteined by arduino board
    # ------------------------------------------------------------------
    datadht_verified = p_a.validate_sensor_data('temperatura', datadht)
    dataumid_verified = p_a.validate_sensor_data('umidade', dataumid)
    datasoil_verified = p_a.validate_sensor_data('umidade solo', datasoil)

    if datadht_verified != 'indefinido' and dataumid_verified != 'indefinido':
        print('\n\n Deu certo\n\n valores verificados')
        print(datadht_verified, datasoil_verified, dataumid_verified)
        print(datasoil_verified)

        print('\n\n Deu certo\n\n valores nao verificados')
        print(datasoil)
        print(datadht, datasoil, dataumid)

        # -------------------------------------------------------------
        # Call a method to send data to cloud mongoDB DB --> not implementded yet
        # -------------------------------------------------------------
        # p_a.sendind_data_py2cloud(datadht_verified, dataumid_verified, datasoil_verified)

        # Numerical data
        # dpo.formataArquivoParam(datadht, dataumid, datasoil)

        # Recupera o estado atual da plantação por meio dos parãmetros
        # temperatura, umidade e umidade do solo
        correntState = dpo.define_disease(datadht_verified, dataumid_verified, datasoil_verified)
        sno = correntState

        if correntState != beforeState:
            dpo.formataArquivoControle(1, 1, sno)
            beforeState = correntState
        else:
            sno = beforeState
            dpo.formataArquivoControle(1, 0, sno)
            # dpo.formataArquivoControle(1, 0, beforeState)


        # -------------------------------------------------------------
        # Invoca o metodo para indicar a c4.5 a existência de dados
        # para analisar
        # -------------------------------------------------------------

        # DEPOIS ENTRA AQUI

        # -------------------------------------------------------------
        #    Define e mostra a praga q está a ameaçar a plantação
        # -------------------------------------------------------------
        # dpo.define_disease(datadht_verified, dataumid_verified, datasoil_verified)

        close_all_conection()
        t.sleep(1)
    else:
        print('\n\n One or more values of parameter are invalid\n\n')
        close_all_conection()
        t.sleep(1)


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
def run_app(rodar):

    while rodar == 1:
        print("\n\n Apliacacao em execucao...\n\n ")
        # main_aplication(rodar)
        main_aplication()

    print("\n\n Apliacacao ENCERRADA")


# ---------------------------------------------------------
#  Calling de main method to start the application
#  1 ->  executando
#  0 ->  parado
# ---------------------------------------------------------

if __name__ == '__main__':
    run_app(1)
