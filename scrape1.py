import json
import time
import requests 
from bs4 import BeautifulSoup 


def getCourse(courseURL):
	course = {}
	req = requests.get(courseURL)
	soup = BeautifulSoup(req.content, 'html5lib')

	title = soup.find("h4", {"class" : "coursepage-coursetitle"}).text
	course["Title"] = title.strip()

	description = soup.find("div", {"class" : "coursedetails-description"})
	p = description.find('p')
	course["Description"] = p.text.strip()

	detailsURL = url+"#CourseInfo"
	req = requests.get(detailsURL)
	detailsSoup = BeautifulSoup(req.content, 'html5lib')

	details = detailsSoup.find_all("ul", {"class" : "CourseInfoTab-list1"})
	for detail in details:
		li = detail.find_all("li")
		for l in li:
			keys = l.find("span")
			value = keys.next_sibling.strip() 
			course[keys.text] = value

	try:
		classifiedAs = soup.find("a", {"class" : "coursepage-coursenumber"})
		cAs = classifiedAs.text
		course["Classified As"] = cAs.strip()
	except:
		course["Classified As"] = "Unknown"

	try:
		ul = soup.find("ul", {"class" : "coursepage-coursemeta"})
		subjectPrevTag = ul.find("i", {"class" : "fa fa-book"})
		subject = subjectPrevTag.parent.text 
		course["Subject"] = subject.strip()
	except:
		course["Subject"] = "Unknown"

	try:
		univPrevTag = ul.find("i", {"class" : "fa fa-university"})
		univ = univPrevTag.parent.text 
		course["University"] = univ.strip()
	except:
		course["University"] = "Unknown"

	try:
		providerPrevTag = ul.find("i", {"class" : "fa fa-laptop"})
		provider = providerPrevTag.parent.text
		course["Provider"] = provider.strip()
	except:
		course["Provider"] = "Unknown"

	return course


def getCoursesURLsList(subjectURL):
	subjectURL = "https://www.coursebuffet.com" + subjectURL
	req = requests.get(subjectURL)
	courseSoup = BeautifulSoup(req.content, 'html5lib')

	courseList = courseSoup.find_all("span", {"class" : "resultlist-unit-coursetitle"})
	CoursesURLsList = []
	for span in courseList:
		anchorTags = span.find_all("a")
		for tag in anchorTags:
			href = tag.get('href')
			href = "https://www.coursebuffet.com" + href
			CoursesURLsList.append(href)

def getSubjectURLsList(areasURL):
	req = requests.get(areasURL)
	soup = BeautifulSoup(req.content, 'html5lib')
	categoryList = soup.find_all("li", {"class" : "col-xs-3"})
	subjectURLsList = []
	for category in categoryList:
		subjectList = category.find_all("li", {"class" : "subname"})
		for subject in subjectList:
			anchorTag = subject.find("a")
			subjectURL = anchorTag.get('href')
			subjectURLsList.append(subjectURL)
	return subjectURLsList

start = time.time()

courseList = []
areasURL = "https://www.coursebuffet.com/areas"
subjectURLsList = getSubjectURLsList(areasURL)
for subjectURL in subjectURLsList:
	courseURLsList = getSubjectURLsList(subjectURL)
	for courseURL in courseURLsList:
		course = getCourse()
		courseList.append(course)

with open("Courses.json", "a+") as outfile:
	json.dump(courseList, outfile, indent = 5) 

print(len(courseList)) 

end = time.time()
print("Time taken = ", end - start)