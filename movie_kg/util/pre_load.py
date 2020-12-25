# -*- coding: utf-8 -*-
from pyhanlp import HanLP
from Model.neo4j_models import Neo4j_Handle

import torch
import torch.nn as nn
import pickle
import os

def init_model():
    words_path = os.path.join(os.getcwd() + '/util', 'words.pkl')
    with open(words_path, 'rb') as f_words:
        words = pickle.load(f_words)

    classes_path = os.path.join(os.getcwd() + '/util', "classes.pkl")
    with open(classes_path, 'rb') as f_classes:
        classes = pickle.load(f_classes)

    classes_index_path = os.path.join(os.getcwd() + '/util', "classes_index.pkl")
    with open(classes_index_path, 'rb') as f_classes_index:
        classes_index = pickle.load(f_classes_index)

    index_classes = dict(zip(classes_index.keys(), classes_index.values()))

    class classifyModel(nn.Module):

        def __init__(self):
            super(classifyModel, self).__init__()
            self.model = nn.Sequential(
                nn.Linear(len(words), 128),
                nn.ReLU(),
                nn.Dropout(0.5),
                nn.Linear(128, 64),
                nn.ReLU(),
                nn.Dropout(0.5),
                nn.Linear(64, len(classes)))

        def forward(self, x):
            out = self.model(x)
            return out


    model = classifyModel()
    model_path = os.path.join(os.getcwd() + '/util', "chatbot_model.h5")
    model.load_state_dict(torch.load(model_path))
    return model, words, classes, index_classes

def init_hanlp():
    segment = HanLP.newSegment().enableNameRecognize(True).enableOrganizationRecognize(True).enablePlaceRecognize(True).enableCustomDictionaryForcing(True)
    return segment

def init_neo4j():
    neo4jconn = Neo4j_Handle()
    neo4jconn.connectNeo4j()
    return neo4jconn

def init_name_dict():
    root = os.path.abspath(os.path.join(os.getcwd(), ".."))
    actor_path = os.path.join(root, 'data/custom_dict/演员名dict.txt')
    movie_path = os.path.join(root, 'data/custom_dict/电影名dict.txt')

    actor_name_dict = {}
    movie_name_dict = {}

    with open(actor_path, 'r', encoding='utf-8') as actor_read, open(movie_path, 'r', encoding='utf-8') as movie_read:
        for line in actor_read:
            line = line.strip().split('#')
            actor_name_dict[line[1]] = line[0]
        for line in movie_read:
            line = line.strip().split('#')
            movie_name_dict[line[1]] = line[0]

    return actor_name_dict, movie_name_dict

def init_category_dict():
    root = os.path.abspath(os.path.join(os.getcwd(), ".."))
    movie_category_path = os.path.join(root, 'data/custom_dict/电影类型dict.txt')

    movie_category = {}

    with open(movie_category_path, 'r', encoding='utf-8') as category_read:
        for line in category_read:
            line = line.strip().split(":")
            movie_category[line[0]] = line[2]
            movie_category[line[1]] = line[2]
    return movie_category

# 初始化
segment = init_hanlp()

# 初始化
neo4jconn = init_neo4j()

# 初始化学科名
name_dict = init_name_dict()

# 初始化分类模型，词典等
model_dict = init_model()

# 初始化电影类型词典
category_dict = init_category_dict()
