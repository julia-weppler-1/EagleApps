import requests
import re
from .models import Plan

def fetch_data_from_api(course_code):
    url = "http://localhost:8080/planning/planningcourses"
    params = {'code': course_code}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        data = response.json()  # Convert response to JSON format
        return data
    except requests.exceptions.RequestException as e:
        # Handle exceptions (e.g., connection errors, timeouts)

        return None
    
def get_course_by_code(code):
    base_url = "http://localhost:8080/planning/planningcourses"
    params = {'code': code}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response.json()  # Returns JSON data from API
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")

        return None
    
# takes course code String
# returns list of prereq course code Strings
def get_prereqs_from_api(course_code):
    course_json = get_course_by_code(course_code)[0]
    prereq_text = course_json['prereqTerseTranslations']
    
    # if there are no prereqs, return []
    if len(prereq_text) > 0:
        prereq_text = prereq_text[0]['translation']['plain']
    else:
        return prereq_text

    # search for 4 letters followed by 4 numbers, case insensitive
    course_pattern = r"(?i)([A-Z]{4}\d{4})"
    # search for 'or', designating choice between two courses
    or_pattern = r"\b(or)\b"

    prereqs = []

    # find all occurrences, with their starting and ending positions within the String
    courses = re.finditer(course_pattern, prereq_text)
    ors = re.finditer(or_pattern, prereq_text)

    # find the starting positions for each match
    course_positions = [match.start() for match in courses]
    or_positions = [match.start() for match in ors]

    # add matches for both courses and 'or', maintaining the order where they appeared in the String
    for pos in sorted(course_positions + or_positions):
        if pos in course_positions:
            # course matches start at pos and end 8 positions later 
            prereqs.append(prereq_text[pos:pos+8].upper()) 
        else:
            prereqs.append("or")

    # while loop searches for 'or' and combines the two courses it is between
    # into 'COURSE1/COURSE2'
    i = 0
    while i < len(prereqs):
        # don't do anything if the 'or' is at the end of the String
        if prereqs[i] == "or" and i < len(prereqs)-1:
            prereqs[i-1] += ("/" + prereqs[i+1])
            # remove the 'or'
            prereqs.pop(i)
            # remove the occurrences[i+1] which was "or'd" to occurrences[i-1]
            prereqs.pop(i)
        else:
            i += 1

    return prereqs

# get list of user plans, making sure the current plan is at the front of that list
def sort_plans_by_current(student, current_plan):
    # get queryset object of all plans associated with the user
    user_plans = Plan.objects.filter(user=student)
    # remove current plan from the queryset
    if current_plan is not None:
        user_plans = user_plans.exclude(id=current_plan.id)
        # cast queryset to list and insert current plan at the front
        user_plans = list(user_plans)
        user_plans.insert(0, current_plan)
    else:
        user_plans = list(user_plans)

    return user_plans

# get dictionary of courses, populating empty classes with "" for display purposes
def get_full_courses_dict(semesters, plan):
    courses = {}
    for sem in semesters:
        courses_in_sem = getattr(plan, sem).split("/")
        # remove the last blank element
        if len(courses_in_sem) > 0:
            courses_in_sem.pop()
        # show blank course cards, up to 5 per semester
        while len(courses_in_sem) < 5:
            courses_in_sem.append("")
        courses[sem] = courses_in_sem
    
    return courses
    