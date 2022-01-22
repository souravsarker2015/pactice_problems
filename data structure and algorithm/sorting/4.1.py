def insertion(array):
    for i in range(len(array)):
        j=i
        while j>0 and array[j-1]>array[j]:
            array[j-1],array[j]=array[j],array[j-1]
            j -=1

if __name__=="__main__":
    array=[2,5,2,4,7]
    insertion(array)
    print(array)