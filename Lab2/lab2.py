# 1. numoy array and some operations
import numpy as np
a=eval(input("Enter array of numbers:"))
print("Array:",a)
print("maximum:",np.max(a))
print("minimum:",np.min(a))
print("mean:",np.mean(a))

#2.accessing elements
import numpy as np
x=np.array([10,20,30,40,50])
print("The third element in the array is:",x[2])
print("The first three elements of array are:",x[0:3])
x[2]=35
print("The updated array is:",x)

#3.operations on matrix
import numpy as np
y=np.array([[1,2,3],[4,5,6],[7,8,9]])
print("the shape of the specified array is",np.shape(y))
print("The sum of array is",np.sum(y))
print("the sum of rows :",np.sum(y,axis=1))

#4.
import numpy as np
z=np.array([[1,2,3],[4,5,6],[7,8,9]])
print(z[1,1])
print("The last column is:",z[:,2])
print("The second row is:",z[1,:])