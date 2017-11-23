 # -*- coding: utf-8 -*-

import DataProcess as dp
import time as t


def app_principal():
    """ This is the main method of application.
     It start this app and control it
    """
    start = dp.DataProcess()
    t_a, h_a, h_s = start.data_in()
    start.define_disease_table_data(t_a, h_a, h_s)


def run_app(rodar):
    while rodar == 1:
        print("\n\n Apliacacao em execução")
        app_principal()
        t.sleep(1)

    print("\n\n Apliacacao NAO em execução")


# --------------------------------------------------
#  Calling de main method to start the application
# --------------------------------------------------


run_app(1)   # executando
#run_app(0)   # parado
