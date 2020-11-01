import itertools

alphabet = "$abcdefghijklmnopqrstuvwxyz"
symbol_map = dict(
  (symb,i)
  for i,symb in enumerate(alphabet)
)

def suffix_bucket(x, i, offset):
    idx = i + offset
    return x[idx] if idx < len(x) else 0

def bucket_sort(x, suffixes, offset):
    buckets = [[] for _ in alphabet]
    counter=0
    for i in suffixes:
        counter=counter+1
        buckets[suffix_bucket(x, i, offset)].append(i)
    return itertools.chain(*buckets)

def radix_sort(x):
    suffixes = range(len(x))
    mapped_x = [symbol_map[symb] for symb in x]
    for offset in range(len(x) - 1, -1, -1):
        suffixes = bucket_sort(mapped_x, suffixes, offset)
    return suffixes

def LCP(res,revres1,T):

    print(res[0])#S
    print(res1[0])#S-1
    l=0
    lcp=[None] * (len(res))
    for i in range(len(T)-1):
        k=revres1[i]
        j=res[k-1]
        while(T[i+l]==T[j+l] and i!=j):
            l=l+1
        lcp[k]=l
        i=i+1
        if(l>0):
            l=l-1
    return lcp
x = 'banana$'
res = radix_sort(x)
res1=[]

for i in res:
    print(i, x[i:])
    res1.append(int(i))

def revers(res1):
    revres1=[None] * (len(res1))
    for i in range(len(res1)):
        revres1[res1[i]]=i
    return revres1
revres1=revers(res1)
lcp_arr=LCP(res1,revres1,x)
for i in (lcp_arr):
    print(i)