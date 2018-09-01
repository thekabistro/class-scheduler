import requests, json, time
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

#url = "sis.rutgers.edu/soc/courses.gz?term=9&year=2018&level=U&campus=NB"



def convert24(str1):

    print(str1)
     
    # Checking if last two elements of time
    # is AM and first two elements are 12
    if str1[-2:] == "AM" and str1[:2] == "12":
        return "00" + str1[2:-2]
         
    # remove the AM    
    elif str1[-2:] == "AM":
        print("[" + str1[:-3]+"]")
        return str1[:-3]
     
    # Checking if last two elements of time
    # is PM and first two elements are 12   
    elif str1[-2:] == "PM" and str1[:2] == "12":
        return str1[:-2]
         
    else:
        # add 12 to hours and remove PM
        return str(int(str1[:2]) + 12) + str1[2:8]


def calendarInit():
    store = file.Storage('token.json')
    creds = store.get()

    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)

    GCAL = build('calendar', 'v3', http=creds.authorize(Http()))
    return GCAL



def createOnGoogleCal():
    print("In googleCal method")





soc_url_courses = "https://sis.rutgers.edu/oldsoc/courses.json?subject={}&semester=92018&campus=NB&level=U"

selected_subject = "198"
selected_class = 416
selected_section = "02"

response = requests.get(soc_url_courses.format(selected_subject))

data = response.json()

print (json.dumps(data, sort_keys=True, indent=4))

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

            if section_num == selected_section:

                for meeting in section_times:
                    class_room = meeting['roomNumber']
                    class_campus = meeting['campusName']
                    class_building = meeting['buildingCode']
                    class_start = meeting['startTime']
                    class_end = meeting['endTime']
                    class_day = meeting['meetingDay']
                    class_type = meeting['meetingModeDesc']
                    class_PM = meeting['pmCode']
                    print('{}\t{}\tSECTION {}\tINDEX {}\t ROOM {} | CAMPUS {} | {} | {} | {}, {} - {} | {}'.format(course_full_num, course_short_title, section_num, section_index, class_room, class_campus, class_building, class_type, class_day, class_start, class_end, class_PM))
                
                    timeCombinedStrStart = convert24("%s:%s:00 %sM"%(class_start[0:2], class_start[2:4],class_PM))
                    timeCombinedStrEnd = convert24("%s:%s:00 %sM"%(class_end[0:2], class_end[2:4],class_PM))
                
                    print(timeCombinedStrStart, " - ", timeCombinedStrEnd)

                    print(meeting['meetingDay'])

                    #timeobj = time.strptime(timeCombinedStrStart, "%I:%M %p")

                    #print(timeobj)
                
                    #start_cmd = "2018-"

                    if meeting['meetingDay'] == 'M':
                        start_input = '2018-09-10T%s'%(timeCombinedStrStart)
                        end_input = '2018-09-10T%s'%(timeCombinedStrEnd)
                    if meeting['meetingDay'] == 'T':
                        start_input = '2018-09-04T%s'%(timeCombinedStrStart)
                        end_input = '2018-09-04T%s'%(timeCombinedStrEnd)
                    if meeting['meetingDay'] == 'W':
                        start_input = '2018-09-05T%s'%(timeCombinedStrStart)
                        end_input = '2018-09-05T%s'%(timeCombinedStrEnd)
                    if meeting['meetingDay'] == 'TH':
                        start_input = '2018-09-06T%s'%(timeCombinedStrStart)
                        end_input = '2018-09-06T%s'%(timeCombinedStrEnd)
                    if meeting['meetingDay'] == 'F':
                        start_input = '2018-09-07T%s'%(timeCombinedStrStart)
                        end_input = '2018-09-07T%s'%(timeCombinedStrEnd)

                    print(start_input)
                    print(end_input)

                    location_input = class_building = meeting['buildingCode'] + " " + meeting['roomNumber'] + " - " + class_campus

                    print(location_input)

                    description_input = course_full_num + " - Section " + section_num

                   # if (end_input) == "2018-09-04T01:20:00":
                    #    end_input = "2018-09-04T13:20:00"

                    GCAL = calendarInit()

                    TIMEZONE = 'America/New_York'
                    RRule = 'RRULE:FREQ=WEEKLY;COUNT=18'
                    EVENT = {
                    'summary': course_short_title,
                    'start':   {'dateTime': start_input,'timeZone': TIMEZONE},
                    'end':     {'dateTime': end_input,'timeZone': TIMEZONE},
                    'recurrence': [RRule],
                    'location': location_input,
                    'description': description_input,
                    'colorId': '6' 
                    }

                    e = GCAL.events().insert(calendarId='primary', body=EVENT).execute()

                    
                    print('''*** %r event added:
                    Start: %s
                    End:   %s''' % (e['summary'].encode('utf-8'),
                        e['start']['dateTime'], e['end']['dateTime']))

                    print('URL: {}'.format(e['htmlLink']))

            
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

