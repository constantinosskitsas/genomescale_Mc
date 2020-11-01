from kdtree import visualize
from networkx.generators.tests.test_small import null


class suffixTree():

    def __init__(self, input,hello,lcs):
        self.root = Node()
        self.root.depth = 0
        self.root.parent = self.root
        self.root.suffix_link = self.root
        self.root.pos = 0

        if(hello):
            input += "$"
            self.input_text = input
            self.build_McCreight(input)
        else:
            self.input_text = max(input, key=len)
            self.buildTree(input,lcs,self.input_text)

    def findHead(self, u, dep, text, i):
        while u.depth == dep and text[dep + i] in u.transition_links:
            u = u.transition_links[text[dep + i]]
            dep = dep + 1
            while dep < u.depth and text[u.pos + dep] == text[i + dep]:
                dep = dep + 1
        return u, dep

    def build_McCreight(self, text):
        u = self.root
        d = 0
        for i in range(len(text)):
            u, d = self.findHead(u, d, text, i)
            if d < u.depth:
                u = self.create_node(text, u, d)
            self.create_leaf(text, i, u, d)
            if u.suffix_link is None:
                self.compute_slink(text,u)
            u=u.suffix_link
            d = d - 1
            if d < 0:
                d = 0

    def buildTree(self,text,lcp,word):
        u=self.root
        v=Node(pos=len(word)-1,depth=1)
        u.transition_links[word[len(word)-1]]=v
        v.parent=u
        for i in range(1,len(text)):
            u=self.root
            subword=text[i]
            sbd=len(subword)
            sbp=len(word)-sbd
            if (lcp[i-1]==0):
                if(lcp[i]==0):
                    v = Node(pos=sbp, depth=sbd)
                    u.transition_links[word[sbp]]=v
                    v.parent=u
                else:
                    if(lcp[i]==v.depth):
                        v = Node(pos=sbp, depth=sbd - 1)
                        u.transition_links[word[sbp]] = v
                        v.parent = u
                        w=Node(pos=sbp,depth=sbd)
                        v.transition_links[word[sbp+sbd-1]]=w
                        w.parent=v
                    else:
                        v = Node(pos=sbp, depth=sbd)
                        u.transition_links[word[sbp]] = v
                        v.parent = u

            else:
                #print("se eroteftika")
                u=u.transition_links[word[sbp]]
                counter=u.depth
                if(u.depth<lcp[i-1]):
                    u.pos=sbp
                while(u.depth<lcp[i-1]):
                    u=u.transition_links[subword[counter]]
                    counter=counter+u.depth
                    if(u.depth<lcp[i-1]):
                        u.pos=sbp
                if (u.depth==lcp[i-1]):
                    v = Node(pos=sbp, depth=sbd)
                    u.transition_links[word[sbp+lcp[i-1]]]=v
                    v.parent=u
                    if (lcp[i]==sbd-1):
                        d = Node(pos=sbp, depth=sbd)
                        v.transition_links[word[sbp+sbd-1]]=d
                else:
                    p=Node(pos=sbp,depth=lcp[i-1])
                    p.parent=u.parent
                    p.parent.transition_links[word[sbp+p.parent.depth]]=p
                    u.parent=p
                    p.transition_links[word[u.pos+p.depth]]=u
                    v=Node(pos=sbp,depth=sbd)
                    p.transition_links[word[v.pos+lcp[i-1]]]=v
                    v.parent=p

    def create_node(self, x, u, d):
        i = u.pos
        p = u.parent
        v = Node(pos=i, depth=d)
        v.transition_links[x[i + d]] = u
        u.parent = v
        p.transition_links[x[i + p.depth]] = v
        v.parent = p
        return v

    def create_leaf(self, x, i, u, d):
        w = Node()
        w.pos = i
        w.depth = len(x) - i
        u.transition_links[x[i + d]] = w
        w.parent = u
        return w

    def compute_slink(self, x, u):
        d = u.depth
        v = u.parent.suffix_link
        while v.depth < d - 1:
            v = v.transition_links[x[u.pos + v.depth + 1]]
        if v.depth > d - 1:
            v = self.create_node(x, v, d - 1)
        u.suffix_link = v
    def find_pattern(self, pattern):
        node = self.root
        while True:
            edge= self.input_text[node.pos + node.parent.depth: node.pos + node.depth]
            if edge.startswith(pattern):
                break

            i = 0
            while (i < len(edge) and edge[i] == pattern[0]):
                pattern = pattern[1:]
                i += 1

            if i != 0:
                if i == len(edge) and pattern != '':
                    pass
                else:
                    return {}
            if pattern[0] in node.transition_links:

                node = node.transition_links[pattern[0]]
            else:
                return {}
        leaves = node.get_leaves1()
        return {n.pos for n in leaves}

##this function produces the sorted prefix matrix and lcp matrix
    #insted of returning the nodes, we can return the pos by saving it in another matrix and returning the other matrix
    #i added one extra 0 on the end just for LCP and SP matrix to have the same length
    def get_sortedPrefix_and_LCP(self, sort_1):
        def cmp1(a):
            return self.input_text[a.pos]
        res=[]
        temp=[]
        lcp=[]
        testmpe=self.root
        x=list(testmpe.transition_links.values())
        if(sort_1==True):
            x=sorted(x, key=self.numeric_compare2, reverse=True)
        else:
            x.reverse()
        if len(x)==0:
            res.append(self)
            return res
        while(len(x)>0):
            temp.append(x.pop())
            if len(temp[0].transition_links.values())==0:
                res.append(temp[0])
                temp.pop()
                counter=0
                hi=0
                if (len(res)>1):
                    x1=res[-1]
                    temp1 = res[-2].parent
                    temp2 = res[-2]
                    if (x1.parent == temp1 or x1.parent == temp2 )and (x1.parent==self.root or x1==self.root):
                        counter=counter+1
                    while  x1!=self.root:
                        temp2=res[-2]
                        while temp2!=self.root:
                            if(x1!=temp2):
                                temp2=temp2.parent
                            else:
                                counter=x1.depth
                                x1=self.root
                                break
                        x1 = x1.parent

                    lcp.append(counter)
            else:
                if (sort_1==True):
                    temp2 = sorted(temp[0].transition_links.values(), key=self.numeric_compare2, reverse=True)
                else:
                    temp2=list(temp[0].transition_links.values())
                    temp2.reverse()
                for k in (temp2):
                    x.append(k)
                temp.pop()
        lcp.append(0)
        return res,lcp


#numeric_compare can be used only for the way that the tree is created
#it is important to notice that, if we have already sorted construction of tree
#even if the values are the same, if the order that the nodes are created are different
#it will not produce correct results! so when we have it order we just reverse and we can pop from
#the last, i have to improve my skils in python...
    def numeric_compare2(self,x):
        return self.input_text[x.pos]

class Node():
    def __init__(self, pos=-1, parentNode=None, depth=-1):
        self.suffix_link = None
        self.transition_links = {}
        self.depth = depth
        self.parent = parentNode
        self.pos = pos

    def __str__(self):
        return ("SNode: pos:" + str(self.pos) + " depth:" + str(self.depth) +
                " transitons:" + str(list(self.transition_links.keys())))

    def get_leaves1(self):
        res=[]
        temp=[]

        x=list(self.transition_links.values())
        if len(self.transition_links)==0:
            res.append(self)
            return res
        while(len(x)>0):
            temp.append(x.pop(0))
            if len(temp[0].transition_links.values())==0:
                res.extend(temp)
                temp.pop()
            else:
                for k in temp[0].transition_links.values():
                    x.append(k)
                temp.pop()
        return (res)

    def numeric_compare(self,x):
        return self.input_text[x.pos]


