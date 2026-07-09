from collections import defaultdict
import json

class KuttiBPE():
    def __init__(self, corpus, mint_toks):
        self.merges = {}
        self.vocab = {i: bytes([i]) for i in range(256)}
        self.data = corpus
        self.mint_toks = mint_toks

    def get_merges(self, stream):
        counts = defaultdict(int)
        for i in zip(stream, stream[1:]):
            counts[i]+=1

        return counts
    
    def merge(self, pair, stream, new):
        i = 0
        new_stream=[]
        while i<len(stream):
            if i < len(stream)-1 and stream[i]==pair[0] and stream[i+1] == pair[1]:
                new_stream.append(new)
                i+=2
            else:
                new_stream.append(stream[i])
                i+=1

        return new_stream

    def train(self):
        merg = self.merges
        toks = self.data.encode('utf-8')
        tok_stre = list(map(int, toks))
        
        for i in range(self.mint_toks):
            count_pair = self.get_merges(tok_stre)
            max_p = max(count_pair, key = lambda p: count_pair[p])
            mint_tok = 256 + i
            re = self.merge(max_p, tok_stre, mint_tok)
            tok_stre = re
            merg[max_p]=mint_tok

        print("train complete, the merges was built, merged, stored in the construcotr dict itself")

    def build_vocab(self):
        merges_dict = self.merges
        for (p0, p1), token in merges_dict.items():
            self.vocab[token] = self.vocab[p0] + self.vocab[p1]
        
        print("vocab built with the merges")
        
    def encode(self, stringst):
        bytestr = stringst.encode('utf-8')
        token = list(map(int, bytestr))

        while len(token) > 1:
            count = self.get_merges(token)
            min_pair = min(count, key = lambda p: self.merges[p] if p in self.merges else float('inf'))
            if min_pair not in self.merges:
                break
            tokmint = self.merges[min_pair]
            repl = self.merge(min_pair, token, tokmint)
            token = repl
        return token

    def decode(self, bytestream):
        raw = b''.join([self.vocab[i] for i in bytestream])
        return raw.decode('utf-8')
  
    def save(self, path, name):
        state={
                f"{name} merges": {f"{p0},{p1}": tok for (p0, p1), tok in self.merges.items()}
                }
        with open(path, "w", encoding='utf-8') as f:
            json.dump(state, f)

        print(f"saved merges dict in {path}")


    def load_pretrained(self, name, path):
        with open(path, "r") as f:
            states = json.load(f)
        
        key = f"{name} merges"
        for i in states:
            if i == key:
                print(f"{name} found")
            else:
                print("pretrained model not found")

        self.merges = states[key]
        load_dict = defaultdict(int)
        for pair,tok in self.merges.items():
            p0, p1 = map(int,pair.split(','))
            load_dict[(p0,p1)] = tok

        vocabpre = {i: bytes([i]) for i in range(256)}
        for (p0, p1), tok in load_dict.items():
            vocabpre[tok] = vocabpre[p0] + vocabpre[p1]

        self.vocab = vocabpre
        self.merges = load_dict

