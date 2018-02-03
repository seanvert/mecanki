#!/usr/bin/python
# -*- coding: utf-8 -*-
import MeCab
import sys
import operator
from math import sin, cos, sqrt, pi

#import pyexcel as pe

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
        self.cores = {}
        # todos os tipos do texto
        self.classes = ['*', '固有名詞', '空白', '数接続', '数', '接尾', '一般', '格助詞', '係助詞', '読点', '代名詞', '自立', '連体化', '非自立', '形容動詞語幹', 'サ変接続', '接続助詞', '副詞可能', '終助詞', '副助詞／並立助詞／終助詞', '副助詞', '並立助詞', '助詞類接続', '名詞接続', '括弧開', '括弧閉', 'ナイ形容詞語幹', '特殊', 'アルファベット', '動詞接続', '接続詞的', '形容詞接続', '間投']

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
        termo = carac[6]
        #passa os filtros pra tirar as palavras indesejadas
        if carac[1] in self.filters:
            if carac[1] == '句点':
                #põe cor nas frases
                for i,c in zip(self.frase,self.tipos):
                    self.colorirhtml(i,c)
                self.frase = []
                #salva as frases coloridas no hash dos dados
                for e in self.termos:
                    self.dados[e].append(self.sentences[self.sentencecounter]+'。')
                self.termos = []
                self.sentencecounter += 1
            else:
                return 1
        elif termo not in self.dados:
            self.dados[termo] = [1]
            self.termos.append(termo)
            self.frase.append(self.node.surface)
            self.tipos.append(carac[1])
            #if carac[1] not in self.lista:
            #        print (carac[1])
            #        self.lista.append(carac[1])
        else:
            self.dados[termo][0] += 1
            self.frase.append(self.node.surface)
            self.termos.append(termo)
            self.tipos.append(carac[1])

    def colorirhtml(self, word, classe):
        cor_var = self.cores[classe]
        self.sentences[self.sentencecounter] = self.sentences[self.sentencecounter].replace(word, '<span style="color:'+ cor_var +'">' + word+'<span>')
    def separa_cores(self):
        quad = int(sqrt(len(self.classes)))+1
        div = pi/(2*quad)
        counter = 0
        for e in range(quad):
            b = int(sin(div+e*div)*255)
            for d in range(quad):
                g = int(sin(div+d*div)*255)
                r = int(cos(div+d*div)*255)
                print(r,g,b)
                if counter < len(self.classes):
                    self.cores[self.classes[counter]]= 'rgb('+str(r)+','+str(g)+','+str(b)+')'
                    counter+=1
                else:
                    return 1
    def readthrough(self):
        while self.node:
            self.queisso()
            self.node = self.node.next

    def arrumaesalva(self):
        tab = sorted(self.dados.items(), key=operator.itemgetter(1), reverse=True)
        print(type(tab))
        saida = open('saida.html', 'w')
        saida.write('<body bgcolor="#636363">')
        for a in tab:#self.dados:
            saida.write(str(a) + '\n')
            #for b in self.dados[a]:
            #    saida.write(str(b) + '\n')
        #print(self.lista)
        #print(self.sentences)
        #print(self.classes)
        #sheet = pe.Sheet(tab)
        #sheet.save_as(self.path + '.csv')

    def ahcorre(self):
        self.open()
        self.splitphrases()
        self.parsemeca()
        self.makenode()
        self.separa_cores()
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
