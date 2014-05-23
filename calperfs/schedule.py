shows=[{'show':'Test', 'date':5,'time':{'HM':[12,16],'AHM':[12,16],'Usher':[12,16]}, 'numberOfStaff':{'HM':1,'AHM':1,'Usher':5},'location':'Zellerbach Auditorium','FOH Lead':'Rob Bean','start':14,'available':[[],[],[]]},
	   {'show':'Test2','date':6,'time':{'HM':[12,16],'AHM':[12,16],'Usher':[12,16]}, 'numberOfStaff':{'HM':1,'AHM':1,'Usher':5},'location':'Zellerbach Playhouse','FOH Lead':'Patrick Hennessey','start':15,'available':[[],[],[]]}]

students=[{'name':'Jessica Allen', 'weekly':{'Monday':'[[10,12],[16,20]]','Tuesday':'[]','Wednesday':'[]','Thursday':'[]','Friday':'[]','Saturday':'[]','Sunday':'[]'}, 'not':[1,7,28],'except':[[5,7,16],[30,8,15]],'max':'AHM','shows':0},
		  {'name':'Max Vale', 'weekly':{'Monday':'[[16,20]]','Tuesday':'[]','Wednesday':'[]','Thursday':'[]','Friday':'[]','Saturday':'[]','Sunday':'[5,4]'}, 'not':[1,7,28],'except':[[5,7,16],[30,8,15]],'max':'HM','shows':0}]
dayOne='Monday'

def getDay(number):
	week=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
	addition={'Sunday':6,'Monday':0,'Tuesday':1,'Wednesday':2,'Thursday':3,'Friday':4,'Saturday':5}
	return week[(number+addition[dayOne]) % 7]

def timeIncludedInTime( timeOne, timeTwo):
	a=timeOne[0]
	b=timeOne[1]
	c=timeTwo[0]
	d=timeTwo[1]
	if (a>=c and b<=d):
		return True
	else:
		return False

def timeIncludedInDay(time, day):
	for item in day:
		if timeIncludedInTime(time, item):
			return true
	return false

def timeIncludedInNot(date, time, notList):
	for item in notList:
		if (notList[0] is date) and timeIncludedInTime(time, [notList[1],notList[2]]):
			return true
	return false

def available(show, student, role):
	if (show['date'] in student['not']):
		return False
	elif timeIncludedInNot(show['date'], show['time'][role], student['not']):
		return False
	elif timeIncludedInDay(show['time'][role],student['weekly'][getDay(show['date'])]):
		return True
	else:
		return False

def allStudentsAvailableHM(show, students):
	answer=[]
	for item in students:
		if item['max'] is 'HM':
			if available(show, item, 'HM'):
				answer.append(item)
	return answer

def allStudentsAvailableAHM(show, students):
	answer=[]
	for item in students:
		if (item['max'] is 'HM') or (item['max'] is 'AHM'):
			if available(show, item, 'AHM'):
				answer.append(item)
	return answer

def allStudentsAvailableUsher(show, students):
	answer=[]
	for item in students:
		if available(show, item, 'Usher'):
			answer.append(item)
	return answer

def allStudentsAvailable(show, students):
	return [allStudentsAvailableHM(show, students),allStudentsAvailableAHM(show, students),allStudentsAvailableUsher(show, students)]

def updateStudent(show, student, role):
	student['not']=student['not'].append(show['date'], show['time']['role'][0],show['time']['role'][1])
	student['shows']=student['shows']+1



import unittest

class Test(unittest.TestCase):
	def getDayTest1(self):
		dayOne='Monday'
		self.assertEqual('Monday',getDay(1))

