# -*- coding: utf-8 -*-

import json


def create_file(texto):
    f = open('tabela.json', 'w')
    f.write(texto)
    f.close()
    # --------------------------------------------
    f2 = open('tabela.json', 'r')
    t = f2.read()
    print("\n\n mostrando testo do arquivo : \n\n")
    print(t)
    print(f2.readline())
    print(f2.tell())
    f2.seek(0)
    print(f2.tell())
    d = dict(f2)
    print(d)
    x = f2.readline()
    print(x)
    print (x[1])
    print (x[2])
    print (x[3])
    print(x[4])

    print "\n\n"
    f.close()


def formata_arquivo():
    t = 'HIGH'
    u = 'LOW'
    s = 'HIGH'

    # d = json.loads(texto)
    d = json.dumps({'temperatura': t, 'umidade': u, 'umidade solo': s}, sort_keys=True, indent=4, separators=(',', ':'))

    create_file(d)

# arquivo1()


formata_arquivo()
