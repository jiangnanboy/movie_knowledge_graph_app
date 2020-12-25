# -*- coding: utf-8 -*-
from django.shortcuts import render
 
# import sys
# sys.path.append("..")
from util.pre_load import segment
from util.nlp_ner import get_ner, get_ner_info, get_detail_ner_info

#分词+词性+实体识别
def ner_post(request):
	ctx ={}
	if request.POST:
		#获取输入文本
		input_text = request.POST['user_text']

		input_text = input_text[:300]
		#移除空格
		input_text = input_text.strip()
		#分词
		word_nature = segment.seg(input_text)

		text = ""
		#实体识别
		ner_list = get_ner(word_nature)
		#遍历输出
		for pair in ner_list:
			if pair[1] == 0:
				text += pair[0]
				continue
			#text += "<a href='detail.html?title=" + pair[0] + "'  data-original-title='" + get_ner_info(pair[1]) + "'  data-placement='top' data-trigger='hover' data-content='"+get_detail_ner_info(pair[1])+"' class='popovers'>" + pair[0] + "</a>"
			if pair[1] == 'nr': # 人物
				text += "<a style='color:blue'   data-original-title='" + get_ner_info(pair[1]) + "'  data-placement='top' data-trigger='hover' data-content='"+get_detail_ner_info(pair[1])+"' class='popovers'>" + pair[0] + "</a>"
			elif pair[1] == 'ns':# 地名
				text += "<a style='color:red'  data-original-title='" + get_ner_info(pair[1]) + "'  data-placement='top' data-trigger='hover' data-content='"+get_detail_ner_info(pair[1])+"' class='popovers'>" + pair[0] + "</a>"
			elif pair[1] == 'nt': # 机构
				text += "<a style='color:orange'  data-original-title='" + get_ner_info(pair[1]) + "'  data-placement='top' data-trigger='hover' data-content='"+get_detail_ner_info(pair[1])+"' class='popovers'>" + pair[0] + "</a>"
			elif pair[1] == 'nm': # 电影名
				text += "<a style='color:yellow'  data-original-title='" + get_ner_info(pair[1]) + "'  data-placement='top' data-trigger='hover' data-content='"+get_detail_ner_info(pair[1])+"' class='popovers'>" + pair[0] + "</a>"
			else: # 演员名
				text += "<a style='color:green'  data-original-title='" + get_ner_info(pair[1]) + "'  data-placement='top' data-trigger='hover' data-content='"+get_detail_ner_info(pair[1])+"' class='popovers'>" + pair[0] + "</a>"

		ctx['rlt'] = text

		'''
		分词及词性
		设置显示格式
		'''
		# 获取词和词性
		seg_word = list(term.word+" <strong><small>["+str(term.nature)+"]</small></strong> " for term in word_nature)
		seg_word = ''.join(seg_word)
		ctx['seg_word'] = seg_word

	return render(request, "index.html", ctx)
