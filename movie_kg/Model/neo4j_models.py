# -*- coding: utf-8 -*-
from py2neo import Graph,Node,Relationship,NodeMatcher

class Entity():
    '''
    知识点
    '''
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Neo4j_Handle():
	graph = None
	matcher = None
	def __init__(self):
		print("Neo4j Init ...")

	def connectNeo4j(self):
		self.graph = Graph("http://127.0.0.1:7474", username="neo4j", password="123")
		self.matcher = NodeMatcher(self.graph)

	# 一.实体查询
	def get_entity_info(self, name) -> list:
		'''
        查找该entity所有的直接关系
        :param name:
        :return:
        '''

		data = self.graph.run(
			"match (source)-[rel]-(target)  where source.name = $name " +
			"return rel ", name=name).data()

		json_list = []
		for an in data:
			result = {}
			rel = an['rel']
			relation_type = list(rel.types())[0]
			start_name = rel.start_node['name']
			end_name = rel.end_node['name']
			result["source"] = start_name
			result['rel_type'] = relation_type
			result['target'] = end_name
			json_list.append(result)

		return json_list

	# 三.关系查询都是直接1度关系
	# 1.关系查询:实体1(与实体1有直接关系的实体与关系)
	def findRelationByEntity1(self,entity1):
		answer = self.graph.run(
			"match (source)-[rel]-(target)  where source.name = $name " +
			"return rel ", name=entity1).data()

		answer_list = []
		for an in answer:
			result = {}
			rel = an['rel']
			relation_type = list(rel.types())[0]
			start_name = rel.start_node['name']
			end_name = rel.end_node['name']
			result["source"] = {'name': start_name}
			result['type'] = relation_type
			result['target'] = {'name': end_name}
			answer_list.append(result)

		return answer_list

	# 2.关系查询：实体2
	def findRelationByEntity2(self,entity1):
		answer = self.graph.run(
			"match (source)-[rel]-(target)  where target.name = $name " +
			"return rel ", name=entity1).data()

		answer_list = []
		for an in answer:
			result = {}
			rel = an['rel']
			relation_type = list(rel.types())[0]
			start_name = rel.start_node['name']
			end_name = rel.end_node['name']
			result["source"] = {'name': start_name}
			result['type'] = relation_type
			result['target'] = {'name': end_name}
			answer_list.append(result)

		return answer_list

	# 3.关系查询：实体1+关系
	def findOtherEntities(self,entity1,relation):
		answer = self.graph.run(
			"match (source)-[rel:" + relation + "]->(target)  where source.name = $name " +
			"return rel ", name=entity1).data()

		answer_list = []
		for an in answer:
			result = {}
			rel = an['rel']
			relation_type = list(rel.types())[0]
			start_name = rel.start_node['name']
			end_name = rel.end_node['name']
			result["source"] = {'name': start_name}
			result['type'] = relation_type
			result['target'] = {'name': end_name}
			answer_list.append(result)

		return answer_list

	# 4.关系查询：关系+实体2
	def findOtherEntities2(self,entity2,relation):

		answer = self.graph.run(
			"match (source)-[rel:" + relation + "]->(target)  where target.name = $name " +
			"return rel ", name=entity2).data()

		answer_list = []
		for an in answer:
			result = {}
			rel = an['rel']
			relation_type = list(rel.types())[0]
			start_name = rel.start_node['name']
			end_name = rel.end_node['name']
			result["source"] = {'name': start_name}
			result['type'] = relation_type
			result['target'] = {'name': end_name}
			answer_list.append(result)

		return answer_list

	# 5.关系查询：实体1+实体2
	def findRelationByEntities(self,entity1,entity2):
		answer = self.graph.run(
			"match (source)-[rel]-(target)  where source.name= $name1 and target.name = $name2 " +
			"return rel ", name1=entity1,name2=entity2).data()

		answer_list = []
		for an in answer:
			result = {}
			rel = an['rel']
			relation_type = list(rel.types())[0]
			start_name = rel.start_node['name']
			end_name = rel.end_node['name']
			result["source"] = {'name': start_name}
			result['type'] = relation_type
			result['target'] = {'name': end_name}
			answer_list.append(result)

		return answer_list

	# 6.关系查询：实体1+关系+实体2(实体-关系->实体)
	def findEntityRelation(self,entity1,relation,entity2):
		answer = self.graph.run(
			"match (source)-[rel:" + relation + "]->(target)  where source.name= $name1 and target.name = $name2 " +
			"return rel ", name1=entity1, name2=entity2).data()

		answer_list = []
		for an in answer:
			result = {}
			rel = an['rel']
			relation_type = list(rel.types())[0]
			start_name = rel.start_node['name']
			end_name = rel.end_node['name']
			result["source"] = {'name': start_name}
			result['type'] = relation_type
			result['target'] = {'name': end_name}
			answer_list.append(result)

		return answer_list

	# 四.问答
	'''
	0:nm 评分
	1:nm 上映时间
	2:nm 类型
	3:nm 简介(暂时没数据)
	4:nm 演员列表
	5:nnt 介绍 (暂时没数据)
	6:nnt ng电影作品
	7:nnt 电影作品
	8:nnt 参演评分大于 x
	9:nnt 参演评分小于 x
	10:nnt 电影类型
	11:nnt nnr合作电影列表
	12:nnt 电影数量
	13:nnt 出生日期(暂时没数据)
	14:评分大于x电影
	15:评分大于x的ng类型电影
	'''
	# 0:nm 评分
	def movie_rate(self, name):
		answer = self.graph.run(
			"match (m:Movie) where m.name = $name return m.name as name, m.rate as rate ", name=name).data()

		answer_dict = {}
		answer_name = []
		answer_list = []
		for an in answer:
			result = {}
			relation_type = '评分'
			start_name = an['name']
			end_name = an['rate']
			result["source"] = {'name': start_name}
			result['type'] = relation_type
			result['target'] = {'name': end_name}
			answer_list.append(result)
			answer_name.append(end_name+' 分')
		answer_dict['answer'] = answer_name
		answer_dict['list'] = answer_list

		if len(answer_name) == 0:
			return []

		return answer_dict

	# 1:nm 上映时间
	def movie_showtime(self, name):
		answer = self.graph.run(
			"match (m:Movie) where m.name = $name return m.name as name, m.showtime as showtime ", name=name).data()

		answer_dict = {}
		answer_name = []
		answer_list = []
		for an in answer:
			result = {}
			relation_type = '上映时间'
			start_name = an['name']
			end_name = an['showtime']
			result["source"] = {'name': start_name}
			result['type'] = relation_type
			result['target'] = {'name': end_name}
			answer_list.append(result)
			answer_name.append(end_name)
		answer_dict['answer'] = answer_name
		answer_dict['list'] = answer_list

		if len(answer_name) == 0:
			return []

		return answer_dict

	# 2: nm 类型
	def movie_category(self, name):
		answer = self.graph.run(
			"match (m:Movie) where m.name = $name return m.name as name, m.category as category", name=name).data()

		answer_dict = {}
		answer_name = []
		answer_list = []
		for an in answer:
			result = {}
			relation_type = '类型'
			start_name = an['name']
			end_name = an['category']
			result["source"] = {'name': start_name}
			result['type'] = relation_type
			result['target'] = {'name': end_name}
			answer_list.append(result)
			answer_name.append(end_name)
		answer_dict['answer'] = answer_name
		answer_dict['list'] = answer_list

		if len(answer_name) == 0:
			return []

		return answer_dict

	# 3:nm 简介(暂时没数据)
	def movie_info(self, name):
		pass

	# 4:nm 演员列表
	def movie_actors(self, name):
		answer = self.graph.run(
			"MATCH (m:Movie)-[rel:ACTOR]->(p:Person) where m.name = $name return rel", name=name).data()

		answer_dict = {}
		answer_name = []
		answer_list = []
		for an in answer:
			result = {}
			rel = an['rel']
			relation_type = list(rel.types())[0]
			start_name = rel.start_node['name']
			end_name = rel.end_node['name']
			result["source"] = {'name': start_name}
			result['type'] = relation_type
			result['target'] = {'name': end_name}
			answer_list.append(result)
			answer_name.append(end_name)
		answer_dict['answer'] = answer_name
		answer_dict['list'] = answer_list

		if len(answer_name) == 0:
			return []

		return answer_dict

	# 5:nnt 介绍 (暂时没数据)
	def actor_info(self, name):
		pass

	# 6:nnt ng电影作品
	def actor_category_movie(self, name, category):
		answer = self.graph.run(
			"MATCH (m:Movie)-[rel:ACTOR]->(p:Person) where p.name='" + name + "' and m.category=~'.*" + category +".*' return rel").data()

		answer_dict = {}
		answer_name = []
		answer_list = []
		for an in answer:
			result = {}
			rel = an['rel']
			relation_type = list(rel.types())[0]
			start_name = rel.start_node['name']
			end_name = rel.end_node['name']
			result["source"] = {'name': start_name}
			result['type'] = relation_type
			result['target'] = {'name': end_name}
			answer_list.append(result)
			answer_name.append(start_name)
		answer_dict['answer'] = answer_name
		answer_dict['list'] = answer_list

		if len(answer_name) == 0:
			return []

		return answer_dict

	# 7:nnt 电影作品
	def actor_movie(self, name):
		answer = self.graph.run(
			"MATCH (m:Movie)-[rel:ACTOR]->(p:Person) where p.name = $name return rel", name=name).data()

		answer_dict = {}
		answer_name = []
		answer_list = []
		for an in answer:
			result = {}
			rel = an['rel']
			relation_type = list(rel.types())[0]
			start_name = rel.start_node['name']
			end_name = rel.end_node['name']
			result["source"] = {'name': start_name}
			result['type'] = relation_type
			result['target'] = {'name': end_name}
			answer_list.append(result)
			answer_name.append(start_name)
		answer_dict['answer'] = answer_name
		answer_dict['list'] = answer_list

		if len(answer_name) == 0:
			return []

		return answer_dict

	# 8:nnt 参演评分大于 x
	def actor_gt_rate_movie(self, name, rate):
		answer = self.graph.run(
			"MATCH (m:Movie)-[rel:ACTOR]->(p:Person) where m.rate>$rate and p.name=$name return rel", rate=rate, name=name).data()

		answer_dict = {}
		answer_name = []
		answer_list = []
		for an in answer:
			result = {}
			rel = an['rel']
			relation_type = list(rel.types())[0]
			start_name = rel.start_node['name']
			end_name = rel.end_node['name']
			result["source"] = {'name': start_name}
			result['type'] = relation_type
			result['target'] = {'name': end_name}
			answer_list.append(result)
			answer_name.append(start_name)
		answer_dict['answer'] = answer_name
		answer_dict['list'] = answer_list

		if len(answer_name) == 0:
			return []

		return answer_dict

	# 9:nnt 参演评分小于 x
	def actor_lt_rate_movie(self, name, rate):
		answer = self.graph.run(
			"MATCH (m:Movie)-[rel:ACTOR]->(p:Person) where m.rate<$rate and p.name=$name return rel", rate=rate,
			name=name).data()

		answer_dict = {}
		answer_name = []
		answer_list = []
		for an in answer:
			result = {}
			rel = an['rel']
			relation_type = list(rel.types())[0]
			start_name = rel.start_node['name']
			end_name = rel.end_node['name']
			result["source"] = {'name': start_name}
			result['type'] = relation_type
			result['target'] = {'name': end_name}
			answer_list.append(result)
			answer_name.append(start_name)
		answer_dict['answer'] = answer_name
		answer_dict['list'] = answer_list

		if len(answer_name) == 0:
			return []

		return answer_dict

	# 10:nnt 电影类型
	def actor_movie_category(self, name):
		answer = self.graph.run(
			"match (m:Movie)-[:ACTOR]->(p:Person{name:$name}) return p.name as name, m.category as category", name=name).data()

		answer_dict = {}
		answer_name = []
		answer_list = []
		movie_cat_set = set()
		name = ''
		for an in answer:
			name = an['name']
			category = an['category']
			category = category.split(';')
			for cat in category:
				movie_cat_set.add(cat)

		for cat in movie_cat_set:
			result = {}
			relation_type = '出演的电影风格'
			start_name = name
			end_name = cat

			result["source"] = {'name': start_name}
			result['type'] = relation_type
			result['target'] = {'name': end_name}
			answer_list.append(result)
			answer_name.append(end_name)

		answer_dict['answer'] = answer_name
		answer_dict['list'] = answer_list

		if len(answer_name) == 0:
			return []

		return answer_dict

	# 11:nnt nnr合作电影列表
	def actor_actor_movie(self, name1, name2):
		answer = self.graph.run(
			"match (p:Person{name:$pname})<-[rel1:ACTOR]-(m:Movie)-[rel2:ACTOR]->(other:Person{name:$oname}) return rel1, rel2", pname=name1,
			oname=name2).data()

		answer_dict = {}
		answer_name = []
		answer_list = []
		for an in answer:
			result = {}
			rel = an['rel1']
			relation_type = list(rel.types())[0]
			start_name = rel.start_node['name']
			end_name = rel.end_node['name']
			result["source"] = {'name': start_name}
			result['type'] = relation_type
			result['target'] = {'name': end_name}
			answer_list.append(result)
			answer_name.append(start_name)

			rel2 = an['rel2']
			relation_type2 = list(rel2.types())[0]
			start_name2 = rel2.start_node['name']
			end_name2 = rel2.end_node['name']
			result2 = {}
			result2["source"] = {'name': start_name2}
			result2['type'] = relation_type2
			result2['target'] = {'name': end_name2}
			answer_list.append(result2)

		answer_dict['answer'] = answer_name
		answer_dict['list'] = answer_list

		if len(answer_name) == 0:
			return []

		return answer_dict

	# 12:nnt 电影数量
	def actor_movie_count(self, name):
		answer = self.graph.run(
			"match (m:Movie)-[:ACTOR]->(p:Person) where p.name = $name return p.name as name, count(m) as count",
			name=name).data()
		answer_dict = {}
		answer_name = []
		answer_list = []
		for an in answer:
			result = {}
			relation_type = '电影数量'
			start_name = an['name']
			end_name = an['count']
			result["source"] = {'name': start_name}
			result['type'] = relation_type
			result['target'] = {'name': str(end_name)}
			answer_list.append(result)
			answer_name.append(str(end_name) + ' 部')
		answer_dict['answer'] = answer_name
		answer_dict['list'] = answer_list

		if len(answer_name) == 0:
			return []

		return answer_dict

	# 13:nnt 出生日期(暂时没数据)
	def movie_info(self, name):
		pass

	# 14:评分大于x电影
	def gt_rate_movie(self, rate):
		answer = self.graph.run(
			"MATCH (m:Movie) where m.rate>$rate return m.name as name, m.rate as rate", rate=rate,).data()

		answer_dict = {}
		answer_name = []
		answer_list = []
		for an in answer:
			result = {}
			relation_type = '评分'
			start_name = an['name']
			end_name = an['rate']
			result["source"] = {'name': start_name}
			result['type'] = relation_type
			result['target'] = {'name': end_name}
			answer_list.append(result)
			answer_name.append(start_name)
		answer_dict['answer'] = answer_name
		answer_dict['list'] = answer_list

		if len(answer_name) == 0:
			return []

		return answer_dict

	# 15:评分大于x的ng类型电影
	def gt_rate_category_movie(self, rate, category):
		answer = self.graph.run(
			"MATCH (m:Movie) where m.rate>$rate and m.category =~'.*category.*' return m.name as name, m.rate as rate, m.category as category", rate=rate, category=category).data()

		answer_dict = {}
		answer_name = []
		answer_list = []
		for an in answer:
			result = {}
			relation_type = '评分'
			start_name = an['name']
			end_name = an['rate']
			result["source"] = {'name': start_name}
			result['type'] = relation_type
			result['target'] = {'name': end_name}
			answer_list.append(result)
			answer_name.append(start_name)

			result = {}
			relation_type_2 = '类型'
			end_name_2 = an['category']
			result["source"] = {'name': start_name}
			result['type'] = relation_type_2
			result['target'] = {'name': end_name_2}
			answer_list.append(result)

		answer_dict['answer'] = answer_name
		answer_dict['list'] = answer_list

		if len(answer_name) == 0:
			return []
		return answer_dict
