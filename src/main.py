import math
import random

class Cidade:
    def __init__(self, x=None, y=None):
        self.x = None
        self.y = None
        if x is not None:
            self.x = x
        else:
            self.x = int(random.random() * 200)
        if y is not None:
            self.y = y
        else:
            self.y = int(random.random() * 200)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def distanciaPara(self, cidade):
        xdistancia = abs(self.getX() - cidade.getX())
        ydistancia = abs(self.getY() - cidade.getY())
        distancia = math.sqrt((xdistancia * xdistancia) + (ydistancia * ydistancia))
        return distancia

    def __repr__(self):
        return str(self.getX()) + ", " + str(self.getY())


class AdmViagem:
    destino = []

    def addCidade(self, cidade):
        self.destino.append(cidade)

    def getCidade(self, index):
        return self.destino[index]

    def quantidadeCidades(self):
        return len(self.destino)


class Viagem:
    def __init__(self, admviagem, viagem=None):
        self.admviagem = admviagem
        self.viagem = []
        self.fitness = 0.0
        self.distancia = 0
        if viagem is not None:
            self.viagem = viagem
        else:
            for i in range(0, self.admviagem.quantidadeCidades()):
                self.viagem.append(None)

    def __len__(self):
        return len(self.viagem)

    def __getitem__(self, index):
        return self.viagem[index]

    def __setitem__(self, key, value):
        self.viagem[key] = value

    def __repr__(self):
        geneString = "|"
        for i in range(0, self.viagemTamanho()):
            geneString += str(self.getCidade(i)) + "|"
        return geneString

    def gerarIndividual(self):
        for cidadeIndex in range(0, self.admviagem.quantidadeCidades()):
            self.setCidade(cidadeIndex, self.admviagem.getCidade(cidadeIndex))
        random.shuffle(self.viagem)

    def getCidade(self, viagemPosition):
        return self.viagem[viagemPosition]

    def setCidade(self, viagemPosition, cidade):
        self.viagem[viagemPosition] = cidade
        self.fitness = 0.0
        self.distancia = 0

    def getFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.getDistancia())
        return self.fitness

    def getDistancia(self):
        if self.distancia == 0:
            viagemdistancia = 0
            for cidadeIndex in range(0, self.viagemTamanho()):
                fromCidade = self.getCidade(cidadeIndex)
                cidadeDestino = None
                if cidadeIndex + 1 < self.viagemTamanho():
                    cidadeDestino = self.getCidade(cidadeIndex + 1)
                else:
                    cidadeDestino = self.getCidade(0)
                viagemdistancia += fromCidade.distanciaPara(cidadeDestino)
            self.distancia = viagemdistancia
        return self.distancia

    def viagemTamanho(self):
        return len(self.viagem)

    def containsCidade(self, cidade):
        return cidade in self.viagem


class Populacao:
    def __init__(self, admviagem, populacaoTamanho, initialise):
        self.viagems = []
        for i in range(0, populacaoTamanho):
            self.viagems.append(None)

        if initialise:
            for i in range(0, populacaoTamanho):
                novaviagem = Viagem(admviagem)
                novaviagem.gerarIndividual()
                self.saveviagem(i, novaviagem)

    def __setitem__(self, key, value):
        self.viagems[key] = value

    def __getitem__(self, index):
        return self.viagems[index]

    def saveviagem(self, index, viagem):
        self.viagems[index] = viagem

    def getviagem(self, index):
        return self.viagems[index]

    def getFittest(self):
        fittest = self.viagems[0]
        for i in range(0, self.populacaoTamanho()):
            if fittest.getFitness() <= self.getviagem(i).getFitness():
                fittest = self.getviagem(i)
        return fittest

    def populacaoTamanho(self):
        return len(self.viagems)


class AG:
    def __init__(self, admviagem):
        self.admviagem = admviagem
        self.mutacaoRate = 0.015
        self.viagemTamanho = 5
        self.elitismo = True

    def agPopulacao(self, pop):
        novaPopulacao = Populacao(self.admviagem, pop.populacaoTamanho(), False)
        elitismoOffset = 0
        if self.elitismo:
            novaPopulacao.saveviagem(0, pop.getFittest())
            elitismoOffset = 1

        for i in range(elitismoOffset, novaPopulacao.populacaoTamanho()):
            pai1 = self.selecao(pop)
            pai2 = self.selecao(pop)
            filho = self.crossover(pai1, pai2)
            novaPopulacao.saveviagem(i, filho)

        for i in range(elitismoOffset, novaPopulacao.populacaoTamanho()):
            self.mutacao(novaPopulacao.getviagem(i))

        return novaPopulacao

    def crossover(self, pai1, pai2):
        filho = Viagem(self.admviagem)

        posicaoInicial = int(random.random() * pai1.viagemTamanho())
        posicaoFinal = int(random.random() * pai1.viagemTamanho())

        for i in range(0, filho.viagemTamanho()):
            if posicaoInicial < posicaoFinal and i > posicaoInicial and i < posicaoFinal:
                filho.setCidade(i, pai1.getCidade(i))
            elif posicaoInicial > posicaoFinal:
                if not (i < posicaoInicial and i > posicaoFinal):
                    filho.setCidade(i, pai1.getCidade(i))

        for i in range(0, pai2.viagemTamanho()):
            if not filho.containsCidade(pai2.getCidade(i)):
                for ii in range(0, filho.viagemTamanho()):
                    if filho.getCidade(ii) == None:
                        filho.setCidade(ii, pai2.getCidade(i))
                        break

        return filho

    def mutacao(self, viagem):
        for viagemPos1 in range(0, viagem.viagemTamanho()):
            if random.random() < self.mutacaoRate:
                viagemPos2 = int(viagem.viagemTamanho() * random.random())

                cidade1 = viagem.getCidade(viagemPos1)
                cidade2 = viagem.getCidade(viagemPos2)

                viagem.setCidade(viagemPos2, cidade1)
                viagem.setCidade(viagemPos1, cidade2)

    def selecao(self, pop):
        viagem = Populacao(self.admviagem, self.viagemTamanho, False)
        for i in range(0, self.viagemTamanho):
            randomId = int(random.random() * pop.populacaoTamanho())
            viagem.saveviagem(i, pop.getviagem(randomId))
        fittest = viagem.getFittest()
        return fittest


if __name__ == '__main__':

    admviagem = AdmViagem()

    cidade = Cidade(60, 200)
    admviagem.addCidade(cidade)
    cidade2 = Cidade(180, 200)
    admviagem.addCidade(cidade2)
    cidade3 = Cidade(80, 180)
    admviagem.addCidade(cidade3)
    cidade4 = Cidade(140, 180)
    admviagem.addCidade(cidade4)
    cidade5 = Cidade(20, 160)
    admviagem.addCidade(cidade5)
    cidade6 = Cidade(100, 160)
    admviagem.addCidade(cidade6)
    cidade7 = Cidade(200, 160)
    admviagem.addCidade(cidade7)
    cidade8 = Cidade(140, 140)
    admviagem.addCidade(cidade8)
    cidade9 = Cidade(40, 120)
    admviagem.addCidade(cidade9)
    cidade10 = Cidade(100, 120)
    admviagem.addCidade(cidade10)
    cidade11 = Cidade(180, 100)
    admviagem.addCidade(cidade11)
    cidade12 = Cidade(60, 80)
    admviagem.addCidade(cidade12)
    cidade13 = Cidade(120, 80)
    admviagem.addCidade(cidade13)
    cidade14 = Cidade(180, 60)
    admviagem.addCidade(cidade14)
    cidade15 = Cidade(20, 40)
    admviagem.addCidade(cidade15)
    cidade16 = Cidade(100, 40)
    admviagem.addCidade(cidade16)
    cidade17 = Cidade(200, 40)
    admviagem.addCidade(cidade17)
    cidade18 = Cidade(20, 20)
    admviagem.addCidade(cidade18)
    cidade19 = Cidade(60, 20)
    admviagem.addCidade(cidade19)
    cidade20 = Cidade(160, 20)
    admviagem.addCidade(cidade20)

    # Inicializa a população
    pop = Populacao(admviagem, 50, True);
    print
    "Distancia inicial: " + str(pop.getFittest().getDistancia())

    ag = AG(admviagem)
    pop = ag.agPopulacao(pop)
    for i in range(0, 100):
        pop = ag.agPopulacao(pop)

    print
    "Distância final: " + str(pop.getFittest().getDistancia())
    print
    "Solução:"
    print
    pop.getFittest()
