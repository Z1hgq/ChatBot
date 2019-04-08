import math
def chunks(arr, m):
    n = int(math.ceil(len(arr) / float(m)))
    return [arr[i:i + n] for i in range(0, len(arr), n)]

arr = [1,2,3,4,5,6,7,8,9,0]

print(chunks(arr,2))