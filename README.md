
这个代码（[参考链接](https://github.com/SimonJYang/JDDC-Baseline-TFIDF)）进行了简单优化升级，
采用的是tfidf模型，主要思路是：首先计算用户的问题与问题库中的问题的相似度并选出top15的相似问题，然后去问题库对应的答案库中找出这15个问题对应的答案， 以此作为回答用户问题的候选答案。

**preprocess.py:**
* 将前3轮对话构造成Q1A1Q2A2Q3+A3的形式(Q或A可以是多个连续句子)，删除多余轮次的对话记录；
* 将同一角色连续说的话合并成单句；
* 删除轮次低于3的会话。

**file_reader.py:**
* 封装读文件操作,按行读取文件内容，并返回一个List。

**cut_words.py:**
* 分词工具做了一个封装。

**setence_similarity.py：**
* 通过tf-idf模型计算相似度。

**sentence.py:**
* 把对句子的所有处理做了一个封装。
