

import requests, json 

#url = "sis.rutgers.edu/soc/courses.gz?term=9&year=2018&level=U&campus=NB"

soc_url_courses = "https://sis.rutgers.edu/oldsoc/courses.json?subject={}&semester=92018&campus=NB&level=U"

selected_subject = 198
selected_class = 344
selected_section = 1

response = requests.get(soc_url_courses.format(selected_subject))

data = response.json()

# print (json.dumps(data, sort_keys=True, indent=4))

#print(data['course_number'=314])

for c in data:
    course_unit_code = c['offeringUnitCode']
    course_subject = c['subject']
    course_number = c['courseNumber']
    course_full_num = '{}:{}:{}'.format(course_unit_code, course_subject, course_number)
    course_short_title = c['title'].strip()
    course_sections = c['sections']
    course_campus = c['campusCode']
    course_credits = c['credits']
    course_url = c['synopsisUrl']
    course_pre_reqs = c['preReqNotes']
    course_core_codes = str(c['coreCodes'])
    print("Code {} | Number {} | Name {}".format(course_unit_code, course_number, course_short_title))
   
    if int(course_number) == int(selected_class):
      
        for section in course_sections:
            
            section_num = section['number']
            section_index = section['index']
            if section['openStatus']:
                section_open_status = 'OPEN'
            else:
                section_open_status = 'CLOSED'
            section_instructors = str(section['instructors'])
            section_times = section['meetingTimes']
            section_notes = section['sectionNotes']
            section_exam_code = section['examCode']

            #print(section_times)

            for meeting in section_times:
                class_room = meeting['roomNumber']
                class_campus = meeting['campusName']
                class_building = meeting['buildingCode']
                class_start = meeting['startTime']
                class_end = meeting['endTime']
                class_type = meeting['meetingModeDesc']
                print('{}\t{}\tSECTION {}\tINDEX {}\t ROOM {} | CAMPUS {} | {} | {} | {} - {}'.format(course_full_num, course_short_title, section_num, section_index, class_room, class_campus, class_building, class_type,class_start, class_end))
            
            print("__________________Section Num {} | Index {} ".format(section_num, section_index))

def get_all_subjects():
    l = 'https://sis.rutgers.edu/soc/subjects.json?semester=92016&campus=NB&level=U'
    r = requests.get(l).json()
    subjects = []

    for c in r:
        subjects.append(c['code'])

    return subjects

def main():
    subjects = get_all_subjects()


def createOnGoogleCal():
    print("In googleCal method")
