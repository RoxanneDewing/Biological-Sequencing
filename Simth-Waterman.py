#Roxanne Dewing



import numpy as np


#This is a recursive TraceBack for SmithWaterman, it explores every path from the highest scores to  when it reaches a 0
def TraceBack_Waterman(i, j, n, m, temp_n, temp_m, arr, lst):
	if (arr[i][j] == 0):
		#print(lst)
		return lst.append([temp_n, temp_m])
		
	Case_Match = (arr[i][j] == arr[i-1][j-1] + Score(n[i-1], m[j-1]))
	Case_GapX = (arr[i][j] == arr[i][j-1] - 2)
	Case_GapY = (arr[i][j] == arr[i-1][j] - 2)
	if(Case_Match):
		TraceBack_Waterman(i-1, j-1, n, m, n[i-1]+temp_n, m[j-1]+temp_m, arr, lst)
	if(Case_GapX):
		TraceBack_Waterman(i, j-1, n, m, "-"+temp_n, m[j-1]+temp_m, arr, lst)
	if(Case_GapY):
		TraceBack_Waterman(i-1, j, n, m, n[i-1]+temp_n, "-"+temp_m, arr, lst)
	
	return lst

	
#This is a helper function that returns the score
def Score(i, j):
	if (i==j):
		return 2
	else:
		return -1


#This function will create the matrix using the recurrence relations and also call the
#trace back function once the matrix is complete
#This function also opens all the text files and writes to them in the specified format
def Smith_Waterman(n, m):
	arr = np.zeros((len(n)+1, len(m)+1))
	for i in range(len(n)+1):
		arr[i][0] = 0
	for j in range(len(m)+1):
		arr[0][j] = 0
	for i_Index in range(1, len(n)+1):
		for j_Index in range(1, len(m)+1):
			Val_one = arr[i_Index-1][j_Index-1]+Score(n[i_Index-1], m[j_Index-1])
			Val_two = arr[i_Index-1][j_Index] -2
			Val_three = arr[i_Index][j_Index-1] -2
			Max = max([Val_one, Val_two, Val_three, 0])
			arr[i_Index][j_Index] = Max
	#Print the max score
	f = open("2.o1.txt", "w+")
	maxval = np.amax(arr)
	f.write(str(int(maxval)))
	f.close()
	
	#Print the array 
	f = open("2.o2.txt", "w+")
	newstr = ""
	for h in range(0, len(n)+1):
		for r in range(0, len(m)+1):
			newstr = newstr + " "+str(int(arr[h][r]))
		f.write(newstr.strip()+"\n")
		newstr = " "
	f.close()
	
	result = np.where(arr == maxval)

	lst = []
	for row in range(len(result)):
		i = result[0][row]
		j = result[1][row]
		newl = TraceBack_Waterman(i, j, n, m, "", "", arr, [])
		lst.extend(newl)

	#Print an alignment in file 2.o3
	f = open("2.o3.txt", "w+")
	f.write(str(lst[0][0]) + "\n" )
	f.write(str(lst[0][1]))
	f.close()
	
	#Print if multiple alignments
	f = open("2.o4.txt", "w+")
	if (len(lst) > 1):
		f.write("YES")
	else:
		f.write("NO")
	f.close()
	
	#Print all the alignments 
	f = open("2.o5.txt", "w+")
	f.write(str(len(lst)))
	for g in range(0, len(lst)):
		f.write("\n")
		f.write(str(lst[g][0]) + "\n" )
		f.write(str(lst[g][1]) + "\n")
	f.close()
	

	
#This is a main function , only used to call Smith waterman with input sequences from 2.in file
def main():
	file = open("2.in.txt", 'r')
	x = file.readline().strip().upper()
	y = file.readline().strip().upper()
	file.close()
	Smith_Waterman(x, y)
if __name__== "__main__":
	main()
	
	
	
	
	
	
	
	