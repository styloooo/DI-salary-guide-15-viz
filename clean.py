import json
import csv
import pprint

raw = '2015.csv'
jsonfile = 'output.json'

#Read in the CSV and put it in a big list

class Case:
    def __init__(self, campus, college, department, name, position, positionSal):
        self.campus = campus
        self.college = college
        self.department = department
        self.name = name
        self.position = position
        self.positionSal = positionSal

everyone = []

with open(raw, 'rb') as csvfile:
	salData = csv.reader(csvfile, delimiter=',', quotechar='"', skipinitialspace=True)
	next(salData, None)
	for row in salData:
		x = Case(row[6], row[0], row[1], row[2], row[3], row[4])
		everyone.append(x)

print everyone[0].name

ui = {
	'name': 'UI',
	'children': []
}

#Build dict that will be used for JSON
for person in everyone:
	#If the campus in't in ui, we add it and the full entry here and move onto next person
	if not any(campus['name'] == person.campus for campus in ui['children']):
		ui['children'].append({
			'name' : person.campus,
			'children' : [{
				'name' : person.college,
				'children' : [{
					'name' : person.department,
					'children' : [{
						'name' : person.name,
						'size' : person.positionSal
					}]
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
							'name' : person.department,
							'children' : [{
								'name' : person.name,
								'size' : person.positionSal
							}]
						}]
					})
					continue

		#College is already in dict, need to check for department now
		for campus in ui['children']:
			if campus['name'] == person.campus:
				for college in campus['children']:
					if college['name'] == person.college:
						if not any(department['name'] == person.department for department in college['children']):
							college['children'].append({
								'name' : person.department,
								'children' : [{
									'name' : person.name,
									'size' : person.positionSal
								}]
							})
							continue

						else:
							for department in college['children']:
								if department['name'] == person.department:
									department['children'].append({
											'name' : person.name,
											'size' : person.positionSal
										})



#with open(jsonfile, 'w') as output:
	#json.dump(ui, output)

		
pp = pprint.PrettyPrinter(indent=1)
pp.pprint(ui)
