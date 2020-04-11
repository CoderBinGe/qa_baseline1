from cut_words import tokenize_with_jieba
from gensim.summarization import bm25
from utils import *
from tqdm import tqdm


class BM25Model(object):
    def __init__(self, fresh=True):
        self.fresh = fresh
        self.model = None
        # self.average_idf = None

    @staticmethod
    def initialize():  # 初始化操作,分词
        segs = tokenize_with_jieba(input_file=file_qaqaq,
                                   output_file=file_questions_segs,
                                   stopwords_file=file_stopwords)
        return segs

    # 训练BM25模型
    def train(self):
        if self.fresh:
            print("重新分词，创建BM25模型...")
            segs = self.initialize()
        else:
            print("从%s读入现有分词结果，创建BM25模型..." % file_questions_segs)
            segs = read_file(file_questions_segs)
            segs = [eval(x) for x in segs]

        self.model = bm25.BM25(segs)
        # self.model = BM25Model = bm25.BM25(segs)
        # self.average_idf = sum(map(lambda k: float(BM25Model.idf[k]), BM25Model.idf.keys())) / len(BM25Model.idf.keys())

    # 输入测试问题，查找最相似的问题
    def predict(self, input_file):
        questions_segs = tokenize_with_jieba(input_file, stopwords_file=file_stopwords)
        print("输入测试文件 %s 分词完成" % input_file)
        model = self.model
        # average_idf = self.average_idf
        # print(average_idf)

        results = []
        for q in questions_segs:
            scores = model.get_scores(q)
            top_sims = sorted(enumerate(scores), key=lambda item: item[1], reverse=True)[:top]
            results.append(top_sims)
        return results


#####################################################################################################
def create_bm25_model(questions, answers):
    questions_tokens = []
    for q in tqdm(questions, desc="cut"):
        q_tokens = n_grams(q, n)
        questions_tokens.append(q_tokens)

    model = bm25.BM25(questions_tokens)
    average_idf = sum(float(val) for val in model.idf.values()) / len(model.idf)
    data = [model, answers, average_idf]
    save_to_pkl(file=pkl_bm25, data=data)
    return model, answers, average_idf


def load_bm25_model():
    return read_from_pkl(pkl_bm25)


def get_bm25_scores(model, document, indexes, average_idf):
    """Computes and returns BM25 scores of given `document` in relation to
    every item in corpus.

    Parameters
    ----------
    model : bm25 Model
    document : list of str
        Document to be scored.
    indexes :
    average_idf : float
        Average idf in corpus.

    Returns
    -------
    list of float
        BM25 scores.
    """
    scores = []
    for index in indexes:
        score = model.get_score(document, index, average_idf)
        scores.append(score)
    return scores
