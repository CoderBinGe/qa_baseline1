# encoding=utf-8

import re

# 预处理所使用的正则表达式
URL_REGULAR_EXPRESSION = """http[s]?://[a-zA-Z0-9|\.|/]+"""  # 匹配http或者https开头的url
URL_ANOTHER_REGULAR_EXPRESSION = """http[s]?://[a-zA-Z0-9\./-]*\[链接x\]"""
ORDERID_REGULAR_EXPRESSION = """\[ORDERID_[0-9]+\]"""  # 匹配[ORDERID_10002026]形式的order id
EMOJI_REGULAR_EXPRESSION = """#E-[a-z|0-9]+\[数字x\]|~O\(∩_∩\)O/~"""  # 匹配#E-s[数字x]形式和颜文字形式的表情
DATE_REGULAR_EXPRESSION = """\[日期x\]"""
TIME_REGULAR_EXPRESSION = """\[时间x\]"""
MONEY_REGULAR_EXPRESSION = """\[金额x\]"""
SITE_REGULAR_EXPRESSION = """\[站点x\]"""
NUMBER_REGULAR_EXPRESSION = """\[数字x\]"""
LOCATION_REGULAR_EXPRESSION = """\[地址x\]"""
NAME_REGULAR_EXPRESSION = """\[姓名x\]"""
MAIL_REGULAR_EXPRESSION = """\[邮箱x\]"""
PHONE_REGULAR_EXPRESSION = """\[电话x\]"""
PICTURE_REGULAR_EXPRESSION = """\[商品快照\]"""
SPLIT_SYN_REGULAR_EXPRESSION = """<s>"""
MULTIPLE_SPACES_REGULAR_EXPRESSION = """\s+"""


class Sentence(object):
    """
        对句子的所有处理做了一个封装包括：
            对句子清洗（新增）
            对句子进行分词
            获取分词之后的列表
            获取原句子（删除）
            获取清洗后的句子
            设置该句子得分（未用）
    """
    def __init__(self, sentence, seg, id=0):
        self.id = id
        # self.origin_sentence = sentence
        self.clean_sentence = self.clean(sentence)
        self.cut_sentence = self.cut(seg)

    # 对句子清洗
    def clean(self, sentence):
        """
        Get a sentnece, return a sentence proprocessed
        """
        s1 = re.sub(URL_ANOTHER_REGULAR_EXPRESSION, ' URL ', sentence)
        s2 = re.sub('&nbsp', '', s1)
        s3 = re.sub(ORDERID_REGULAR_EXPRESSION, ' ORDER ', s2)
        s4 = re.sub(DATE_REGULAR_EXPRESSION, ' DATE ', s3)
        s5 = re.sub(TIME_REGULAR_EXPRESSION, ' TIME ', s4)
        s6 = re.sub(MONEY_REGULAR_EXPRESSION, ' MONEY ', s5)
        s7 = re.sub(EMOJI_REGULAR_EXPRESSION, ' EMOJI ', s6)
        s8 = re.sub(SITE_REGULAR_EXPRESSION, ' SITE ', s7)
        s9 = re.sub(NUMBER_REGULAR_EXPRESSION, ' NUMBER ', s8)
        s10 = re.sub(LOCATION_REGULAR_EXPRESSION, ' LOCATION ', s9)
        s11 = re.sub(MAIL_REGULAR_EXPRESSION, ' EMAIL ', s10)
        s12 = re.sub(NAME_REGULAR_EXPRESSION, ' NAME ', s11)
        s13 = re.sub(PHONE_REGULAR_EXPRESSION, ' PHONE ', s12)
        s14 = re.sub(PICTURE_REGULAR_EXPRESSION, ' PICTURE ', s13)
        s15 = re.sub(URL_REGULAR_EXPRESSION, ' URL ', s14)
        s16 = re.sub(SPLIT_SYN_REGULAR_EXPRESSION, " ", s15)
        s17 = re.sub(MULTIPLE_SPACES_REGULAR_EXPRESSION, ' ', s16)
        return s17

    # 对句子分词
    def cut(self, seg):
        return seg.setence_cut_for_search(self.clean_sentence)
        # return seg.sentence_cut(self.clean_sentence)

    # 获取分词后的词列表
    def get_cut_sentence(self):
        return self.cut_sentence

    # 获取原句子
    # def get_origin_sentence(self):
    #     return self.origin_sentence

    # 获取清洗后的句子
    def get_clean_sentence(self):
        return self.clean_sentence

    # 设置该句子得分
    def set_score(self, score):
        self.score = score
