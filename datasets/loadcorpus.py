import textacy
#import code

def as_stream(corpus):
    for recipe in corpus:
        content = " ".join(recipe['steps'])
        yield content

def as_meta(corpus):
    for recipe in corpus:
        yield {
                'title': recipe['title'],
                'servings': recipe['yield_']
        }

corpus = textacy.fileio.read.read_json_lines("NYC+openrecipes_cleanv1.jsonl")
metacorpus = textacy.fileio.read.read_json_lines("NYC+openrecipes_cleanv1.jsonl")

c = textacy.Corpus('en', texts=as_stream(corpus)) #, metadatas=as_meta(metacorpus))

#code.interact(locals=locals())
