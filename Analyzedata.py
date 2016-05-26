import sys, getopt
inputFile=''
outputFile=''
byteOffset=0
def read_in_chunks(file, chunk_size):
    #"""Lazy function (generator) to read a file piece by piece.
    #Default chunk size: 1k."""
	#file_object=open('G:\\Wholedata2.txt','r')
	print file
	file_object=open(str(file),'r')
	while True:
		data = file_object.read(chunk_size)
		if not data:
			break
		yield data	
	#for piece in read_in_chunks(f):
   # process_data(piece)

def ProcessData():
	Lastline=''
	PreviousCollege=''
	PreviousCourse=''
	print inputFile
	DataDictionary={'College':'' ,'estd':0,'Course':'','malecount':0, 'femalecount':0, 'maleplaced':0, 'femaleplaced':0, 'avggpa':0.0, 'avgmalegpa':0.0, 'avgfemalegpa':0.0, 'year':0}
	WriteDictionaryHeaderToFile(DataDictionary,'G:\\analyzedData.txt')
	for dataChunk in read_in_chunks(inputFile,4096):
		lines=dataChunk.split('\n')
		if(Lastline!=''):
			lines[0]=Lastline+lines[0]
		if(dataChunk.endswith('\n')|dataChunk.endswith('\r')):
			Lastline=''			
		else:
			Lastline=lines[len(lines)-1]
		lines.pop()
		for line in lines:
			print line
			columns=line.split(',')
			if(columns[0]==PreviousCollege):
				if(columns[2]==PreviousCourse):
					DataDictionary['avggpa']=float(DataDictionary['avggpa'])+float(columns[7])
					if(columns[3]=='M'):
						DataDictionary['malecount']+=1
						DataDictionary['avgmalegpa']=float(DataDictionary['avgmalegpa'])+float(columns[7])
						if(columns[8]=='1'):
							DataDictionary['maleplaced']+=1
					elif(columns[3]=='F'):
						DataDictionary['femalecount']+=1
						DataDictionary['avgfemalegpa']=float(DataDictionary['avgfemalegpa'])+float(columns[7])
						if(columns[8]=='1'):
							DataDictionary['femaleplaced']+=1

				else:
					WriteDictionaryToFile(calculateAverage(DataDictionary),'G:\\analyzedData.txt')
					PreviousCourse=columns[2]
					DataDictionary['year']=columns[6]
					DataDictionary['Course']=columns[2]
					DataDictionary['avggpa']=columns[7]
					if(columns[3]=='M'):
						DataDictionary['malecount']=1
						DataDictionary['avgmalegpa']=columns[7]
						DataDictionary['femalecount']=0
						DataDictionary['avgfemalegpa']=0.0
						if(columns[8]=='1'):
							DataDictionary['maleplaced']=1
							DataDictionary['femaleplaced']=0
					elif(columns[3]=='F'):
						DataDictionary['femalecount']=1
						DataDictionary['avgfemalegpa']=columns[7]
						DataDictionary['malecount']=0
						DataDictionary['avgmalegpa']=0.0
						if(columns[8]=='1'):
							DataDictionary['femaleplaced']=1
							DataDictionary['maleplaced']=0
					
			else:
				if(DataDictionary['estd']!=0):
					WriteDictionaryToFile(calculateAverage(DataDictionary),'G:\\analyzedData.txt')
				DataDictionary['College']=columns[0]
				DataDictionary['Course']=columns[2]
				DataDictionary['estd']=columns[1]
				DataDictionary['avggpa']=columns[7]
				DataDictionary['year']=columns[6]
				if(columns[3]=='M'):
					DataDictionary['malecount']=1
					DataDictionary['avgmalegpa']=columns[7]
					DataDictionary['femalecount']=0
					DataDictionary['avgfemalegpa']=0.0
					if(columns[8]=='1'):
						DataDictionary['maleplaced']=1
						DataDictionary['femaleplaced']=0
				elif(columns[3]=='F'):
					DataDictionary['femalecount']=1
					DataDictionary['avgfemalegpa']=columns[7]
					DataDictionary['malecount']=0
					DataDictionary['avgmalegpa']=0.0
					if(columns[8]=='1'):
						DataDictionary['femaleplaced']=1
						DataDictionary['maleplaced']=0
				PreviousCollege=columns[0]
				PreviousCourse=columns[2]
			#print DataDictionary
		#WriteDictionaryToFile(DataDictionary,'G:\\analyzedData.txt')

def WriteDictionaryToFile(Dictionary, Filename):
	f = open(Filename,"a")
	for key,value in Dictionary.items():
		f.write(str(value)+',')
	f.write('\n')
	f.close()

def WriteDictionaryHeaderToFile(Dictionary, Filename):
	f = open(Filename,"a")
	for key,value in Dictionary.items():
		f.write(str(key)+',')
	f.write('\n')
	f.close()
	
def calculateAverage(dictionary):
	dictionary['avggpa']=round(float(dictionary['avggpa'])/int(dictionary['malecount']+dictionary['femalecount']),1)
	if(int(dictionary['malecount'])>0):
		dictionary['avgmalegpa']=round(float(dictionary['avgmalegpa'])/int(dictionary['malecount']),1)
	if(int(dictionary['femalecount'])>0):
		dictionary['avgfemalegpa']=round(float(dictionary['avgfemalegpa'])/int(dictionary['femalecount']),1)
	return dictionary
	

def CmdLineArgs(argv):
   global inputFile
   global outputFile
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'Analyzedata.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-help':
         print 'Analyzedata.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputFile = arg
      elif opt in ("-o", "--ofile"):
         outputFile = arg


CmdLineArgs(sys.argv[1:])
ProcessData()
