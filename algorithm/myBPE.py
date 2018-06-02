import re, collections

def get_stats(vocab):
    pairs = collections.defaultdict(int)
    for word, freq in vocab.items():
        symbols = word.split()
        for i in range(len(symbols)-1):
            pairs[symbols[i],symbols[i+1]] += freq
    return pairs

def merge_vocab(pair, v_in):
    v_out = {}
    bigram = re.escape(' '.join(pair))
    p = re.compile(r'(?<!<\S)' + bigram + r'(?!\S)')
    for word in v_in:
        w_out = p.sub(''.join(pair), word)
        v_out[w_out] = v_in[word]
    return v_out

def txt2voc(text):
    wl = text.split()
    vocab = {}
    for w in wl:
        w = ' '.join(w)+' </w>'
        vocab[w] = vocab.get(w,0) + 1
    return vocab

def bpe(num_merges, text):
    vocab = txt2voc(text)
    pairs_lst = []
    for i in range(num_merges):
        pairs = get_stats(vocab)
        pairs_lst.append(pairs)
        best = max(pairs, key=pairs.get)
        vocab = merge_vocab(best, vocab)
    return (pairs_lst, vocab)

if __name__=='__main__':
    num_merges = 10
    text='low low low low low lowest lowest newer newer newer newer newer newer wider wider wider'
    (pairs_lst, vocab) = bpe(num_merges, text)
    for pairs in pairs_lst:
        print(pairs)
    print('vocab',vocab)
