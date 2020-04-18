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

	detailsURL = courseURL + "#CourseInfo"
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



URL = "https://www.coursebuffet.com/areas"
req = requests.get(URL)
soup = BeautifulSoup(req.content, 'html5lib')

start = time.time()
courseList = []

categoryList = soup.find_all("li", {"class" : "col-xs-3"})
for category in categoryList:
	subjectList = category.find_all("li", {"class" : "subname"})
	for subject in subjectList:
		anchorTag = subject.find("a")
		subjectURL = anchorTag.get('href')
		subjectURL = "https://www.coursebuffet.com" + subjectURL

# for i in range(1):
# 	for j in range(1):
# 		subjectURL = "https://www.coursebuffet.com/sub/computer-engineering"

		r = requests.get(subjectURL)
		
		courseSoup = BeautifulSoup(r.content, 'html5lib')
		path = courseSoup.find_all("span", {"class" : "resultlist-unit-coursetitle"})

		for span in path:
			aTags = span.find_all("a")
			for tag in aTags:
				course = {}
				href = tag.get('href')
				href = "https://www.coursebuffet.com" + href
				course = getCourse(href)

				print(course)
				courseList.append(course)
				with open("Courses.json", "a+") as outfile: 
				    json.dump(course, outfile, indent = 3) 

print(len(courseList))

end = time.time()
print("Time taken = ", end - start)