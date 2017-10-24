# app.py
from flask import Flask, render_template, request
from wordnik import WordApi as wap, swagger
from config import myapikey # Delete this after you insert your key
apiUrl = 'http://api.wordnik.com/v4'
apiKey = myapikey # <----- Insert your api key here
client = swagger.ApiClient(apiKey, apiUrl)


class WordnikWrapper(object):
    def __init__(self, wordapi, dictionary):
        self._wordapi = wordapi

        if 'definitions' in dictionary:
            setattr(self, 'definitions', wordapi.getDefinitions(dictionary['word'], sourceDictionaries=dictionary['source_dict'], limit=10))
        if 'examples' in dictionary:
            setattr(self, 'examples', wordapi.getExamples(dictionary['word'], limit=5))
        if 'rel_words' in dictionary:
            setattr(self, 'rel_words', wordapi.getRelatedWords(dictionary['word']))
        if 'pronunciations' in dictionary:
            setattr(self, 'pronunciations', wordapi.getTextPronunciations(dictionary['word']))
        if 'hyphenation' in dictionary:
            setattr(self, 'hyphenation', wordapi.getHyphenation(dictionary['word']))
        if 'frequency' in dictionary:
            setattr(self, 'frequency', wordapi.getWordFrequency(dictionary['word'], startYear=1900))

    def reassign_definitions(self):
        templist = []
        try:
            for defn in self.definitions:
                templist.append(defn.text)
        except AttributeError:
            print("Missing definitions")
        else:
            self.definitions = templist

    def reassign_examples(self):
        templist = []
        try:
            for ex in self.examples.examples:
                templist.append(ex.text)
        except AttributeError:
            print("Missing examples")
        else:
            self.examples = templist

    def reassign_relatedwords(self):
        templist = []
        try:
            for synonym in self.rel_words[1].words:
                templist.append(synonym)
        except AttributeError:
            print("Missing rel_words")
        else:
            self.rel_words = templist

    def reassign_pronunciations(self):
        templist = []
        try:
            for pron in self.pronunciations:
                templist.append(pron.raw)
        except AttributeError:
            print("Missing pronunciations")
        else:
            self.pronunciations = templist

    def reassign_hyphenation(self):
        templist = []
        stringlist = []
        try:
            for syllable in self.hyphenation:
                stringlist.append(syllable.text)
        except AttributeError:
            print("Missing hyphenation")
        else:
            templist.append("-".join(stringlist))
            self.hyphenation = templist

    def reassign_frequency(self):
        templist = []
        try:
            templist.append(self.frequency.totalCount)
        except AttributeError:
            print("Missing frequency")
        else:
            self.frequency = templist

    def configure_attributes(self):
        self.reassign_definitions()
        self.reassign_examples()
        self.reassign_relatedwords()
        self.reassign_pronunciations()
        self.reassign_hyphenation()
        self.reassign_frequency()

    def print_all_attributes(self):
        try:
            print(self.definitions)
        except AttributeError:
            print("Missing definitions")
        try:
            print(self.examples)
        except AttributeError:
            print("Missing examples")
        try:
            print(self.rel_words)
        except AttributeError:
            print("Missing rel words")
        try:
            print(self.pronunciations)
        except AttributeError:
            print("Missing pronunciations")
        try:
            print(self.hyphenation)
        except AttributeError:
            print("Missing hyphenation")
        try:
            print(self.frequency)
        except AttributeError:
            print("Missing frequency")

    def dictify(self):
        # configures the object as a dictionary for output to the next file
        # reassign_attributes() should be run before this
        mydict = {}
        try:
            mydict['Definitions'] = self.definitions
        except AttributeError:
            print("Missing definitions")
        try:
            mydict['Examples'] = self.examples
        except AttributeError:
            print("Missing examples")
        try:
            mydict['Related Words'] = self.rel_words
        except AttributeError:
            print("Missing rel words")
        try:
            mydict['Pronunciations'] = self.pronunciations
        except AttributeError:
            print("Missing pronunciations")
        try:
            mydict['hyphenation'] = self.hyphenation
        except AttributeError:
            print("Missing hyphenation")
        try:
            mydict['Frequency'] = self.frequency
        except AttributeError:
            print("Missing frequency")
        return mydict

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")

@app.route('/attribute_list', methods=['GET', 'POST'])
def attribute_list():
    result = request.form
    wordApi = wap.WordApi(client)
    wrap = WordnikWrapper(wordApi, result)
    wrap.configure_attributes()
    wrap.print_all_attributes()
    return render_template("attribute_list.html", result = wrap.dictify())

@app.route('/well_done', methods=['GET', 'POST'])
def final():
    result = request.form
    # put result data into json for fun
    # also put result data into anki
    return render_template("well_done.html")

if __name__ == '__main__':
    app.run(debug=True)