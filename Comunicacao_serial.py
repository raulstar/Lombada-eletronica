import  serial

try:

    conexao = serial.Serial("COM8", 9600, timeout=0.5)
    print(conexao)
    print("Conecxao na porta", conexao.portstr)
except serial.SerialException:
    print("nao conexao")
    pass

while True:
    serialstring = ""
    serialstring = input("Digite o comando ")
    conexao.write(serialstring.encode(encoding='ascii', errors='strict'))
    
    #conexao.write(b"teste")
    # if comando == "l":
    #     conexao.write(b'1')
    # else: 
    #     conexao.write(b'0')

    # if  input("Continue?").upper()=="N":
    #     break

conexao.close()
print("Conecao fechada")