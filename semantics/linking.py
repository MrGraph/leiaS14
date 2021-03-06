from knowledge.lexicon import *
from copy import copy, deepcopy
from itertools import chain


"generates all possible combinations of token-to-sense mapping"
def permutesenses(tokens, lexicon):
    if len(tokens) == 0:
        return [[]]
            
    return [[sense] + senses
            for senses in permutesenses(tokens[1:], lexicon)
            for sense in lexicon[tokens[0]]]


# can use dependencies as heuristic of where to start from


#"generates all possible combinations of how specified instances can be linked via their slots"
#def link(instances):
    #if len(instances) == 0:
        #return [[]]
    
    #return [[do(i, exclude(copy(instances), i), i.slots.keys())] + link(exclude(copy(instances), i))
             #for i in instances]


#def link_each(instances):
    #linkings = []
    
    #for i in filter(lambda i: len(i.slots) > 0, 
                    #instances):
        #linkings.append(link_single(i, exclude(copy(instances), i), i.slots.keys()))
    
    #return linkings

#"generates all possible combinations of filler assignment the to given head instance's slots"
#def link_single(head, filler_concepts, slotnames):
    #if len(filler_concepts) == 0 or len(slotnames) == 0:
        #return head
    
    #return [link_single(branch(head, slotnames[0], Instance(fc)), 
                        #exclude(copy(filler_concepts), fc), 
                        #copy(slotnames)[1:])
            #for fc in filler_concepts]


#def branch(head, slotname, filler):
    
    ##print 'branch %s' % filler
    
    #clone = deepcopy(head)
    #clone.slots[slotname].fill(filler)
    
    #return clone


#def exclude(collection, element):
    #collection.remove(element)
    
    #return collection

#### Below are the function necessary for generate all linking

### access => generate permu of index to generate element of the access
def permu(sizeSlot,sizeFiller,distList=[],access=[]):
    if distList==[]:
        distList=[sizeFiller]*sizeSlot
    return helper(distList,used=[0]*(sizeFiller+1),access=access)

## Generate permu that allows repeat element
def productRule(distList=[]):
    return helper(distList,repeat=True)

def helper(permuList,repeat=False,size=0,used=[0]*100,current=[],access=[]):
    temp = []
    if size == len(permuList):
        return [current]
    for i in range(permuList[size]):
        if repeat:
            temp = temp + helper(permuList,repeat,size+1,used,current+[i])  
        elif used[i]==0:
            used[i]=1
            if access==[]:
                temp = temp +helper(permuList,repeat,size+1,used,current+[i])
            else:
                temp = temp + helper(permuList,repeat,size+1,used,current+[access[i]],access=access)
            used[i]=0
    return temp

### Generate a list of concept except itself
def getRestList(indexOut,size):
    temp = []
    for n in range(size+1):
        if n!=indexOut:
            temp.append(n)
    return temp

#Input = list of the concept 
#Output = list of all possible instance
def findAllLinking(listConcept):
    listInstance = []
    listPermu = []
    ### generate all the combination of the assignment 
    sizeFiller = len(listConcept)-1
    index = 0 
    for Con in listConcept:
        currentList = getRestList(index,sizeFiller)
        sizeSlots = len(Con.slots())
        p = permu(sizeSlots,sizeFiller,access=currentList)
        listPermu += [p]
        index = index+1
    sizeList =[]
    for l in listPermu:
        sizeList.append(len(l))
    ### generate all combination of orders of assignment
    OrderList = productRule(sizeList)

    for i in OrderList:
        #Generate new set of Instance
        InstanceList =[]
        for j in listConcept:
            temp = j()
            InstanceList.append(temp)
        status = True
        for j in range(len(InstanceList)):
            ind = 0
            for slot in InstanceList[j].slots():
                ### Example
                ### [ [[]] , [[0,2]],[2,0]], [[0,1], [1,0]] ]
                ### listPermu[j] -> get the list of permu of j instance
                ### i[j] -> get the number of the possible permu 
                ### ind -> get the slot to be filled
                indexIn = listPermu[j][i[j]][ind] 
                status = status and InstanceList[j].slots()[slot].fill(InstanceList[indexIn])
                ind = ind+1
        if status:
            listInstance.append(InstanceList)
    return listInstance
    
     