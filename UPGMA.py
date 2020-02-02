import numpy 


#A Binary tree helper class
class Tree:
	def __init__(self, node, edgeLength, cLength, Left, Right):
		self.node = node
		self.edgeLength = edgeLength
		self.cLength = cLength
		self.Left = Left
		self.Right = Right
	

#this function takes a root of a tree and recursively explores in pre order 
def PreOrder(root):
	if root is None:
		return ''
	else:
		if (root.Left is None):
			return 'S' + root.node +':'+str("{0:0.2f}".format(root.edgeLength))
		else:
			if (root.edgeLength == 0):
				return 'S'+root.node +'(' + PreOrder(root.Left) +')'+ '('+ PreOrder(root.Right)+')'
			return 'S'+root.node +':'+ str("{0:0.2f}".format(root.edgeLength))+'(' + PreOrder(root.Left) +')'+ '('+ PreOrder(root.Right)+')'

#this is a function that finds the distance between two sequences, the sequences 
#may also be different lengths
def Hamming(x, y):
	x = x +'_'
	y = y +'_'
	score = 0
	for i in range(len(x)):
		if(x[i] == '_' or y[i]=='_'):
			return score + abs(len(x) - len(y))
		if(x[i] != y[i]):
			score+=1

#this is a recursive UPGMA algorithm, it takes in a list of Sequence names and the corresponding
#distance matrix and returns the root node of a tree and also a 0 or 1 value (isMore)
#that indicates if there were different trees that could have been made 
def Cluster(SequenceNodes, dist, isMore):
	#base case
	if (len(SequenceNodes) ==2):
	
		nameK =  SequenceNodes[0].node + SequenceNodes[1].node 
		min = dist[0][1]
		SequenceNodes[0].edgeLength = min/2 - SequenceNodes[0].cLength
		SequenceNodes[1].edgeLength = min/2 - SequenceNodes[1].cLength
		NodeK = Tree(nameK, 0, 0, SequenceNodes[0], SequenceNodes[1])
		return NodeK, isMore
	
	
	min = numpy.min(dist)
	tup = numpy.where(dist == min)
	Coord = []

	#this gets rid of symmetric entries in list
	for k in range(len(tup[0])):
		if ([tup[1][k], tup[0][k]]) not in Coord:
			Coord.append([tup[0][k], tup[1][k]])

	
	if (len(Coord) > 1 and isMore == 0):
		isMore = 1

	

	x = Coord[0][0]
	y = Coord[0][1]


	#define new Node (cluster)
	nameK =  SequenceNodes[x].node + SequenceNodes[y].node 
	SequenceNodes[x].edgeLength = min/2 - SequenceNodes[x].cLength 
	SequenceNodes[y].edgeLength = min/2 - SequenceNodes[y].cLength 
	NodeK = Tree(nameK, 0, min/2, SequenceNodes[x], SequenceNodes[y])
		
		
	#Calculate UPGMA distances to new cluster k
	col = numpy.zeros((len(SequenceNodes)-2,1))
	row = numpy.zeros((1, len(SequenceNodes)-1))
	CardX = len(SequenceNodes[x].node)
	CardY = len(SequenceNodes[y].node)
	counter = 0
	for l in range(len(SequenceNodes)):
		if (l==x or l==y):
			continue
		row[0][counter+1] = ((dist[x][l]*CardX) + (dist[y][l]*CardY))/(CardX+CardY)
		col[counter][0] = ((dist[x][l]*CardX) + (dist[y][l]*CardY))/(CardX+CardY)
		counter+=1
	row[0][0] = numpy.inf

		
	#delete clusters
		
	if (x<y):
		del SequenceNodes[x]
		del SequenceNodes[y-1]
	else:
		del SequenceNodes[y]
		del SequenceNodes[x-1]


		

	SequenceNodes.insert(0, NodeK)
	dist = numpy.delete(dist, [x, y], axis=1)
	dist = numpy.delete(dist, [x, y], axis=0)
	dist = numpy.concatenate((col, dist), axis = 1)
	dist = numpy.concatenate((row, dist), axis = 0)

	#recursive call
	return Cluster(SequenceNodes, dist, isMore)

	


	
	
#this function finds the distance matrix, is uses the Hamming function 
def distance(SequenceName, Sequence):
	dist = numpy.zeros((len(Sequence), len(Sequence)))
	for i in range(len(Sequence)):
		for j in range(i, len(Sequence)):
			if (i == j):
				dist[i][j] = numpy.inf
			else:
				dist[i][j] = Hamming(Sequence[i], Sequence[j])
				dist[j][i] = dist[i][j]   #by symmetry
	#print matrix
	f = open("3.o1.txt", "w+")
	f.write('-')
	for i in range(len(SequenceName)):
		f.write(' S' + SequenceName[i])
	f.write('\n')	
	for j in range(len(SequenceName)):
		f.write('S' + SequenceName[j])
		for k in range(len(SequenceName)):
			if (dist[j][k] == numpy.inf):
				f.write(' 0')
			else:
				f.write(' '+str(int(dist[j][k])))
		f.write('\n')
	f.close()
	
	
	SequenceNodes = []
	for x in range(len(SequenceName)):
		a = Tree(SequenceName[x], 0, 0, None, None)
		SequenceNodes.append(a)
	root, isMore = Cluster(SequenceNodes, dist, 0)
	temp = PreOrder(root)
	f = open("3.o2.txt", "w+")
	f.write(temp)
	f.close()
	f = open("3.o3.txt", "w+")
	if (isMore == 1):
		f.write('YES')
	else:
		f.write('NO')
	f.close()
		
	#print(temp)
	
	
#main function, reads in a text file named 3.in.txt
def main():
	file = open("3.in.txt", 'r')
	line = file.readline()
	SequenceName = []
	Sequence = []
	count = 1
	while line:
		if (count %2 == 1):
			SequenceName.append(line.strip()[2:])
			#print(line.strip())	
		else:
			Sequence.append(line.strip())
		line = file.readline()
		count +=1
	file.close()
	distance(SequenceName, Sequence)
	

if __name__ == '__main__':
	main()