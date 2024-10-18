import  serial

try:

    conectado = serial.Serial("COM8", 1152200, timeout=0.5)
    print(conectado)
    print("cconectado na porta", conectado.portstr)
except serial.SerialException:
    print("nao conectado")
    pass

while True:
    comando = input("Digite o comando ")

    if comando == "l":
        conectado.write(b'1')
    else: 
        conectado.write(b'0')

    if  input("Continue?").upper()=="N":
        break

conectado.close()
print("Conecao fechada")