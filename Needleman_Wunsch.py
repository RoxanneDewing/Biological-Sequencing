import numpy as np


#This is a recursive TraceBack for NeedleMen Wunsch, it explores every path back to F(0, 0)
def TraceBack_Wunsch(i, j, n, m, temp_n, temp_m, arr, lst):
	if (i==0 and j==0): 
		return lst.append([temp_n, temp_m])
	if (i==0):
		TraceBack_Wunsch(i, j-1, n, m, "-"+temp_n, m[j-1]+temp_m, arr, lst)
	if (j==0): 
		TraceBack_Wunsch(i-1, j, n, m, n[i-1]+temp_n, "-"+temp_m, arr, lst)
	Case_Match = (arr[i][j] == arr[i-1][j-1] + Score(n[i-1], m[j-1]))
	Case_GapX = (arr[i][j] == arr[i][j-1] - 2)
	Case_GapY = (arr[i][j] == arr[i-1][j] - 2)
	if(Case_Match):
		TraceBack_Wunsch(i-1, j-1, n, m, n[i-1]+temp_n, m[j-1]+temp_m, arr, lst)
	if(Case_GapX):
		TraceBack_Wunsch(i, j-1, n, m, "-"+temp_n, m[j-1]+temp_m, arr, lst)
	if(Case_GapY):
		TraceBack_Wunsch(i-1, j, n, m, n[i-1]+temp_n, "-"+temp_m, arr, lst)
	
	return lst

	
#This is a helper function that returns the score
def Score(i, j):
	if (i==j):
		return 2
	else:
		return -1
#This function will create the matrix using the recurrence relations and also call the
#trace back function once the matrix is complete
#This function also opens all the text files and writes to them
def Needleman_Wunsch(n, m):
	arr = np.zeros((len(n)+1, len(m)+1))
	for i in range(len(n)+1):
		arr[i][0] = -2*i
	for j in range(len(m)+1):
		arr[0][j] = -2*j
	for i_Index in range(1, len(n)+1):
		for j_Index in range(1, len(m)+1):
			Val_one = arr[i_Index-1][j_Index-1]+Score(n[i_Index-1], m[j_Index-1])
			Val_two = arr[i_Index-1][j_Index] -2
			Val_three = arr[i_Index][j_Index-1] -2
			Max = max([Val_one, Val_two, Val_three])
			arr[i_Index][j_Index] = Max

	#Print the max score in file 2.o1
	f = open("2.o1.txt", "w+")
	f.write(str(int(arr[len(n)][len(m)])))
	f.close()
	
	#Print the array in file 2.o2
	f = open("2.o2.txt", "w+")
	newstr = " "
	for h in range(0, len(n)+1):
		for r in range(0, len(m)+1):
			newstr = newstr + " "+str(int(arr[h][r]))
		f.write(newstr.strip()+"\n")
		newstr = " "
	f.close()
	
	lst = TraceBack_Wunsch(len(n), len(m), n, m, "", "", arr, [])
	
	#Print an alignment
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
	
	#print all alignments - Bonus
	f = open("2.o5.txt", "w+")
	f.write(str(len(lst)))
	for g in range(0, len(lst)):
		f.write("\n")
		f.write(str(lst[g][0]) + "\n" )
		f.write(str(lst[g][1]) + "\n")
	f.close()
	
	#print(lst)
	
#This is a main function , only used to call NeedleMan_Wunsch with input sequences from 2.in file
def main():
	file = open("2.in.txt", 'r')
	x = file.readline().strip().upper()
	y = file.readline().strip().upper()
	file.close()
	Needleman_Wunsch(x, y)
if __name__== "__main__":
	main()