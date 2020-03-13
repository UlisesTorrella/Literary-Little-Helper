# Literary Little Helper
The main idea of this tiny project is to generate grammatically correct meaningless
natural language. 

It's a literary helper in hopes to throw bits of inspiration to a stuck author. It 
feeds on the authors chosen texts, in my case lots of spanish written books, and makes small
meaningless poems and phrases.

From any corpus, given proper tokenization (here only the spanish tokenization is implemented). It should generate
it's own inference rules to form a Context Sensitive grammar.

# Generating / Usage
This is the goal of this project. We can randomly generate grammatically correct sentences and verses. 

Train a model:
> train_model.py -n name -d directory -c corpus\

Tokenize (it might take a while, depends on the tokenizer):
> train_tokenize.py -n name -d directory \

Define a context sensitive grammar: (it doesnt use the entire corpus, just a small fraction)
> train_grammar.py -n name -d directory -c corpus \

# Uses:
python 3
nltk
pickle
docopt
PIL for the publish.py thing

Generate:

For spanish:

Poems:

    litlithelp_stanza.py -s syllables -r rhyme -d directory \
    Options:
      -r <type_of_rhyme>     asonante, consonante
      -s <syllables> syllables for each verse
      -d <directory> where is the trained data
      -h --help      Show this screen.


If the corpus is too small, or the tokenization it's not correct, it wont be able to 
produce verses and rhymes. In that case shows "no pude"

There is also a publish.py feature, that generates an image to pretend to be a quoted fragment of a poem

Sentences:
   
      litlithelp_sentence.py -d directory -n times
    Options:
      -d <directory> where is the trained data
      -n <times>      how many

##Gibberish Poems:
>epílogo kaminando \
derroteros jubilable \
pasadizos repartía \
demasiado Admirable

>ornitorrincos desvinculado\
ánimo conmovedoramente \
la mitología a Tolstoy\
cardenal Retrospectivamente

>invertido, No tristemente ejemplar \
ahí quiero pensar condescendencia \
significativamente a incluirse \
preocupaciones en un acaricia 

>considerado – hasta sentimientos , arbitraria \
pronósticos por el centinela a Reconocer \
la felicidad pertenece tomado al costes \
la cerca están indiferente al oscurecer

##Gibberish Sentences:
>Cuando los vegetales entendieron , la muchacha alzó con un modo de bailarina .

>Los terrores fueron con ocasión minutos , como recién ahora fueron arrobadores . 

>aunque su hijo acaba , y el ensayo de nuestros deseos y con temor de su tesoro , muy echará ella esperando . 

>entre todo confecciona holandeses 
## Tokenization
The tokenization system is simple, but exhaustive.
It must contain a tokenize() method that give a word returns its syntactic meaning, also it must be a suryective function. (In the spanish tokenizer I consider unknown words as unique tokens)


Only the spanish language tokenizator is implemented in this repo.

## Modeling
###Grammar:
We need a model of the language and a tokenized dictionary of the vocabulary\
When modeling context sensitive grammar we only take small portions of the corpus to get a hint of how sentences are shaped.

Non terminal symbols are defined in a hierarchy that signify how "deep" into the sentence we are generating.
So, if we find various sentences starting with the same tokens, we have multiple paths to follow, making it 
less predictable yet correct.

The Grammar system is based on Symbols, auto defined during training.

###Model:
Only a simple AddOne Ngram model.
