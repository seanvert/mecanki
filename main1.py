#!/usr/bin/python
# -*- coding: utf-8 -*-
import MeCab
import sys
import operator
import itertools
import pyexcel as pe

class Mecanki (object):
    def __init__(self, path, options=[]):
        self.t = MeCab.Tagger(" ".join(sys.argv))
        self.path = path
        self.options = []
        self.text = ''
        self.sentences = []
        self.node = None
        self.dados = {}
        self.sentencecounter = 0
        self.paleta = {}
        self.lista = []
        #paleta de cores
        self.paleta = [ 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]

        # todos os tipos do texto
        self.classes = {'*': '', '固有名詞': '', '空白': '', '数接続': '', '数': '', '接尾': '', '一般': '', '格助詞': '', '係助詞': '', '読点': '', '代名詞': '', '自立': '', '連体化': '', '非自立': '', '形容動詞語幹': '', 'サ変接続': '', '接続助詞': '', '副詞可能': '', '終助詞': '', '副助詞／並立助詞／終助詞': '', '副助詞': '', '並立助詞': '', '助詞類接続': '', '名詞接続': ''}
        #iteradores da parte colorida
        self.frase = []
        self.termos = []
        self.tipos = []
        #tirar ponto, vírgula, (binding particle 係助詞), (case making particle),
        #( n sei oq é 同じ 大きな *), (partícula conjuntiva 接続助詞),
        # (paralel marker 　と　や　並立助詞), (fecha parenteses 括弧閉), (abre parenteses 括弧開)
        self.filters = ['句点']
    def open(self):
        # open the file path
        self.text = open(self.path, 'r').read()

    #def settext(self):
    #    self.text =

    def splitphrases(self, dot='。'):
        self.sentences = self.text.replace('\n', '').replace("\u3000", '').split(dot)

    def parsemeca(self):
        self.t.parse(self.text)

    def makenode(self):
        self.node = self.t.parseToNode(self.text)
        print(self.node.surface)

    def sentences(self):
        return self.sentences

    def queisso(self):
        #separa as caracteristicas da palavra numa lista
        #Original Form\t, Part of Speech, Part of Speech section 1, Part of Speech section 2, Part of Speech section 3, Conjugated form, Inflection, Reading, Pronounciation
        carac = self.node.feature.split(",")
        #termo na forma de dicionário (conjugated form)
        #print(carac)
        #frase = []
        termo = carac[6]
        if carac[1] in self.filters:
            if carac[1] == '句点':
                #print(frase)
                for i,c in zip(self.frase,self.tipos):
                    self.colorirhtml(i,c)
                    self.frase = []
                for e in self.termos:
                    self.dados[e].append(self.sentences[self.sentencecounter])    
                self.sentencecounter += 1
            else:
                return 1
        elif termo not in self.dados:
            self.dados[termo] = [1]#, self.sentences[self.sentencecounter]]
            self.termos.append(termo)
            self.frase.append(self.node.surface)
            self.tipos.append(carac[1])
            #print(self.frase)
            #self.colorirhtml()
            #print(self.node.surface)
            if carac[1] not in self.lista:
                    print (carac[1])
                    self.lista.append(carac[1])
        else:
            self.dados[termo][0] += 1
            self.frase.append(self.node.surface)
            self.termos.append(termo)
            self.tipos.append(carac[1])
            #self.dados[termo].append(self.sentences[self.sentencecounter])
            #self.colorirhtml()
    def colorirhtml(self, word, classe):#, wordclass):
        #self.wordclasses.index(wordclass)
        cor_var = self.classes[classe]
        
        self.sentences[self.sentencecounter] = self.sentences[self.sentencecounter].replace(word, '<span style="color:'+ cor_var +'">' + word+'<span>')
        print(self.sentences[self.sentencecounter]+ '\n')

    def montapaleta(self):
        i=0
        for chave in self.classes:
            self.classes[chave] = 'rgb('+str(self.paleta[i]*2)+','+str(self.paleta[i]*i)+','+str(self.paleta[i]*3)+')'
            i+=1
            

    def readthrough(self):
        while self.node:
            self.queisso()
            self.node = self.node.next

    def arrumaesalva(self):
        tab = sorted(self.dados.items(), key=operator.itemgetter(1), reverse=True)
        sheet = pe.Sheet(tab)
        #print(tab)
        #print(self.sentences)
        print(self.classes)
        sheet.save_as(self.path + '.csv')

    def ahcorre(self):
        self.open()
        self.splitphrases()
        self.parsemeca()
        self.makenode()
        self.montapaleta()
        self.queisso()
        self.readthrough()
        self.arrumaesalva()

    def uhuuuul(self):

        print( "uhuuuul:D")

def main():

    mishima = Mecanki("/home/sean/Bureau/etudies programa/pythonjp/mishima")
    mishima.ahcorre()


if __name__ == '__main__':
    main()
