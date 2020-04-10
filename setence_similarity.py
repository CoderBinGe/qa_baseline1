# encoding=utf-8


from gensim import corpora, models, similarities
from sentence import Sentence
from collections import defaultdict
import os
import pickle


class SentenceSimilarity():
    """
        通过tfidf模型计算相似度
    """

    def __init__(self, seg, model_path=None):
        self.seg = seg
        self.model_path = model_path
        if self.model_path is not None:
            self.pkl_file = os.path.join(self.model_path, "corpus_and_dictionary.pkl")
            self.file_model = os.path.join(self.model_path, "tfidf.model")
            self.file_index = os.path.join(self.model_path, 'index.index')

    def set_sentences(self, sentences):
        self.sentences = []
        for i in range(0, len(sentences)):
            self.sentences.append(Sentence(sentences[i], self.seg, i))

    # 构建其他复杂模型前需要的简单模型
    def simple_model(self, min_frequency=1):
        self.texts = self.get_cut_sentences()

        # 删除低频词
        frequency = defaultdict(int)
        for text in self.texts:
            for token in text:
                frequency[token] += 1

        self.texts = [[token for token in text if frequency[token] > min_frequency] for text in self.texts]
        self.dictionary = corpora.Dictionary(self.texts)
        self.corpus_simple = [self.dictionary.doc2bow(text) for text in self.texts]

    # 获取分词后的句子
    def get_cut_sentences(self):
        cut_sentences = []

        for sentence in self.sentences:
            cut_sentences.append(sentence.get_cut_sentence())

        return cut_sentences

    # tfidf模型
    # def TfidfModel(self):
    #     self.simple_model()
    #
    #     # 转换模型
    #     self.model = models.TfidfModel(self.corpus_simple)
    #     self.corpus = self.model[self.corpus_simple]
    #
    #     # 创建相似度矩阵
    #     self.index = similarities.MatrixSimilarity(self.corpus)

    # tfidf模型
    def TfidfModel(self):
        if os.path.exists(self.file_model):
            with open(self.pkl_file, 'rb') as f:
                self.dictionary, self.corpus_simple = pickle.load(f)
            self.model = models.TfidfModel.load(self.file_model)
            self.index = similarities.MatrixSimilarity.load(self.file_index)
            print('load tfidf model successfully.')
        else:
            self.simple_model()
            # 转换模型
            self.model = models.TfidfModel(self.corpus_simple)
            self.corpus = self.model[self.corpus_simple]
            # 创建相似度矩阵
            self.index = similarities.MatrixSimilarity(self.corpus)
            print("train tfidf model success.")
            # 保存模型
            if self.model_path is not None:
                with open(self.pkl_file, 'wb') as f:
                    pickle.dump([self.dictionary, self.corpus_simple], f)
                self.model.save(self.file_model)
                self.index.save(self.file_index)

    # 对新输入的句子（比较的句子）进行预处理
    def sentence2vec(self, sentence):
        sentence = Sentence(sentence, self.seg)
        vec_bow = self.dictionary.doc2bow(sentence.get_cut_sentence())
        return self.model[vec_bow]

    # 求最相似的句子
    def similarity(self, sentence, top=15):
        sentence_vec = self.sentence2vec(sentence)
        sims = self.index[sentence_vec]

        # 按相似度降序排序
        sim_sort = sorted(list(enumerate(sims)), key=lambda item: item[1], reverse=True)
        top_15 = sim_sort[0:top]
        return top_15

    # 求最相似的句子
    def similarity_k(self, sentence, k):
        sentence_vec = self.sentence2vec(sentence)
        sims = self.index[sentence_vec]
        # 按相似度降序排序
        sim_k = sorted(list(enumerate(sims)), key=lambda item: item[1], reverse=True)[:k]
        indexs = [i[0] for i in sim_k]
        scores = [i[1] for i in sim_k]
        return indexs, scores
