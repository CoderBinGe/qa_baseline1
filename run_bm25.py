from bm25 import *
from config import *
from utils import read_file
from cut_words import jieba_tokenize


def run_prediction(input_file, output_file):
    model = BM25Model()
    model.train()

    print('predict most similarity questions in %s' % input_file)
    sim_questions = model.predict(input_file)

    print("read reference answers from %s" % file_a)
    answers = read_file(file_a)

    print("result will write to %s" % output_file)
    with open(output_file, 'w', encoding='utf-8') as file_result:
        for top_sims in sim_questions:
            answer_list = []
            for j in range(0, len(top_sims)):
                answer_index = top_sims[j][0]
                answer = answers[answer_index]
                answer_list.append((answer, len(answer)))
            max_len_answer = sorted(answer_list, key=lambda x: x[1], reverse=True)[0][0]
            file_result.write(str(top_sims[j][1]) + '\t' + max_len_answer)
            file_result.write("\n")


# def run_prediction(input_file, output_file):
#     # 加载模型
#     model, answers, average_idf = load_bm25_model()
#     print("load model from %s success." % pkl_bm25)
#
#     # 处理输入的测试数据集
#     test_questions = read_file(input_file)
#
#     predict_answers = []
#     for q in test_questions:
#         q_tokens = jieba_tokenize(q)
#         indexes = list(range(model.corpus_size))
#         scores = get_bm25_scores(model=model, document=q_tokens,
#                                  indexes=indexes, average_idf=average_idf)
#         top_sims = sorted(enumerate(scores), key=lambda item: item[1], reverse=True)[:top]
#
#         candidates = []  # 候选答案
#         for x in top_sims:
#             candidates.append(answers[x[0]].replace("\t", " "))
#         # 选最长
#         candidates = sorted(candidates, key=lambda x: len(x), reverse=True)
#         print(candidates)
#         predict_answers.append(candidates[0])
#
#     write_file(file=output_file, content=predict_answers, mode='w', encoding='utf-8')


if __name__ == '__main__':
    input_file = "./processed_data/devQuestions.txt"
    output_file = "./output/bm25_result.txt"
    # create_bm25_model(file_qaqaq, file_a)
    run_prediction(input_file, output_file)
