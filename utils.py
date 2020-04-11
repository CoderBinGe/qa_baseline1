import codecs
import pickle
from config import *

# 按行读入数据，返回一个List
def read_file(file):
    sentences = []
    file_obj = codecs.open(file, 'r', 'utf-8')
    while True:
        line = file_obj.readline()
        line = line.strip('\r\n')  # 回车换行
        if not line:
            break
        sentences.append(line)
    file_obj.close()

    return sentences


def write_file(file, content=None, mode="a", encoding='utf-8'):
    with open(file, mode, encoding=encoding) as f:
        if isinstance(content, str):
            content += "\n"
            f.write(content)
        elif isinstance(content, list):
            content = [i.strip("\n") + '\n' for i in content]
            f.writelines(content)
        elif content is None:
            pass
        else:
            raise ValueError("If content is not None, it must be list or str!")


def n_grams(text, n=3):
    """基于字符的n-gram切词

    :param text: str
        文本
    :param n: int
        n-grams参数
    :return: list
        提取的n元特征
    """
    chars = list(text)
    grams = []
    if len(chars) < n:
        grams.append("".join(chars))
    else:
        for i in range(len(chars) - n + 1):
            gram = "".join(chars[i:i + n])
            grams.append(gram)
    return grams


def save_to_pkl(file, data, protocol=None):
    if protocol is None:
        protocol = pickle.HIGHEST_PROTOCOL
    with open(file, 'wb') as f:
        pickle.dump(data, f, protocol=protocol)


def read_from_pkl(file):
    with open(file, 'rb') as f:
        data = pickle.load(f)
    return data

if __name__ == '__main__':
    sentences = read_file(file_qaqaq)
