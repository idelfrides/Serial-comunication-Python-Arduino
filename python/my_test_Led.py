#!/usr/bin/python
# -*- coding: utf-8 -*-

import ModuloPyArduino as mpa
import time as t


def app_principal_led():
    """ This is the main method of application.
     It start this app and control it
    """
    """
        import serial
        ser = serial.Serial(0)  # open first serial port
        print ser.portstr       # check which port was really used
        ser.write("hello")      # write a string
        ser.close()             # close port 
    """


    start = mpa.ModuloPyArduino()
    p, v = start.config_arduino()
    con = start.set_conection(p, v)


    print "\n Status of conection: ", con
    if con != 0:
        start.serial_loop_app(con, 1)
    else:
        pass

    con.close()

# method run_app with parameter
def run_app(rodar):
    while rodar == 1:
        print("\n\n Apliacacao em execução")
        app_principal_led()
        t.sleep(1)
    print("\n\n Apliacacao NAO em execução")


# method run_app without parameter
def run_app_led():
    print("\n\n Apliacacao em execução")
    app_principal_led()
    t.sleep(2)
    print("\n\n Apliacacao Encerrada\n\n\n")
    t.sleep(2)


# --------------------------------------------------
#  Calling de main method to start the application
# --------------------------------------------------

# run_app(1)   # executando
# run_app_led(0)   # parado

run_app_led()   # executando
