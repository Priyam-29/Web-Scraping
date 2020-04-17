import json
import time
start = time.time()

import requests 
from bs4 import BeautifulSoup 

# URL = "https://www.coursebuffet.com/areas"
# req = requests.get(URL)
# soup = BeautifulSoup(req.content, 'html5lib')

courseList = []

# categoryList = soup.find_all("li", {"class" : "col-xs-3"})
# for category in categoryList:
# 	subjectList = category.find_all("li", {"class" : "subname"})
# 	for subject in subjectList:
# 		anchorTag = subject.find("a")
# 		subjectURL = anchorTag.get('href')
# 		subjectURL = "https://www.coursebuffet.com" + subjectURL

for i in range(1):
	for j in range(1):
		subjectURL = "https://www.coursebuffet.com/sub/computer-engineering"

		r = requests.get(subjectURL)
		
		courseSoup = BeautifulSoup(r.content, 'html5lib')
		path = courseSoup.find_all("span", {"class" : "resultlist-unit-coursetitle"})

		for span in path:
			aTags = span.find_all("a")
			for tag in aTags:
				course = {}
				href = tag.get('href')
				title = tag.text
				course["Title"] = title.strip()
				href = "https://www.coursebuffet.com" + href

				cr = requests.get(href) 
				soup2 = BeautifulSoup(cr.content, 'html5lib')
				description = soup2.find("div", {"class" : "coursedetails-description"})
				p = description.find('p')
				course["Description"] = p.text.strip()

				href3 = href+"#CourseInfo"
				r3 = requests.get(href3)
				soup3 = BeautifulSoup(r3.content, 'html5lib')
				details = soup3.find_all("ul", {"class" : "CourseInfoTab-list1"})
				for detail in details:
					li = detail.find_all("li")
					for l in li:
						keys = l.find("span")
						value = keys.next_sibling.strip() 
						course[keys.text] = value

				try:
					classifiedAs = soup2.find("a", {"class" : "coursepage-coursenumber"})
					cAs = classifiedAs.text
					course["Classified As"] = cAs.strip()
				except:
					course["Classified As"] = "Unknown"

				try:
					ul2 = soup2.find("ul", {"class" : "coursepage-coursemeta"})
					subjectPrevTag = ul2.find("i", {"class" : "fa fa-book"})
					subject = subjectPrevTag.parent.text 
					course["Subject"] = subject.strip()
				except:
					course["Subject"] = "Unknown"

				try:
					univPrevTag = ul2.find("i", {"class" : "fa fa-university"})
					univ = univPrevTag.parent.text 
					course["University"] = univ.strip()
				except:
					course["University"] = "Unknown"

				try:
					providerPrevTag = ul2.find("i", {"class" : "fa fa-laptop"})
					provider = providerPrevTag.parent.text
					course["Provider"] = provider.strip()
				except:
					course["Provider"] = "Unknown"

			print(course)
			courseList.append(course)

print(len(courseList))

with open("Courses.json", "w+") as outfile: 
    json.dump(courseList, outfile, indent = 3) 

end = time.time()
print("Time taken = ", end - start)