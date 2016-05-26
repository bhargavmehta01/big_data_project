#import array.*
from __future__ import print_function
from array import array
import random
#reads selected data from files to dictionary by column names
Cources={}
def Load_CSVTODICTionary(FileName,Columns):
	results = {}
	DataColumns=Columns.split(",")
	with open(FileName, "r") as cache:
		# read file into a list of lines
		lines = cache.readlines()        
		# loop through lines
		results[0]=Columns
		LineNumber=0
		expression=""
		DataColumns_Index = array("i",[])
		for line in lines:
			line=line.strip()
			#print LineNumber
			if(LineNumber==0):
				FileColumns=line.split(",")
				for DataColumn in DataColumns:
					count=0
					for column in FileColumns:
						if(column==DataColumn):
							expression=expression + "line["+str(count)+"]+\",\"+"
							DataColumns_Index.append(count)
							break
						count=count+1
				LineNumber=LineNumber+1
				expression=expression[:-5]
				continue
			line = line.split(",")
			# use first item in list for the key, join remaining list items
			# with ", " for the value.
			exec("results[LineNumber] = "+expression)
			LineNumber=LineNumber+1
	return results

def GenerateRandomName(FirstNameList,LastNameList,StudentsCount):
	studentnames={}
	for count in range(0,StudentsCount):
		lastname = random.randint(1,len(LastNameList)-1)
		firstname = random.randint(1,len(FirstNameList)-1)
		studentnames[count]=FirstNameList[firstname].replace(",",":")+":"+LastNameList[lastname]
	return studentnames
		
def WriteDictionaryToFile(Dictionary, Filename):
	f = open(Filename,"a")
	for count in range(0,len(Dictionary)-1):
		f.write(Dictionary[count]+"\n")
	f.close()
	
def GenerateUniversityData(Names):
	global Cources
	Cources=Load_CSVTODICTionary("Cources.txt","Cources")
	for count in range(0,len(Names)-1):
		Names[count]=Names[count]+":"+str(random.randint(1850,2010))+":"+GenerateCources()
	return Names
	
def GenerateCources():
#	NumberOfCources=random.randint(1,9)
	global Cources
	CourceList=""
	Strength=""
	for count in range(1,random.randint(4,9)):
		CourceAdded = 0
		while CourceAdded == 0:
			subject=Cources.values()[random.randint(1,len(Cources)-1)]
			if(subject not in CourceList):
				CourceList=CourceList+subject+","
				CourceAdded=1
		Strength=Strength+str(random.randint(15,30))+","
	return CourceList[:-3]+":"+Strength[:-1]
	
def ChunkToArray(Data,Delimiter,Data_last):
	Data_lines=Data.split(Delimiter)
	#if(len(Data_lines)==0):
		#break
	#else:
	Data_lines[0]=Data_last+Data_lines[0]
	if Data.endswith(Delimiter):
		if len(Data_lines)>1:
			Data_last=Data_lines[len(Data_lines)-1]
			Data_lines.pop()
	else:
		Data_last=Data_lines[len(Data_lines)-1]
		Data_lines.pop()
	return {'lines':Data_lines,'LastLine':Data_last}

	
def GenerateWholeData(StudentFile,CollegeFile,OutputFile,forLastyears):
	S_Data=open(StudentFile,"r")
	C_Data=open(CollegeFile,"r")
	W_Data=open(OutputFile,"a")
	CChunk_last=""
	SChunk_last=""
	SChunk_lines=[]
	while True:
		CChunk=C_Data.read(1024)
		if CChunk=="":
			break
		else:
			Cdata=ChunkToArray(CChunk,"\n",CChunk_last)
			CChunk_lines=Cdata['lines']
			CChunk_last=Cdata['LastLine']
		# CChunk_lines=CChunk.split("\n")
		# if len(CChunk_lines)==0:
			# break
		# else:
			# CChunk_lines[0]=CChunk_last+CChunk_lines[0]
			# if CChunk.endswith("\n"):
				# if len(CChunk_lines)>1:
					# CChunk_last=CChunk_lines[len(CChunk_lines)-1]
					# CChunk_lines.pop()
			# else:
				# CChunk_last=CChunk_lines[len(CChunk_lines)-1]
				# CChunk_lines.pop()		
			for entry in CChunk_lines:
				for year in range(1,forLastyears):
					results={}
					CChunk_linetoColumns= entry.split(":")
					CChunk_lineCources=CChunk_linetoColumns[2].split(",")
					CChunk_lineCource_Strength=CChunk_linetoColumns[3].split(",")
					for count in range(0,len(CChunk_lineCources)-1):
						for strength in range(0,int(CChunk_lineCource_Strength[count-1])):
							if(len(SChunk_lines)>0):
								studentInfo=SChunk_lines[len(SChunk_lines)-1].split(":")
								SChunk_lines.pop()
								results[len(results)]=CChunk_linetoColumns[0]+","+CChunk_linetoColumns[1]+","+CChunk_lineCources[count]+","+studentInfo[1]+","+studentInfo[0]+","+studentInfo[2]+","+ str(2015-year) +","+str(round(random.uniform(2.6,4.0),1))+","+str(random.randint(0,1))
							else:
								SChunk=S_Data.read(4096)
								#if SChunk=="":
									#print "STUDENT NAMES ENDED"
								Sdata=ChunkToArray(SChunk,"\n",SChunk_last)
								SChunk_lines=Sdata['lines']
								SChunk_last=Sdata['LastLine']
								studentInfo=SChunk_lines[len(SChunk_lines)-1].split(":")
								SChunk_lines.pop()
								results[len(results)]=CChunk_linetoColumns[0]+","+CChunk_linetoColumns[1]+","+CChunk_lineCources[count]+","+studentInfo[1]+","+studentInfo[0]+","+studentInfo[2]+","+ str(2015-year)+","+str(round(random.uniform(2.6,4.0),1))+","+str(random.randint(0,1))
					WriteDictionaryToFile(results,OutputFile)

F_Names=Load_CSVTODICTionary("yob2014.txt","name,gender")
L_Names=Load_CSVTODICTionary("app_c.csv","name")
Student_names=GenerateRandomName(F_Names,L_Names,10000000)
WriteDictionaryToFile(Student_names,"G:\\studentlist.txt")
U_Names=Load_CSVTODICTionary("MERGED2012_PP.csv","INSTNM")
College_list=GenerateUniversityData(U_Names)
WriteDictionaryToFile(College_list,"g:\\colleges.txt")
GenerateWholeData("G:\\studentlist.txt","G:\\colleges.txt","G:\\Wholedata2.txt",5)