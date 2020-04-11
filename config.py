import os

data_path = "./data/"
processed_data_path = "./processed_data/"
output_path = "./output/"


file_chat = os.path.join(data_path, "chat.txt")
file_stopwords = os.path.join(data_path, "stopword.txt")


file_qaqaq = os.path.join(processed_data_path, "questions.txt")
file_a = os.path.join(processed_data_path, "answers.txt")

seg_name = "jieba"

model_path = './tfidf/'

top = 15

file_questions_segs = os.path.join(processed_data_path, 'questions_segs.txt')

n = 3 # n-grams参数
bm25_path = './bm25/'
pkl_bm25 = os.path.join(bm25_path, "bm25_%i.model.small.pkl" % n)