#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import random as r
import json


class DataProcess(object):
    temperatura = -1
    info = """
         Informação sobre app  kkkk
         hhhhhh ooooo nnnn jjjjj
         ppppppppp sssss kkkk frrrr
         wwwww aaaa qqqqq zzzz xxxx                    
     """

    info_data_in = """ Entrada de dados para testar o algoritmo """

    def __init__(self):
        print("\n\n ---------------------------------------------")
        print(self.info)
        print("\n ---------------------------------------------")

    def data_in(self):
        print("\n\n " + self.info_data_in)
        what = True
        while what:
            # self.limpa_tela_win()
            # self.limpa_tela()
            self.menu('temperatura')
            temperatura = int(input("\n Informe a temperatura:  "))
            if temperatura != 1 and temperatura != 0:
                print("\n\n WARNNING: Invalid option!!")
            else:
                what = False

        what = True
        while what:
            # self.limpa_tela_win()
            # self.limpa_tela()
            self.menu("humidade")
            humidade = int(input("\n Informe a humidade:  "))
            if humidade != 1 and humidade != 0:
                print("\n\n WARNNING: Invalid option!!")
            else:
                what = False

        what = True
        while what:
            # self.limpa_tela_win()
            # self.limpa_tela()
            self.menu("umidade solo")
            umidade_solo = int(input("\n Informe a umidade:  "))
            if umidade_solo != 2 and umidade_solo != 3 and umidade_solo != 4:
                print("\n\n WARNNING: Invalid option!!")
            else:
                what = False

        return temperatura, humidade, umidade_solo

    # @staticmethod
    def limpa_tela_win(self):
        os.system('cls')

    # @staticmethod
    def limpa_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def menu(param):
        controller = 1
        while controller == 1:
            if param == "temperatura":
                print("\n\n  MENU DE OPÇÕES: Temperatura Ambiente\n\n 1 --> ALTA \n\n 0 --> BAIXA")
                controller = 0
            elif param == 'humidade':
                print("\n\n MENU DE OPÇÕES: Humidade Ambiente\n\n 1 --> ALTA \n\n 0 --> BAIXA")
                controller = 0
            elif param == 'umidade solo':
                print("\n\n MENU DE OPÇÕES: Humidade solo\n\n 2 --> Molhado \n\n 3 --> Moderado\n\n 4 --> Úmido")
                controller = 0
            else:
                controller = 1


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


    # @staticmethod
    def define_disease(self, t, h, s):
        """ define a disease under the atributes
            t = temperatue, h = humidity, s = soil moisture
        """

        if t == "HIGH" and h == "HIGH" and s == "WET":
            self.show_disease(1)
        elif t == "LOW" and h == "HIGH" and s == "WET":
            self.show_disease(2)
        elif t == "LOW" and h == "HIGH" and s == "MODERATE":
            self.show_disease(3)
        elif t == "LOW" and h == "HIGH" and s == "WET":
            self.show_disease(4)
        elif t == "LOW" and h == "HIGH" and s == "MOIST":
            self.show_disease(5)
        elif t == "LOW" and h == "HIGH" and s == "MOIST":
            self.show_disease(6)
        elif t == "HIGH" and h == "HIGH" and s == "MOIST":
            self.show_disease(7)
        else:
            print("\n\n Combinação de parâmetros invalida. \n Aplicação será encerrada!!\n\n")
            return 0

    def define_disease_table_data(self, t, h, s):
        """ define a disease under the atributes
            t = temperatue, h = humidity, s = soil moisture
        """
        aux1 = r.randint(1, 2)
        aux2 = r.randint(5, 6)

        if t == 1 and h == 1 and s == 2:
            self.show_disease(1)
        elif t == 0 and h == 1 and s == 2 and aux1 == 1:
            self.show_disease(2)
        elif t == 0 and h == 1 and s == 3:
            self.show_disease(3)
        elif t == 0 and h == 1 and s == 2 and aux1 == 2:
            self.show_disease(4)
        elif t == 0 and h == 1 and s == 4 and aux2 == 5:
            self.show_disease(5)
        elif t == 0 and h == 1 and s == 4 and aux2 == 6:
            self.show_disease(6)
        elif t == 1 and h == 1 and s == 4:
            self.show_disease(7)
        else:
            print("\n\n Combinação de parâmetros invalida. \n Aplicação será encerrada!!\n\n")
            return 0

    # @staticmethod
    def show_disease(self, sno):
        """ print a disease corresponding the combination of atributes.
            there are 7 possibilities in this application
        """

        if sno == 1:
            print("\n\n DISEASE: XXXX - 1\n")
        elif sno == 2:
            print("\n\n DISEASE: XXXX - 2\n")
        elif sno == 3:
            print("\n\n DISEASE: XXXX - 3\n")
        elif sno == 4:
            print("\n\n DISEASE: XXXX - 4\n")
        elif sno == 5:
            print("\n\n DISEASE: XXXX - 5\n")
        elif sno == 6:
            print("\n\n DISEASE: XXXX - 6\n")
        else:
            print("\n\n DISEASE: XXXX - 7\n")