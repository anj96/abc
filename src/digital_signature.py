def modInv(a,m) :
    a%=m
    for x in range(1,m):
        if (a*x)%m == 1:
            return x
    return None

p = int(input("p: "))
x = int(input("x: "))
a = int(input("a: "))
d = int(input("d: "))
k = int(input("k: "))
b = (a**d)%p
print (b)
r = (a**k)%p
print (r)
q = modInv(r,(p-1))
s=((x-(d*r))%(p-1)* (q))%(p-1)
print s

