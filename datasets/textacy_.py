import textacy

def as_stream(corpus):
    for recipe in corpus:
        content = recipe['instructions']
        yield content

corpus = textacy.fileio.read_json_lines("NYC+openrecipe.jsonl")
c = textacy.Corpus('en', texts=as_stream(corpus))
