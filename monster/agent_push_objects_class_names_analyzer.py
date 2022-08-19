import sys
from .electro_colors import alert_danger
from .electro_colors import alert_primary
from .electro_colors import alert_secondary
from .electro_colors import alert_info


class AgentPushObjectsClassNamesAnalyzer:

    def __init__(self, agent_path):
        self.agent_path = agent_path
        self.agent_content = []

    def fetch_agent_content(self):
        with open(self.agent_path, 'r') as agent_file:
            self.agent_content.extend(agent_file.readlines())

    def is_all_okay(self):
        for lin in self.agent_content:
            if 'array_push(' in lin and '@' not in lin:
                print(alert_danger(self.agent_path))
                sys.exit(alert_danger(f'Push class annotation not found: {lin}'))
            elif 'array_push(' in lin and '@' in lin:
                lin = lin.strip()
                content_after_at_sign = lin[(lin.find('@') + 1):]
                if ' ' in content_after_at_sign:
                    content_after_at_sign = content_after_at_sign.split(' ')[0]
                if content_after_at_sign == '':
                    print(alert_danger(self.agent_path))
                    sys.exit(alert_danger(f'Invalid Push class annotation: {lin}'))
                elif content_after_at_sign[0] != '_' and not content_after_at_sign[0].isupper():
                    print(alert_danger(self.agent_path))
                    sys.exit(alert_danger(f'Invalid Push class annotation: {lin}'))

    def display_names(self):
        shown = False
        for lin in self.agent_content:
            if 'array_push(' in lin and '@' in lin and '@_' not in lin:
                if not shown:
                    print()
                    print(alert_primary(self.agent_path))
                    shown = True
                lin = lin.strip()
                content_after_at_sign = lin[lin.find('@'):]
                if ' ' in content_after_at_sign:
                    content_after_at_sign = content_after_at_sign.split(' ')[0]
                print(alert_info(f'data class {content_after_at_sign.replace("@", "")}()'))
        if shown:
            print()
        else:
            print(alert_secondary(f'No class objects found in {self.agent_path}'))
