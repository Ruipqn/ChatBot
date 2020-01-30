import nltk
from nltk.tokenize import RegexpTokenizer
import unidecode


stopwords = nltk.corpus.stopwords.words('portuguese')
def checkstopwords(L):
    filtered_words = [word for word in L if word not in stopwords]
    return filtered_words

def unidecodeWord(pergunta):
    return unidecode.unidecode(pergunta)

def StemmingWord (pergunta):
    Stm = nltk.stem.RSLPStemmer()
    for w in range(len(pergunta)):
        pergunta[w] = Stm.stem(pergunta[w])

    return pergunta

def process (pergunta):

    pergunta = unidecodeWord(pergunta)
    tokenizer = RegexpTokenizer(r'\w+')
    pre_process = tokenizer.tokenize(pergunta) # swap to list of strings

    pre_process = checkstopwords(pre_process)
    pre_process = StemmingWord(pre_process)

    return pre_process



def processTFIDF (pergunta):

    pergunta = unidecodeWord(pergunta)
    tokenizer = RegexpTokenizer(r'\w+')
    pre_process = tokenizer.tokenize(pergunta) # swap to list of strings

    pre_process = checkstopwords(pre_process)
    pre_process = stemmingWord(pre_process)

    return pre_process

def stemmingWord(pergunta):
    Stm = nltk.stem.RSLPStemmer()
    for w in range(len(pergunta)):
        pergunta[w] = Stm.stem(pergunta[w])
    str = ''
    for w in range(len(pergunta)):
        str += pergunta[w] + ' '
    return str