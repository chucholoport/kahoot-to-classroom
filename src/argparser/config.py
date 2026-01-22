from dataclasses import dataclass

@dataclass
class kahoot_to_classroom:
    description: str = 'Automations for scholar purposes'
    epilog:      str = 'author: jesus.loport'
    report:      str = 'Kahoot report file(s) to convert to Google Classroom format'
    reference:   str = 'Google Classroom report file for data reference'
    out:         str = 'Output file path. If directory does not exist, then creates it'