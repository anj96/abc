n = int(raw_input('\n'))
for _ in range(n):
    x = raw_input()
    num_array = list(map(int, x.split()))
for i in range(0,n):
    sum = 0
    sum = (num_array[i]*(num_array[i]+1))/2
    sum = (2**(num_array[i]-1))*sum
    print sum
