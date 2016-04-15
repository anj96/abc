a = int(raw_input('\n'))
fact = 1
for i in range(0,(a-1)):
    fact *=(a-i)
print fact

x=0
while (fact%10==0):
    fact/=10
    x+=1



print x
