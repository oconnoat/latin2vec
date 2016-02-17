import gensim, logging
from gensim.models import word2vec
import glob
from lxml import etree
import regex as re
#from cltk.stem.lemma import LemmaReplacer



stopwords = set('ab, ac, ad, adhic, aliqui, aliquis, an, ante, apud, at, atque, aut, autem, cum, cur, de, deinde, dum, ego, enim, ergo, es, est, et, etiam, etsi, ex, fio, haud, hic, iam, idem, igitur, ille, in, infra, inter, interim, ipse, is, ita, magis, modo, mox, nam, ne, nec, necque, neque, nisi, non, nos, o, ob, per, possum, post, pro, quae, quam, quare, qui, quia, quicumque, quidem, quilibet, quis, quisnam, quisquam, quisque, quisquis, quo, quoniam, sed, si, sic, sive, sub, sui, sum, super, suus, tam, tamen, trans, tu, tum, ubi, uel, uero, unus, ut'.split(', '))
#http://www.perseus.tufts.edu/hopper/stopwords


class LatSentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in glob.glob(self.dirname):
            #Load the xml
            tree = etree.parse(fname,
            etree.XMLParser(remove_blank_text=True, resolve_entities=False))
            notag = etree.tostring(tree, encoding='utf8', method='text')
            for line in notag.splitlines():
                lemmatizer = LemmaReplacer('latin')
                punc = re.sub(r"\p{P}+",r" ",line).replace('\t',' ')
                yield [word.lower() for word in punc.split(' ') if word.lower() not in stopwords and word != '']
                #yield lemmatizer.lemmatize(punc.lower())

#all the latin
latin = LatSentences('Classics/*/opensource/*_lat.xml')

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
sentences = [['first', 'sentence'], ['second', 'sentence']]
# train word2vec on the two sentences

model = word2vec.Word2Vec(latin, size=200)
model.save('latinveclem.model')


