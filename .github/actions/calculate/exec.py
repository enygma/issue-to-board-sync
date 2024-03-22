from github_projectv2.project import Project
import re
import os
import json

project_id = os.getenv('PROJECT_ID')
org = os.getenv('ORG')

context = json.loads(os.getenv('COMMAND_CONTEXT'))
issue_input = context["event"]["issue"]["body"]

print(issue_input)
# print(os.getenv('COMMAND_CONTEXT'))
issue_id = context["event"]["issue"]["number"]

project = Project()
project.get(org, project_id)
if project is None:
    print('Project not found')
    exit()

def parse_input(input, search_string):
    """
    Parse the input and find the level for the provided search string
    """
    regex = "%s: (.+)" % search_string
    x = re.search(regex, input)

    if x is None:
        print('Level "%s" not found' % search_string)
        return None
    else:
        return x.group(1)

def find_field(project, field_name):
    field = None
    """
    Find the field by name
    """
    for f in project.fields:
        if f.name == field_name:
            return f
        
    if field is None:
        print('Field "%s" not found' % field_name)
        exit()

def find_option(field, input):
    found = None
    for option in field.options:
        if option.name == input:
            found = option
            return option
    
    if found is None:
        print('Option "%s" not found' % input)
        exit()


def update_item_priority(project, item, levels):
    # Calculate the priority and update the project
    priority = calculate_priority(
        levels['Impact Level'], 
        levels['Effort Level'], 
        levels['Confidence Level'], 
        levels['Risk Level'])
    
    print(f"The calculated priority is: {priority}")
    field = find_field(project, 'Priority')
    option = find_option(field, priority)

    res = item.update_field_value(project, field, option)
    print(res)

def update_project_levels(project, input):
    """
    Update the project levels based on the input from the issue
    """
    levels = ['Impact Level', 'Effort Level', 'Confidence Level', 'Risk Level']

    # Update the project with the new values
    items = project.get_items()
    item_found = False

    for item in items:
        if item.number == issue_id:
            levels_found = {}
            print('Updating item title: %s' % item.title)

            for level in levels:
                print('Updating level: %s' % level)
                input = parse_input(issue_input, level)
                field = find_field(project, level)
                option = find_option(field, input)

                # Adding the updated level to the dictionary
                levels_found[level] = input

                res = item.update_field_value(project, field, option)
                print(res)
            
            update_item_priority(project, item, levels_found)
            return item
        
        if not item_found:
            print('Item %s not found to update' % issue_id)

    return levels_found

def calculate_priority(reach, impact, confidence, effort):
    reach = reach.title()
    impact = impact.title()
    confidence = confidence.title()
    effort = effort.title()

    reach_score = {'High': 1, 'Low': 0}
    impact_score = {'High': 2, 'Medium': 1, 'Low': 0}
    confidence_score = {'High': 1, 'Low': 0}
    effort_score = {'High': 0, 'Low': 1}

    priority = 5  # Start with the maximum score of 5
    priority -= reach_score.get(reach, 0)
    priority -= impact_score.get(impact, 0)
    priority -= confidence_score.get(confidence, 0)
    priority -= effort_score.get(effort, 0)

    priority_map = {5: 'P5', 4: 'P4', 3: 'P3', 2: 'P2', 1: 'P1', 0: 'P0'}
    return priority_map.get(priority, 'Invalid input')


# Run it!
levels_found = update_project_levels(project, issue_input)