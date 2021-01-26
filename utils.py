import csv
import json

csv_file = './database/operators.csv'
# Returns contents of the database/operators.csv as a json
# Assume headings in csv are Oper Name, Oper Source, Creation Time, Oper Path
def operators_dict():
    data = {}
    try:
        list1 = []
        with open(csv_file, encoding='utf-8') as csvf: 
            for line in csvf:
                row = line.split(',')
                inner_data = {}
                inner_data['oper_name'] = row[0].strip()
                inner_data['oper_source'] = row[1].strip()
                inner_data['create_time'] = row[2].strip()
                inner_data['oper_path'] = row[3].strip()
                list1.append(inner_data)
        data['operators'] = list1
    except Exception as e:
        print ("Exception {}".format(str(e)))
    return data

#operators_dict()
