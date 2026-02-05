from dataclasses import dataclass

@dataclass
class kahoot_to_classroom:
    description: str = 'Automations for scholar purposes'
    epilog:      str = 'author: jesus.loport'
    config:      str = 'Configuration for group to evaluate'
    report:      str = 'Kahoot report file(s) to convert to Google Classroom format'
    autograde:   str = 'Trigger Google Classroom API to automatically grade based on Kahoot reports'
    kahoot:      str = 'Source for grading criteria: Kahoot'
    github:      str = 'Source for grading criteria: GitHub'