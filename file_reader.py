import codecs

from config import *


class FileReader(object):
    """
        封装读文件操作,按行读取文件内容，并返回一个List
    """

    def __init__(self, file):
        self.file = file

    # 按行读入数据，返回一个List
    def read_lines(self):
        self.sentences = []
        file_obj = codecs.open(self.file, 'r', 'utf-8')
        while True:
            line = file_obj.readline()
            line = line.strip('\r\n')  # 回车换行
            if not line:
                break
            self.sentences.append(line)
        file_obj.close()

        return self.sentences


if __name__ == '__main__':
    file_obj = FileReader(processed_data_path + "trainQuestions.txt")
    train_sentences = file_obj.read_lines()
    print(train_sentences[:2])
