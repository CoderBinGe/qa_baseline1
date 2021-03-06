# encoding=utf-8
import jieba
from thulac import thulac
from utils import *

class JiebaSeg(object):
    """
        基于jieba分词工具做了一个封装
            加载停用词
            对句子进行切分并去除停用词
    """

    def __init__(self, file_stopwords):
        self.stopwords = self.read_in_stopword(file_stopwords)

    def read_in_stopword(self, file_stopwords):
        with open(file_stopwords, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        stopwords = [x.strip() for x in lines]
        return stopwords

    def sentence_cut(self, sentence, stopword=True):
        seg_list = jieba.cut(sentence)  # 切词

        results = []
        for seg in seg_list:
            if stopword and seg in self.stopwords:
                continue  # 去除停用词
            results.append(seg)
        return results

    def setence_cut_for_search(self, sentence, stopword=True):
        # 搜索引擎模式，在精确模式的基础上，对长词再次切分，提高召回率
        seg_list = jieba.cut_for_search(sentence)

        results = []
        for seg in seg_list:
            if seg in self.stopwords and stopword:
                continue
            results.append(seg)

        return results


class LacSeg(object):
    """清华大学的分词器"""

    def __init__(self, clear_sw=True):
        self.name = "thulac"
        self.tl = thulac(filt=clear_sw)  # 使用过滤器去除一些没有意义的词语，例如“可以”

    def sentence_cut(self, sentence):
        lac_tokens = self.tl.cut(sentence)
        return [x[0] for x in lac_tokens]

    def setence_cut_for_search(self, sentence):
        return self.sentence_cut(sentence)


def tokenize_with_jieba(input_file, stopwords_file=None, cut_for_search=False, output_file=None):
    sentences = read_file(input_file)
    sentences_segs = []
    for sentence in sentences:
        if cut_for_search:
            seg_list = jieba.cut_for_search(sentence)
        else:
            seg_list = jieba.cut(sentence)
        sentences_segs.append(list(seg_list))

    # 如果传入了stopwords_file文件，去停用词
    if stopwords_file:
        stopwords = read_file(stopwords_file)
        segs = []
        for seg_list in sentences_segs:
            results = []
            for seg in seg_list:
                if seg in stopwords:
                    continue
                results.append(seg)
            segs.append(results)
    else:
        segs = sentences_segs

    if output_file:
        segs_out = [str(x) for x in segs]
        write_file(output_file, segs_out, mode='w', encoding='utf-8')

    return segs



def jieba_tokenize(text, for_search=False):
    if for_search:
        tokens = list(jieba.cut_for_search(text))
    else:
        tokens = list(jieba.cut(text))
    return tokens