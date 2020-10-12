from kdtree import visualize
from networkx.generators.tests.test_small import null


class suffixTree():

    def __init__(self, input):
        self.root = Node()
        self.root.depth = 0
        self.root.parent = self.root
        self.root.suffix_link = self.root
        self.root.pos = 0
        input += "$"
        self.input_text = input
        self.build_McCreight(input)

    def findHead(self, u, dep, text, i):
        while u.depth == dep and text[dep + i] in u.transition_links:
            u = u.transition_links[text[dep + i]]
            dep = dep + 1
            while dep < u.depth and text[u.pos + dep] == text[i + dep]:
                dep = dep + 1
        return u, dep

    def build_McCreight(self, text):
        print("hi")
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
        print(node)
        while True:
            edge= self.input_text[node.pos + node.parent.depth: node.pos + node.depth]
            if edge.startswith(pattern):
                print("jo")
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



class Node():
    def __init__(self, pos=-1, parentNode=None, depth=-1):
        self.suffix_link = None
        self.transition_links = {}
        self.depth = depth
        self.parent = parentNode
        self.pos = pos


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


