def selection(array):
    for i in range(len(array)-1):
        min=i
        for j in range(i+1,len(array)):
            if array[j]<=array[min]:
                min=j
        
        if min!=i:
            array[min],array[i]=array[i],array[min]

if __name__=="__main__":
    x=[4,3,5,1]
    selection(x)
    print(x)