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
    l = f2.readline()
    print(l)
    print (l[1])
    print (l[2])
    print (l[3])
<<<<<<< HEAD
=======
    print(l[4])
>>>>>>> 255646f4279f8595d7247d390daeb77be100512e


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
