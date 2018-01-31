#!/usr/bin/python
# -*- coding: utf-8 -*-
import MeCab
import sys
import operator
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
        self.carac = []
        self.termo = ''
        #tirar ponto, vírgula, (binding particle 係助詞), (case making particle),
        #( n sei oq é 同じ 大きな *), (partícula conjuntiva 接続助詞),
        # (paralel marker 　と　や　並立助詞), (fecha parenteses 括弧閉), (abre parenteses 括弧開)
        self.filters = ['句点', '読点', '係助詞', '格助詞', '連体化', '*', '接続助詞', '並立助詞', '括弧閉', '括弧開']
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
        termo = carac[6]

        if carac[1] in self.filters:
            if carac[1] == '句点':
                self.sentencecounter += 1
            else:
                return 1
        elif termo not in self.dados:
            self.dados[termo] = [1, self.sentences[self.sentencecounter]]
            #if carac[1] == '':
            #        print (termo)
        else:
            self.dados[termo][0] += 1
            self.dados[termo].append(self.sentences[self.sentencecounter])
    def readthrough(self):
        while self.node:
            self.queisso()
            self.node = self.node.next

    def arrumaesalva(self):
        tab = sorted(self.dados.items(), key=operator.itemgetter(1), reverse=True)
        sheet = pe.Sheet(tab)
        print(tab)
        sheet.save_as(self.path + '.csv')

    def ahcorre(self):
        self.open()
        self.splitphrases()
        self.parsemeca()
        self.makenode()
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
