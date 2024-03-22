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

def update_project_levels(project, input):
    """
    Update the project levels based on the input from the issue
    """
    levels = ['Impact Level', 'Effort Level', 'Confidence Level', 'Risk Level']
    for level in levels:
        print('Updating level: %s' % level)

        input = parse_input(issue_input, level)
        if input is None:
            continue

        field = find_field(project, level)

        # Find the option for the new field value
        option = find_option(field, input)

        # Update the project with the new values
        items = project.get_items()
        for item in items:
            if item.number == issue_id:
                print('Updating item title: %s' % item.title)
                res = item.update_field_value(project, field, option)
                # print(res)

            print('Item %s not found to update' % issue_id)

# Run it!
update_project_levels(project, issue_input)