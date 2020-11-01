from McCreight import suffixTree
from McCreight import Node
import time
import pickle
h=suffixTree("mississippi",True,None)
start1 = time.time()
mpe=h.find_pattern("pi")
time_elapsed1 = time.time() - start1
sorted_prefix, lcp_matrix=h.get_sortedPrefix_and_LCP(True)
k=[]
lcs=[]

for i in sorted_prefix:
    k.append(h.input_text[i.pos: i.pos + i.depth])
    print(h.input_text[i.pos: i.pos + i.depth])
for mpo in lcp_matrix:
    lcs.append(mpo)
    print(mpo)
lcs.append(0)
savesp=[]
savelcp=[]
with open('outfile', 'wb') as fp:
    pickle.dump(k, fp)
with open('outfile1', 'wb') as fp:
    pickle.dump(lcp_matrix, fp)
with open ('outfile', 'rb') as fp:
    itemlist = pickle.load(fp)
with open ('outfile1', 'rb') as fp:
    itemlist1 = pickle.load(fp)
d1=suffixTree(itemlist,False,itemlist1)
resmpe1,hohompe1=d1.get_sortedPrefix_and_LCP(False)
for i in resmpe1:
    print(i)
    print(d1.input_text[i.pos: i.pos + i.depth])
for i in hohompe1:
    print(i)


