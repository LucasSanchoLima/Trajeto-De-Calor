import cv2
from pathlib import Path

def Click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(str(frame[y][x]) + ": " + str(x) + ", " + str(y))

def Rua(frame, rua, cor):
    x = 0

    while x < frame.shape[0]:
        y = 0
        qtdPixel = 0
        qtdSalto = 40
        salto = 1

        while y < frame.shape[1]:
            if rua[x][y][0] >= 100:
                frame[x][y] = cor
                qtdPixel += 1
                if salto == 1:
                    salto = 0
                    y += -qtdSalto

            elif qtdPixel >= qtdSalto: break
            elif salto == 1: y+= qtdSalto

            y += 1
        x += 1

    return frame

caminhoVideo = "./video_input2.mp4"
#caminhoParte1 = str(Path(__file__).with_name("Rua1.png"))
caminhoParte1 = "./Ruas/Rua1.png"
caminhoRua = "./Ruas/Rua"

video = cv2.VideoCapture(caminhoVideo)
rua1 = cv2.imread(caminhoParte1)

if video.isOpened() == False:
    print("Erro ao abrir o arquivo de video")
    exit()

retorno, frame = video.read()
original = frame.copy()

input("Pressione enter para começar")

qtdCarro = [0,0,0,0,0,0,0,0]
qtdPixel = [0,0,0,0,0,0,0,0]
sensibilidadePixel = 10

cor = [98, 61, 35]
sensibilidade = 15

posicao = [[119,832],[371,880],[588,883],[822,884],[1207,879],[1408,916],[1630,838],[1844,880]]

#formato: [xi, xf, yi, yf]
recorte = [[0,1920,0,1080],[63,429,794,1062],[335,645,835,1065],[622,870,845,1055],[1078,1267,716,889],[1250,1647,705,1077],[1392,1705,698,949],[0,1920,0,1080]]
#[622,870,845,1055],[1078,1267,716,889],[1392,1705,698,949]

corAnterior = [cor, cor, cor, cor, cor, cor, cor, cor]

while video.isOpened():

    retorno, frame = video.read()

    if not retorno: break

    x = 0

    while x < 8:

        if frame[posicao[x][1]][posicao[x][0]][0] > corAnterior[x][0] + sensibilidade or frame[posicao[x][1]][posicao[x][0]][0] < corAnterior[x][0] - sensibilidade:
            if qtdPixel[x] >= sensibilidadePixel:
                qtdPixel[x] = 0
                qtdCarro[x] += 1
                cv2.imwrite("./Carros/Faixa"+str(x+1)+"/Carro"+str(qtdCarro[x])+".jpg", frame[recorte[x][2]:recorte[x][3],recorte[x][0]:recorte[x][1]])

        else: 
            qtdPixel[x] += 1
            corAnterior[x] = frame[posicao[x][1]][posicao[x][0]]

        x += 1

    
print(qtdCarro)

total = 15
porcentagemCalor = 255/max(qtdCarro)

x = 0
while x < 8:

    vermelho = int(qtdCarro[x]*porcentagemCalor)
    azul = 255 - vermelho

    original = Rua(original, cv2.imread(caminhoRua+str(x+1)+".png"), [azul, 0, vermelho])
    x += 1

cv2.imshow("original", original)

cv2.waitKey(0)

cv2.imwrite("MapaCalor.jpg", original)

cv2.destroyAllWindows()