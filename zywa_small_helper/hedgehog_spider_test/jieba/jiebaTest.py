#!/usr/bin/python
# -*- coding:utf-8 -*-
import jieba
from jieba import analyse
from collections import Counter

if __name__ == "__main__":

    word_lst = []
    key_list = []
    for line in open('/Users/magic/Downloads/123.txt'):  # 1.txt是需要分词统计的文档

        item = line.strip('\n\r').split('\t')  # 制表格切分
        # print item
        tags = analyse.extract_tags(item[0])  # jieba分词
        for t in tags:
            word_lst.append(t)
    print(word_lst)

    cnt = Counter()
    for word in word_lst:
        cnt[word] += 1
    print(cnt.most_common())  # [('blue', 3), ('red', 2), ('green', 1)]
