a,b,n=[int(n) for n in raw_input().split(" ")]
'''
d=(n-2*a)/(a-b)
l=d*(a-b)
while l+a<n:
    d+=1
    l=l+a-b
d+=1
print d
'''
d = 0
while (n>0):
    d+=1
    n-=a;
    if (n ==0):
        d+=1
        exit
    else:
        n+=b


print d