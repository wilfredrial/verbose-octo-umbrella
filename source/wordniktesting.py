# wordniktesting.py
# Just a file to test the output of some
from wordnik import WordApi as wap
from wordnik import swagger
from config import myapikey # Delete this after you insert your key
apiUrl = 'http://api.wordnik.com/v4'
apiKey = myapikey # <----- Insert your api key here
client = swagger.ApiClient(apiKey, apiUrl)

wordApi = wap.WordApi(client)
TEST_WORD = 'scruple'
def ig_defns():
    definitions = wordApi.getDefinitions(TEST_WORD, sourceDictionaries='wiktionary', limit=10)
    print(len(definitions))
    print(definitions)

def ig_examples():
    my_examples = wordApi.getExamples(TEST_WORD, limit=10)
    for txt in my_examples.examples:
        print(txt.text)

def ig_relwords():
    related = wordApi.getRelatedWords(TEST_WORD)
    print(related[1].words)  # index 1 seems to be the synonyms
    for rel in related[1].words:
        print(rel)

def ig_pronunc():
    pronunciation = wordApi.getTextPronunciations(TEST_WORD)
    for pron in pronunciation:
        print(pron.raw)

def ig_hyphenation():
    hyphenation = wordApi.getHyphenation(TEST_WORD)
    for syllable in hyphenation:
        print(syllable.text)

def ig_freq():
    frequency = wordApi.getWordFrequency(TEST_WORD, startYear=1900, endYear=2012)
    print(frequency.totalCount)

def ig_audio():
    # I will need some fancy library to handle downloading files
    pass

if __name__ == "__main__":
    ig_defns()
    # ig_examples()
    # ig_relwords()
    # ig_pronunc()
    # ig_hyphenation()
    # ig_freq()
    print('end of main')