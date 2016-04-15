num_array=list()
n = (int(raw_input('\n')))
a = (raw_input())
num_array = list(map(int, a.split(" ")))
flag = 0
for i in range(len(num_array)):
    for j in range(len(num_array)):
        if (num_array[i]%num_array[j]==0 and i!=j):
            flag = 1

    if (flag==0):
        print num_array[i] ,
    flag=0
