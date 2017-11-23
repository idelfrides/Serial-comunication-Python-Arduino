# -*- coding: utf-8 -*-

import ModuloPyArduino as mpa
import time as t


def app_principal_led():
    """ This is the main method of application.
     It start this app and control it
    """

    start = mpa.ModuloPyArduino()
    p, v = start.config_arduino()
    con = start.set_conection(p, v)

    if con != 0:
        start.serial_loop(con)
    else:
        pass


def run_app(rodar):
    while rodar == 1:
        print("\n\n Apliacacao em execução")
        app_principal_led()
        t.sleep(1)

    print("\n\n Apliacacao NAO em execução")


def run_app_led():
    print("\n\n Apliacacao em execução")
    app_principal_led()
    t.sleep(1)
    print("\n\n Apliacacao NAO em execução\n\n\n")
    t.sleep(2)


# --------------------------------------------------
#  Calling de main method to start the application
# --------------------------------------------------

# run_app(1)   # executando
# run_app_led(0)   # parado

run_app_led()   # executando
