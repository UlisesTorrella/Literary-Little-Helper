# Literary Little Helper
The main idea of this tiny project is to generate grammatically correct 
natural language. 

It's a literary helper in hopes to throw bits of inspiration to a stuck author. It 
feeds on the authors chosen texts, in my case lots of spanish written books, and makes small
meaningless poems and phrases.

From any corpus, given proper tokenization. It should generate
it's own inference rules to form a Context Sensitive grammar.

# Generating / Usage
This is the goal of this project. We can randomly generate grammatically correct sentences and verses. 

Build a model:
> train_model.py -n name -d directory -c corpus\

Tokenize (it might take a while, depends on the tokenizer):
> litlit_tokenize.py -n name -d directory \

Define a context sensitive grammar:
> train_grammar.py -n name -d directory -c corpus \

Generate:

For spanish:

Poems:

    litlithelp_spanish_poem.py -s syllables -r rhyme -d directory -n name \    
    Options: \
      -r <rhyme>     asonante, consonante \
      -s <syllables> syllables (int) \
      -d <directory> where the trained data is\
      -n <name>      trained data set name

If the corpus is too small, or the tokenization it's not correct, it wont be able to 
produce verses and rhymes. In that case shows "no pude"

Sentences:

   
      litlithelp_sentence.py -d directory -n name -s sentences
    
    Options:
      -d <directory> where is the trained data
      -n <name>      trained data set name
      -s <sentences> how many
      -h --help      Show this screen.
##Gibberish Poems:
>epílogo kaminando \
derroteros jubilable \
pasadizos repartía \
demasiado Admirable


>entre todo confecciona holandeses \
>entraba alimentamos apartemos \
>aligeramiento en acercásemos \
>considerando , hondamente Bebamos

>invertido, No tristemente ejemplar \
ahí quiero pensar condescendencia \
significativamente a incluirse \
preocupaciones en un acaricia 

>considerado – hasta sentimientos , arbitraria \
pronósticos por el centinela a Reconocer \
la felicidad pertenece tomado al costes \
la cerca están indiferente al oscurecer

##Gibberish Sentences:
>tercer , bueno , tal al frío terrón de clasificación que había la noche , que Jeremías Aureliano Buendía no cuando logró con el barrio de una ceremonia entera no es toda cosa que un frasco grande que la tierra .

>Los terrores fueron con ocasión minutos , como recién ahora fueron arrobadores . 

>aunque su hijo acaba , y el ensayo de nuestros deseos y con temor de su tesoro , muy echará ella esperando . 

>cuándo y absolutamente hubieron atado la mesa de comer haya de bailar , Telémaco y que incluso aman de Néstor engancharon los ojos , llenaron al muerto rey y que parecieron a quien trato y el pecho caliente . 

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