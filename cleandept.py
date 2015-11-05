import json
import csv
import pprint

raw = 'dept_sums15.csv'
jsonfile = 'deptsums.json'

#Read in the CSV and put it in a big list
# 0					1		2		3
# Department name, College, Campus, Salary

class Case:
    def __init__(self, name, college, campus, salary):
        self.campus = campus
        self.college = college
        self.name = name
        self.salary = salary

everyone = []

with open(raw, 'rb') as csvfile:
	salData = csv.reader(csvfile, delimiter=',', quotechar='"', skipinitialspace=True)
	next(salData, None)
	for row in salData:
		x = Case(row[0], row[1], row[2], row[3])
		everyone.append(x)

ui = {
	'name': 'UI',
	'children': []
}

#Build dict that will be used for JSON
for person in everyone:

	salary = person.salary.replace(',', '')

	#If the campus in't in ui, we add it and the full entry here and move onto next person
	if not any(campus['name'] == person.campus for campus in ui['children']):
		ui['children'].append({
			'name' : person.campus,
			'children' : [{
				'name' : person.college,
				'children' : [{
					'name' : person.name,
					'size' : float(salary)
				}]
			}]
		})

	#Campus is already in dict.
	#Now we need to check whether campus' children has:
	#College
	#If it doesn't, add the entire entry
	#If it does, we need to check for department in college's children
	#If it doesn't, add the entire entry
	#If it does, we need to append the employee to dept's children
	else:
		#If the college isn't in campus's children, add it and the full entry
		#If college is already in UI's children, nothing happens in this loop 
		for campus in ui['children']:
			if campus['name'] == person.campus:
				if not any(college['name'] == person.college for college in campus['children']):
					campus['children'].append({
						'name' : person.college,
						'children' : [{
							'name' : person.name,
							'size' : float(salary)
						}]
					})
					continue

		#College is already in dict, need to add department now
		for campus in ui['children']:
			if campus['name'] == person.campus:
				for college in campus['children']:
					if college['name'] == person.college:
						if not any(department['name'] == person.name for department in college['children']):
							college['children'].append({
								'name' : person.name,
								'size' : float(salary)
								})
						else:
							for department in college['children']:
								if department['name'] == person.name:
									department['size'] += float(salary)



with open(jsonfile, 'w') as output:
	json.dump(ui, output)

		
pp = pprint.PrettyPrinter(indent=1)
pp.pprint(ui)
