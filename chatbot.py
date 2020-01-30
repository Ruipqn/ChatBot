import xml.etree.ElementTree as ET
from nltk.tokenize import RegexpTokenizer
import nltk
import pre_processing as PP
import Similarity_Functions as SF
import timeit
import sys

start_time = timeit.default_timer()

if len(sys.argv) >=3:
    file = sys.argv[1]
    filename = sys.argv[2]
else:
    print("Call should have 2 arguments, KB.xml and test.txt")
    print("KB.xml corresponds to the corpora file")
    print("test.txt corresponds to the file of questions (inputs)")
    sys.exit()


tree = ET.parse('KB.xml')
root = tree.getroot()

# DOCUMENTOS [ DOCUMENTO[TITULO, FAQLIST[FAQ[FONTE,PERGUNTAS[PERGUNTA]] ]]

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

#ITERATE DOCUMENTS
l_conjPergs = [] #forma do l_conjPergs [l_pergunta1,l_pergunta2,l_pergunta3....]
l_conjPergsTF = []
for x in range(len(root)): #iterate over DOCUMENTS
    #print(root[e][0].text) #TITULOS
    documento = root[x]

    for y in range(len(documento[1])): #iterate over FAQ LIST of that document
        faq = documento[1][y]
        l_perguntas = [] #forma do l_perguntas [perguntaX_estilo1,perguntaX_estilo2,...,id_reposta]
        l_perguntasTF = []
        for z in range(len(faq[1])): #iterate over FAQ
            pergunta = faq[1][z].text
            #print( faq[2].attrib['id'])
            perguntaTF = faq[1][z].text
            l_perguntasTF.append(perguntaTF)

            pergunta = PP.process(pergunta)
            l_perguntas.append(pergunta)

        l_perguntas.append([faq[2].attrib['id']])

        l_conjPergs.append(l_perguntas)
        l_conjPergsTF.append(l_perguntasTF)
use = "tf-idf"

fp = open(filename,'r',encoding = 'utf8')
resultados = open("resultados.txt",'w',encoding='utf8')
line = fp.readline()
error = 0
threshold_delete = 0
threshold_error =0
should_be_ignored=0

string = ''
listTF = []

for i in l_conjPergsTF:
    for l in range(len(i)):
        word = PP.process(i[l])
        word_aux = PP.stemmingWord(word)
        string += word_aux + ' '
    listTF.append(string)
    string = ''


while line:
    line_original = line
    line_TF = (line + '.')[:-1]
    #print("\nLinha:",line)
    line = PP.process(line)
    question = ' '.join([str(elem) for elem in line])

    if (use == "jaccard"):
        result = SF.jaccard(l_conjPergs, question) # [1- Probabilidade de ser Correto, frase que queriamos avaliar, numero da resposta obtida]
        threshold = 0.75
        if (float(result[0]) >= threshold):
            result[2] = "0"
            threshold_delete += 1
    elif (use == "med"):
        result = SF.editDistance(l_conjPergs, question)
        threshold = 100
        if (float(result[0]) >= threshold):
            result[2] = "0"
            threshold_delete += 1
    elif (use == "tf-idf"):
        result = SF.ComputeTFIDF(listTF, line_TF)
        threshold = 0.18455229296676515
        if (float(result[0]) <= threshold):
            result[2] = "0"
            threshold_delete += 1


    #write to file resultados
    resultados.write(result[2]+'\n')

    line = fp.readline()

fp.close()
resultados.close()

time = timeit.default_timer() - start_time
print("Execution time: " + str(time) + " seconds")
