import sys
import os 
import re
import copy
import itertools
for inputs in range(len(sys.argv)):
	index_loco=sys.argv[1]+'inverted_index.txt'
	num_docs=int(sys.argv[2])
	weight= float(sys.argv[3])
	query= sys.argv[4:]
for word in query:
	#print word
	query=map(lambda word:word if word =='AND' or word =='OR' else word.lower(),query)
	

op=open(index_loco, 'r')
read_some=op.readlines()
#print read_some

index = {}
words = []
master = []
docs = []
pos = []
docIndex = {}
docs2 = []
docs3 = []
def score_word(list):
	top=0

	while top < num_docs and top<(len(score_doc)) :
		print score_doc[top][0],score_doc[top][1]
		top +=1
	return

def one_word(query):
	body_docs_contain=[]
	title_docs_contain=[]
	score_doc=[]
	for word in query:
		term = word
	for key, value in docIndex.iteritems():
		if key == term:
			body_docs_contain = value
		elif key=="title."+term:
			title_docs_contain=value
	for title in title_docs_contain:
		title_value=1*weight
		if title in body_docs_contain:
			total= title_value + (1-weight)*1
			score_doc.append((title, total))
		else:
			total=title_value

			score_doc.append((title, total))
	for words in body_docs_contain:
		if words not in title_docs_contain:
			word_score=1*(1-weight)
			score_doc.append((words, word_score))
	#print score_doc
	#print sorted(score_doc, key = lambda row: (-int(row[1]), row[0]))
	score_doc=sorted(score_doc, key=lambda x: x[1],reverse=True)
	#print score_doc
	#print score_doc



	
		 
	#print score_doc

	return score_doc
with open(index_loco, 'r') as f:
	for line in f:
		master.append(line.split("\t"))

for value in range(len(master)-1):
	#print master[value][0]
	#print(master[value][1])
	words.append(master[value][0])
	docs.append(master[value][1])

for value in docs:
	L = value.split(";")
	L.pop(len(L)-1)
	docs2.append(L)

'''
for value in docs2:
	print value
	for i in value:
'''
class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)
     def show(self):
     	print self.items

def convertPrefix(infix):

	listInfix = list(infix)
	tempInfix = []
	#print listInfix
	needsClose = False
#	for value in listInfix:
#		if value


	precedence = {"AND":1, "OR":1, ")":0}
	excludes = ["AND","OR", "(", ")"]
	includes = []

	temp = []
	opstack = Stack()
	sol = []
	for value in listInfix:
		
		if value == ')' :
			temp.append(" )")
		elif value == '(':
			temp.append("( ")
		else:
			temp.append(value)

	
	#print temp
	temp = "".join(temp)
	#print "is this temp", temp
	split_infix = temp.split()

	#print includes
	#print split_infix

	signal = False
	start = 0 
	finish = 0
	subword = []
	ranges = []
	tempSplit  = []
	forbodenTerms  = []
	for value in range(len(split_infix)):
		if split_infix[value][0] =='"':
			#print split_infix[value]
			start = value
			currentphrase = []
			for value in range(value, len(split_infix)):
				forbodenTerms.append(value)
				currentphrase.append(split_infix[value])
				if split_infix[value][len(split_infix[value])-1] =='"':
					break
			currentphrase = " ".join(currentphrase)
			tempSplit.append(currentphrase[1:-1])
			#print forbodenTerms

		if value not in forbodenTerms:
			tempSplit.append(split_infix[value])
		#forbodenTerms = []
	#print tempSplit
	split_infix = tempSplit
	for value in split_infix:
		if value not in excludes:
			includes.append(value)

	split_infix.reverse()
	#print split_infix

	#print split_infix
	for val in split_infix:
		if val in includes:
			sol.append('('+val+')')
		elif val == "(":
			top_val = opstack.pop()
			#print "final part"
			#print sol
			#opstack.show()
			while top_val != ")" :
				sol.append("'"+top_val+"'")
				top_val = opstack.pop()
			sol.append("(")

		elif val == ")":
			sol.append(")")
			opstack.push(val)

		else:
			#print "issue is here", val
			while (not opstack.isEmpty() and precedence[opstack.peek()] >= precedence[val]):
				sol.append("'"+opstack.pop()+"'")
			opstack.push(val)
		#print sol
		#print("opstack")
		#opstack.show()
	while not opstack.isEmpty():
		sol.append("'"+opstack.pop()+"'")
	sol.reverse()
	#print sol
	final_sol = []

	for val in range (len(sol)-1):
		if sol[val] == "(":
			sol[val+1] =  "(" +  sol[val+1]

		elif sol[val + 1] ==")":
			sol[val] = sol[val] + ")"

	for val in sol:
		if val not in [")","("]:
			final_sol.append(val)
	final_sol[0] = "("+final_sol[0]
	final_sol[len(final_sol)-1] = final_sol[len(final_sol)-1] +")"
	final_sol = ",".join(final_sol)
	print final_sol






	return final_sol

#def deep_get(dictionary, *keys):
    #return reduce(lambda d, key: d.get(key, None) if isinstance(d, dict) else None, keys, dictionary)
def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)
def the_decider(l, subLen):
	print l.sort()
def handle_phrase(query):
	#body of text
	#print query
	#print query
	x=[]
	new_d={}
	queryLen = len(query)
	for term in query:

		#print term
		x.append(posIndex.get(term,{}).keys())
		result = set(x[0]).intersection(*x)
		new_result=list(result)
	#print new_result

	for value in query:
		for key,item in posIndex.get(value,{}).items():
			if key in new_result:
				#print value,key,item
				if key not in new_d:
					new_d[key] = item
				else:
					new_d[key] = natural_sort(list(new_d[key] + natural_sort(item)))
					#new_d[key].sort()
	
	#for i in new_result:
		#the_decider(new_d[i],queryLen)
		#print   i, new_d[i]
	#print new_d
	for it,stuff in new_d.iteritems():
		stuff=filter(lambda a: a != '', stuff)
		new_d[it]=stuff

	from itertools import groupby
	from operator import itemgetter
	body_docs=[]
	bod_score=[]
	for keys, item in new_d.iteritems():
		#print item
		item= map(int, item)
		for k, g in groupby(enumerate(item), lambda (i, w): i-w):
		     tupler =(keys, map(itemgetter(1), g))
		     #print tupler
		     if len(tupler[1])==len(query):
		     	body_docs.append(tupler)
		     

		#print [item[i:i+len(query)] for i in range(0, len(item), len(query))]    
	#print new_d

	for things in body_docs:
		bod_score.append(things[0])
	#print body_docs
	#print bod_score
	#



	
	return bod_score

def score_phrase(body,title):
	scorer=[]
	if not body:
		for item in title:
			title_val=1*weight
			scorer.append((item,title_val))
			scorer=sorted(scorer, key=lambda x: x[1],reverse=True)
			top=0
			while top < num_docs and top<(len(scorer)):
				print scorer[top][0],scorer[top][1]
				top+=1

	elif not title:
		for val in body:
			bod_val=1-(weight)
			scorer.append((val,bod_val))
			scorer=sorted(scorer, key=lambda x: x[1],reverse=True)
			top=0
			while top < num_docs and top<(len(scorer)):
				print scorer[top][0],scorer[top][1]
				top+=1
	else:
		for titles in title:
			title_value=1*weight
			if titles in body:
				total= title_value + (1-weight)*1
				scorer.append((titles, total))
			else:
				total=title_value
				scorer.append((titles,total))
		for words in body:
			if words not in title:
				word_score=1*(1-weight)
				scorer.append((words, word_score))
		scorer=sorted(scorer, key=lambda x: x[1],reverse=True)

		top=0

		while top < num_docs and top<(len(scorer)) :
			print scorer[top][0],scorer[top][1]
			top +=1

		#print score_doc
	return
	#else:


posIndex = {}
tempIndex = {}
for i in range(len(docs2)):
	#print words[i], docs2[i]
	docIndex[words[i]] = []

	for j in docs2[i]:
		temp = j.split(":")
		docIndex[words[i]].append(temp[0])
		tempIndex[temp[0]] = temp[1].split(",")
	#print words[i]
	#print tempIndex 
	posIndex[words[i]] = tempIndex.copy()
	tempIndex.clear()
#print posIndex
if len(query)==0:
	print 'No query to process'


elif len(query) == 1 and not len(query[0].split()) >1:
	score_doc=one_word(query)
	score_word(score_doc)

elif len(query) > 1 and 'AND' not in query and 'OR' not in query :
	#print query

	phrase_list=handle_phrase(query)
	title_query=["title." + element for element in query]
	#print title_query

	title_list=handle_phrase(title_query)
	#print title_list
	#print phrase_list
	score_phrase(phrase_list,title_list)
	#print phrase_list

elif query[len(query)-1]== 'AND' or query[len(query)-1]=='OR':
	print 'ILL DEFINED'
elif len(query) == 3 and 'AND' in query:

	lister=[]
	listo=[]
	lister.append(query[0])
	listo.append(query[2])
	a=one_word(lister)
	b=one_word(listo)
	#print a
	#print b
	for element in a:
		for thing in b:

			if element[0]==thing[0]:

				print element[0],element[1]
elif len(query) == 3 and 'AND' in query:

	lister=[]
	listo=[]
	lister.append(query[0])
	listo.append(query[2])
	a=one_word(lister)
	b=one_word(listo)
	#print a
	#print b
	for element in a:
		for thing in b:

			if element[0]==thing[0]:
				print element[0],element[1]
elif len(query) == 3 and 'OR' in query:

	lister=[]
	listo=[]
	lister.append(query[0])
	listo.append(query[2])
	a=one_word(lister)
	b=one_word(listo)
	#print a
	#print b
	for value in b:
		a.append(value)
	score_doc=a
	score_word(score_doc)
elif len(query) == 3 and 'OR' in query and ' ' in query[0]:

	lister=[]
	listo=[]
	lister.append(query[0])
	listo.append(query[2])
	a=(lister)
	b=one_word(listo)
	#print a

	#print b
	for value in b:
		a.append(value)
	score_doc=a
	score_word(score_doc)

	
	#print listo
elif len(query) > 1 and 'AND' in query or 'OR'  in query :

	process=' '.join(query)
	print process

	convertPrefix(process)

#x=posIndex.get('the', {}).get('doc_2') 
#print x
#if int(x[0])>7:

