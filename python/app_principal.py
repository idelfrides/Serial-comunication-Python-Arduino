# -*- coding: utf-8 -*-

import ModuloPyArduino as mpa
# import DataProcess as dp
import time as t


def main_aplication(loop):
    print("\n\n Eu sou principal")
    p_a = mpa.ModuloPyArduino()
    # dpo = dp.DataProcess()

    p_a.appInfo()
    psoil, v = p_a.config_arduino()
    # ps, psoil, pdht, pumid, v = p_a.config_arduino()

    # con_s = p_a.set_conection(ps, v)
    con_soil = p_a.set_conection(psoil, v)
    # con_dht = p_a.set_conection(pdht, v)
    # con_umid = p_a.set_conection(pumid, v)

    p_a.serial_loop_app(con_soil, loop)

    # recuperando dados coletados pelo arduino
    # datadht = p_a.get_data_arduino2py(con_dht)
    # datasoil = p_a.get_data_arduino2py(con_soil)
    # dataumid = p_a.get_data_arduino2py(con_umid)

    # print('\n\n Deu certo\n\n valores nao verificados')
    # print(datasoil)

    # close_all_conection()
    # con_soil.close()
    # t.sleep(1)

    # --------------------------------------------------------------
    #  Management  of the data obteined by arduino board
    # --------------------------------------------------------------
    # datadht_verified = p_a.validate_sensor_data('temperatura', datadht)
    # dataumid_verified = p_a.validate_sensor_data('umidade', dataumid)
    # datasoil_verified = p_a.validate_sensor_data('umidade solo', datasoil)

    # if datadht_verified != 'indefinido' and datasoil_verified != 'indefinido':
        #  print('\n\n Deu certo\n\n valores verificados')
        # print(datadht_verified, datasoil_verified, dataumid_verified)
        # print(datasoil_verified)

        # print('\n\n Deu certo\n\n valores nao verificados')
        # print(datasoil)
        # print(datadht, datasoil, dataumid)

        # chama o metodo para enviar dados para cloud mongoDB DB
        # p_a.sendind_data_py2cloud(datadht_verified, datasoil_verified, dataumid_verified)

        # dados numéricos
        # dpo.formata_arquivo(datadht, datasoil, dataumid)

        # invoca o metodo para indicar o c4.5 a existência de dados para analisar

        # dpo.define_disease(datadht_verified, dataumid_verified, datasoil_verified)
        # close_all_conection()
        # t.sleep(1)
    # else:
      # print('\n\n One or more value of parameter are invalid\n\n')
        # close_all_conection()
        # t.sleep(1)


def close_all_conection():
    global con_s
    global con_dht
    global con_umid
    global con_soil

    con_s.close()
    con_dht.close()
    con_soil.close()
    con_umid.close()


def run_app(rodar):

    while rodar == 1:
        print("\n\n Apliacacao em execução")
        main_aplication(rodar)

    print("\n\n Apliacacao NAO em execução")


# ---------------------------------------------------
#  Calling de main method to start the application
#  1 ->  executando
#  0 ->  parado
# ---------------------------------------------------

run_app(1)
