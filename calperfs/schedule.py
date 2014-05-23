__author__ = 'Jessica'

def getDay(dayOne, number):
	week=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
	addition = {'Sunday' : 6, 'Monday' : 0, 'Tuesday' : 1, 'Wednesday' : 2,'Thursday':3,'Friday':4,'Saturday':5}
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

def timeOverlapWithTime( timeOne, timeTwo):
	a=timeOne[0]
	b=timeOne[1]
	c=timeTwo[0]
	d=timeTwo[1]
	if (a>c and a<d) or (b>c and b<d) or (a<=c and b>c):
		return True
	else:
		return False

def timeIncludedInDay(time, day):
	for item in day:
		if timeIncludedInTime(time, item):
			return True
	return False

def timeIncludedInExcept(date, time, exceptList):
	for item in exceptList:
		if (item[0] is date) and timeOverlapWithTime(time, [item[1],item[2]]):
			return True
	return False

def available(show, student, role,dayOne):
	if (show['date'] in student['not']):
		return False
	elif timeIncludedInExcept(show['date'], show['time'][role], student['except']):
		return False
	elif timeIncludedInDay(show['time'][role],student['weekly'][getDay(dayOne,show['date'])]):
		return True
	else:
		return False

def allStudentsAvailableHM(show, students, dayOne):
	answer=[]
	for item in students:
		if item['max'] is 'HM':
			if available(show, item, 'HM',dayOne):
				answer.append(item)
	return answer

def allStudentsAvailableAHM(show, students, dayOne):
	answer=[]
	for item in students:
		if (item['max'] is 'HM') or (item['max'] is 'AHM'):
			if available(show, item, 'AHM', dayOne):
				answer.append(item)
	return answer

def allStudentsAvailableUsher(show, students, dayOne):
	answer=[]
	for item in students:
		if available(show, item, 'Usher', dayOne):
			answer.append(item)
	return answer

def allStudentsAvailable(show, students, dayOne):
	return [allStudentsAvailableHM(show, students, dayOne),allStudentsAvailableAHM(show, students, dayOne),allStudentsAvailableUsher(show, students,dayOne)]

def updateStudent(show, student, role):
	student['except']=student['except']+[([show['date'], show['time'][role][0],show['time'][role][1]])]
	if role is 'HM':
		student['shows'][0]=(student['shows'][0]+1)
	elif role is 'AHM':
		student['shows'][1]=(student['shows'][1]+1)
	else:
		student['shows'][2]=(student['shows'][2]+1)

def schedule (shows, students, dayOne):
	for item in shows:
		item['available']=allStudentsAvailable(item, students, dayOne)
	for item in shows:
		HM=[]
		sorted(item['available'][0], key=lambda student: student['shows'][0])
		for i in range(0,min(item['numberOfStaff']['HM'],len(item['available'][0]))):
			HM.append(item['available'][0][i])
			updateStudent(item,item['available'][0][i],'HM')
		print HM
		item['available']=allStudentsAvailable(item, students, dayOne)
		AHM=[]
		sorted(item['available'][1], key=lambda student: student['shows'][1])
		for i in range(0,min(item['numberOfStaff']['AHM'],len(item['available'][1]))):
			AHM.append(item['available'][1][i])
			updateStudent(item,item['available'][1][i],'AHM')
		print AHM
		item['available']=allStudentsAvailable(item, students, dayOne)
		Usher=[]
		sorted(item['available'][2], key=lambda student: student['shows'][2])
		for i in range(0,min(item['numberOfStaff']['Usher'],len(item['available'][1]))):
			Usher.append(item['available'][2][i])
			updateStudent(item,item['available'][2][i],'Usher')
		print Usher
		item['scheduled']=[HM,AHM,Usher]
		print item['scheduled']
		for item in shows:
			item['available']=allStudentsAvailable(item, students, dayOne)
	print shows

def dayOne(day, month, year):
	convertMonth={1:11,2:12,3:1,4:2,5:3,6:4,7:5,8:6,9:7,10:8,11:9,12:10}
	d=day
	if(month is 1 or month is 2):
		y=year-1
	else:
		y=year
	m= convertMonth[month]
	w=(d+int(2.6*m-.2)+5*(y % 4)+4*(y%100)+6*(y%400))%7
	dayOfWeek={1:'Monday',2:'Tuesday',3:'Wednesday',4:'Thursday',5:'Friday',6:'Saturday',0:'Sunday'}
	return dayOfWeek[w]

import unittest
class TestGetDayOne(unittest.TestCase):
	def testGetDayOne1(self):
		self.assertEqual('Monday',dayOne(26,5,2014))
	def testGetDayOne2(self):
		self.assertEqual('Thursday',dayOne(25,12,2014))
	def testGetDayOne3(self):
		self.assertEqual('Friday',dayOne(1,4,2016))
class TestGetDay(unittest.TestCase):
	def testGetDay1(self):
		self.assertEqual('Monday',getDay('Monday',1))
	def testGetDay2(self):
		self.assertEqual('Tuesday',getDay('Tuesday',1))
	def testGetDay3(self):
		self.assertEqual('Monday',getDay('Monday',8))
	def testGetDay4(self):
		self.assertEqual('Tuesday',getDay('Tuesday',8))
	def testGetDay5(self):
		self.assertEqual('Wednesday',getDay('Monday',10))
	def testGetDay6(self):
		self.assertEqual('Saturday',getDay('Monday',20))
class TestTimeIncludedInTime(unittest.TestCase):
	def testTimeIncludedInTime1(self):
		self.assertTrue(timeIncludedInTime([8,10],[7,12]))
	def testTimeIncludedInTime2(self):
		self.assertTrue(timeIncludedInTime([8,10],[7,10]))
	def testTimeIncludedInTime3(self):
		self.assertTrue(timeIncludedInTime([8,10.5],[7,11]))
	def testTimeIncludedInTime4(self):
		self.assertFalse(timeIncludedInTime([8,13],[7,12]))
	def testTimeIncludedInTime5(self):
		self.assertFalse(timeIncludedInTime([6,10],[7,10]))
	def testTimeIncludedInTime6(self):
		self.assertFalse(timeIncludedInTime([8,11.5],[7,11]))
class TestTimeOverlapWithTime(unittest.TestCase):
	def testTimeOverlapWithTime1(self):
		self.assertTrue(timeOverlapWithTime([8,10],[7,12]))
	def testTimeOverlapWithTime2(self):
		self.assertTrue(timeOverlapWithTime([8,10],[7,10]))
	def testTimeOverlapWithTime3(self):
		self.assertTrue(timeOverlapWithTime([8,10.5],[7,11]))
	def testTimeOverlapWithTime4(self):
		self.assertTrue(timeOverlapWithTime([8,13],[7,12]))
	def testTimeOverlapWithTime5(self):
		self.assertTrue(timeOverlapWithTime([6,10],[7,10]))
	def testTimeOverlapWithTime6(self):
		self.assertTrue(timeOverlapWithTime([8,11.5],[7,11]))
	def testTimeOverlapWithTime7(self):
		self.assertFalse(timeOverlapWithTime([11,12],[7,11]))
	def testTimeOverlapWithTime8(self):
		self.assertFalse(timeOverlapWithTime([6,7],[7,11]))
class TestTimeIncludedInDay(unittest.TestCase):
	def testTimeIncludedInDay1(self):
		self.assertTrue(timeIncludedInDay([8,10],[[7,12]]))
	def testTimeIncludedInDay2(self):
		self.assertTrue(timeIncludedInDay([8,10],[[0,2],[7,12]]))
	def testTimeIncludedInDay3(self):
		self.assertTrue(timeIncludedInDay([8,10],[[7,12],[15,24]]))
	def testTimeIncludedInDay4(self):
		self.assertTrue(timeIncludedInDay([8,10],[[15,24],[7,12]]))
	def testTimeIncludedInDay5(self):
		self.assertFalse(timeIncludedInDay([6,10],[[7,12]]))
	def testTimeIncludedInDay6(self):
		self.assertFalse(timeIncludedInDay([6,10],[[0,2],[7,12]]))
	def testTimeIncludedInDay7(self):
		self.assertFalse(timeIncludedInDay([6,10],[[7,12],[15,24]]))
	def testTimeIncludedInDay8(self):
		self.assertFalse(timeIncludedInDay([6,10],[[15,24],[7,12]]))
class TestTimeIncludedInExcept(unittest.TestCase):
	def testTimeIncludedInExcept1(self):
		self.assertTrue(timeIncludedInExcept(5,[8,10],[[5,7,12]]))
	def testTimeIncludedInExcept2(self):
		self.assertTrue(timeIncludedInExcept(5,[8,10],[[2,8,10],[5,7,12]]))
	def testTimeIncludedInExcept3(self):
		self.assertTrue(timeIncludedInExcept(2,[8,10],[[2,8.5,10],[5,7,12]]))
	def testTimeIncludedInExcept4(self):
		self.assertFalse(timeIncludedInExcept(8,[8,10],[[2,8.5,10],[5,7,12]]))
	def testTimeIncludedInExcept5(self):
		self.assertFalse(timeIncludedInExcept(2,[10,12],[[2,8.5,10],[5,7,12]]))
	def testTimeIncludedInExcept6(self):
		self.assertTrue(timeIncludedInExcept(2,[9,11],[[2,8.5,10],[5,7,12]]))
	def testTimeIncludedInExcept7(self):
		self.assertFalse(timeIncludedInExcept(2,[6,8.5],[[2,8.5,10],[5,7,12]]))
class TestAvailable(unittest.TestCase):
	def setUp(self):
		self.showOne={'show':'Test', 'date':5,'time':{'HM':[4,16],'AHM':[12,16],'Usher':[12,16]}, 'numberOfStaff':{'HM':1,'AHM':1,'Usher':5},'location':'Zellerbach Auditorium','FOH Lead':'Rob Bean','start':14,'available':[[],[],[]]}
		self.showTwo={'show':'Test2','date':28,'time':{'HM':[12,16],'AHM':[12,16],'Usher':[12,16]}, 'numberOfStaff':{'HM':1,'AHM':1,'Usher':5},'location':'Zellerbach Playhouse','FOH Lead':'Patrick Hennessey','start':15,'available':[[],[],[]]}
		self.studentOne={'name':'Jessica Allen', 'weekly':{'Monday':[[10,12],[16,20]],'Tuesday':[],'Wednesday':[],'Thursday':[],'Friday':[[10,18]],'Saturday':[],'Sunday':[]}, 'not':[1,7,28],'except':[[5,7,16],[30,8,15]],'max':'AHM','shows':[0,0,0],'available':0}
		self.studentTwo= {'name':'Max Vale', 'weekly':{'Monday':[[16,20]],'Tuesday':[],'Wednesday':[],'Thursday':[],'Friday':[[10,18]],'Saturday':[],'Sunday':[[5,4]]}, 'not':[1,7,28],'except':[[30,8,15]],'max':'HM','shows':[0,0,0],'available':0}
	def testAvailable1(self):
		self.assertFalse(available(self.showOne, self.studentOne,'AHM','Monday'))
	def testAvailable2(self):
		self.assertTrue(available(self.showOne, self.studentTwo,'AHM','Monday'))
	def testAvailable3(self):
		self.assertFalse(available(self.showOne, self.studentTwo,'HM','Monday'))
	def testAvailable4(self):
		self.assertFalse(available(self.showTwo, self.studentOne,'AHM','Monday'))
class TestAllStudentsAvailable(unittest.TestCase):
	def setUp(self):
		self.shows=[{'show':'Test', 'date':1,'time':{'HM':[17,18],'AHM':[17,18],'Usher':[17,18]}, 'numberOfStaff':{'HM':1,'AHM':1,'Usher':5},'location':'Zellerbach Auditorium','FOH Lead':'Rob Bean','start':14,'available':[[],[],[]]},
	  		 {'show':'Test2','date':6,'time':{'HM':[12,16],'AHM':[12,16],'Usher':[12,16]}, 'numberOfStaff':{'HM':1,'AHM':1,'Usher':5},'location':'Zellerbach Playhouse','FOH Lead':'Patrick Hennessey','start':15,'available':[[],[],[]]}]
		self.students=[{'name':'Jessica Allen', 'weekly':{'Monday':[[10,12],[16,20]],'Tuesday':[],'Wednesday':[],'Thursday':[],'Friday':[[10,18]],'Saturday':[],'Sunday':[]}, 'not':[7,28],'except':[[5,7,16],[30,8,15]],'max':'AHM','shows':[0,0,0]},
		 	 {'name':'Max Vale', 'weekly':{'Monday':[[16,20]],'Tuesday':[],'Wednesday':[],'Thursday':[],'Friday':[[10,18]],'Saturday':[],'Sunday':[[5,4]]}, 'not':[7,28],'except':[[30,8,15]],'max':'HM','shows':[0,0,0]}]
	def testAllStudentsAvailableHM1(self):
		self.assertTrue(available(self.shows[0],self.students[1],'HM','Monday'))
		self.assertEqual(allStudentsAvailableHM(self.shows[0],self.students, 'Monday')[0]['name'],'Max Vale')
	def testAllStudentsAvailableAHM1(self):
		self.assertTrue(available(self.shows[0],self.students[0],'AHM','Monday'))
		self.assertTrue(available(self.shows[0],self.students[1],'AHM','Monday'))
		self.assertEqual(allStudentsAvailableAHM(self.shows[0],self.students, 'Monday')[1]['name'],'Max Vale')
		self.assertEqual(allStudentsAvailableAHM(self.shows[0],self.students, 'Monday')[0]['name'],'Jessica Allen')
	def testAllStudentsAvailableUsher1(self):
		self.assertTrue(available(self.shows[0],self.students[0],'Usher','Monday'))
		self.assertTrue(available(self.shows[0],self.students[1],'Usher','Monday'))
		self.assertEqual(allStudentsAvailableUsher(self.shows[0],self.students, 'Monday')[1]['name'],'Max Vale')
		self.assertEqual(allStudentsAvailableUsher(self.shows[0],self.students, 'Monday')[0]['name'],'Jessica Allen')
	def testAllStudentsAvailable1(self):
		self.assertEqual(3,len(allStudentsAvailable(self.shows[0],self.students,'Monday')))
		self.assertEqual(3,len(allStudentsAvailable(self.shows[1],self.students,'Monday')))
	def testAllStudentsAvailable2(self):
		self.assertEqual(1,len(allStudentsAvailable(self.shows[0],self.students,'Monday')[0]))
		self.assertEqual(2,len(allStudentsAvailable(self.shows[0],self.students,'Monday')[1]))
		self.assertEqual(2,len(allStudentsAvailable(self.shows[0],self.students,'Monday')[2]))
class TestSchedule(unittest.TestCase):
	def setUp(self):
		self.shows=[{'show':'Test', 'date':1,'time':{'HM':[17,18],'AHM':[17,18],'Usher':[17,18]}, 'numberOfStaff':{'HM':1,'AHM':1,'Usher':5},'location':'Zellerbach Auditorium','FOH Lead':'Rob Bean','start':14,'available':[[],[],[]]},
	  		 {'show':'Test2','date':6,'time':{'HM':[12,16],'AHM':[12,16],'Usher':[12,16]}, 'numberOfStaff':{'HM':1,'AHM':1,'Usher':5},'location':'Zellerbach Playhouse','FOH Lead':'Patrick Hennessey','start':15,'available':[[],[],[]]}]
		self.students=[{'name':'Jessica Allen', 'weekly':{'Monday':[[10,12],[16,20]],'Tuesday':[],'Wednesday':[],'Thursday':[],'Friday':[[10,18]],'Saturday':[],'Sunday':[]}, 'not':[7,28],'except':[[5,7,16],[30,8,15]],'max':'AHM','shows':[0,0,0]},
		 	 {'name':'Max Vale', 'weekly':{'Monday':[[16,20]],'Tuesday':[],'Wednesday':[],'Thursday':[],'Friday':[[10,18]],'Saturday':[],'Sunday':[[5,4]]}, 'not':[7,28],'except':[[30,8,15]],'max':'HM','shows':[0,0,0]}]
	def testSchedule1(self):
		schedule(self.shows,self.students,'Monday')
