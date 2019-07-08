import subprocess
import requests
import obd
import time
import _thread as thread
import threading
from datetime import datetime, date

class MyThread (threading.Thread):  

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        #processo = subprocess.Popen(["/opt/sakis3g/sakis3g --sudo connect"], shell = True)
        while(1):
            time.sleep(10)
            #le o arquivo
            arquivo = open('/home/pi/Desktop/lista.txt', 'r')
            km_arquivo = arquivo.read()

            while (km_arquivo == ""):
                time.sleep(1)
                arquivo = open('/home/pi/Desktop/lista.txt', 'r')
                km_arquivo = arquivo.read()

            arquivo = open('/home/pi/Desktop/lista.txt', 'r')
            km_arquivo = arquivo.read()

            url = "http://manutencaoveicular.com.br/somar_km_do_veiculo.php"
            
            headers = {
                "From": "daniel.falsetti@gmail.com",
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0"
            }

            data={'codigo_dispositivo':1717 , 'km': km_arquivo, 'host': '192.168.90.90'}
            

            try:
                #response = requests.get(url, headers=headers)
                response = requests.post(url,data=data,headers=headers,params=data)
                print(response.text)

                #requests.post('http://danielfalsetti-001-site7.ftempurl.com:80/somar_km_do_veiculo.php', data={'codigo_dispositivo': '1313', 'km': 1, 'host': '192.168.90.90' })
                # limpa o arquivo
                arquivo = open('/home/pi/Desktop/lista.txt', 'w')
                arquivo.close()
            except:
                print("deu ruim")
                time.sleep(5)

MyThread().start()
#connection = obd.OBD("COM3")
#connection = obd.OBD("/dev/ttyUSB0", baudrate = 38400, fast=False)
connection = obd.OBD("/dev/ttyUSB0",fast=False)

'''
while(1):

    arquivo = open('/home/pi/Desktop/lista.txt', 'r')  # Abre o arquivo (leitura)
    conteudoarq = arquivo.read()

    if (conteudoarq == ""):
        conteudoarq = "0"
        conteudoarq = float(conteudoarq)
    else:
        conteudoarq = float(conteudoarq)

    time.sleep(1.2)

    arquivo = open('/home/pi/Desktop/lista.txt', 'w')
    resultado = conteudoarq + 1
    arquivo.write(str(resultado))
    arquivo.close()

    print(resultado)


'''


while(1):
    
    try:
        cmd = obd.commands.SPEED
        response1 = connection.query(cmd)
        tempo1 = datetime.now().time()
        resposta1 = str(response1)
        resposta1 = resposta1.replace("kph", "")
        resposta1 = float(resposta1)

        time.sleep(2)

        cmd = obd.commands.SPEED
        response2 = connection.query(cmd)
        tempo2 = datetime.now().time()
        resposta2 = str(response2)
        resposta2 = resposta2.replace("kph", "")
        resposta2 = float(resposta2)

        tempototal = datetime.combine(date.min, tempo2) - datetime.combine(date.min, tempo1)
        tempototal = str(tempototal).replace("0:00:02.", "")
        #tempototal = ((float(tempototal) + 100000) / 2) * 10
        tempototal = float(tempototal) + 1000000

        km = ((resposta1 + resposta2) / 2) * ((tempototal / 1000000) / 3600)
        
        arquivo = open('/home/pi/Desktop/lista.txt', 'r')  # Abre o arquivo (leitura)
        conteudoarq = arquivo.read()

        if (conteudoarq == ""):
            conteudoarq = "0"
            conteudoarq = float(conteudoarq)
        else:
            conteudoarq = float(conteudoarq)
        

        arquivo = open('/home/pi/Desktop/lista.txt', 'w')
        resultado = conteudoarq + km
        arquivo.write(str(resultado))
        arquivo.close()

        print(resultado)
    except:
        print("tenta pegar km novamente")







