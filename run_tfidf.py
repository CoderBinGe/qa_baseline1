# encoding=utf-8

from config import *
from cut_words import *
from file_reader import FileReader
from setence_similarity import SentenceSimilarity


# 读入训练集
file_obj = FileReader(processed_data_path + "trainQuestions.txt")
train_questions = file_obj.read_lines()

# 读入测试集
file_obj = FileReader(processed_data_path + "devQuestions.txt")
dev_questions = file_obj.read_lines()


# 分词
if seg_name == 'jieba':
    seg = JiebaSeg(file_stopwords)
elif seg_name == 'thulac':
    seg = LacSeg(clear_sw=True)
else:
    raise ValueError("conf.seg_name值错误，可选值['jieba', 'thulac']")


# 训练模型
ss = SentenceSimilarity(seg, model_path=model_path)
ss.set_sentences(train_questions)
ss.TfidfModel()

file_result = open('./output/result.txt', 'w', encoding='utf-8')

with open("./processed_data/trainAnswers.txt", 'r', encoding='utf-8') as file_answer:
    line = file_answer.readlines()

for i in range(0, len(dev_questions)):
    top_15 = ss.similarity(dev_questions[i])

    for j in range(0, len(top_15)):
        answer_index = top_15[j][0]
        answer = line[answer_index]
        file_result.write(str(top_15[j][1]) + '\t' + str(answer))
    file_result.write("\n")

file_result.close()
file_answer.close()
