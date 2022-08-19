from .case_converters import pascal_to_snake
from .electro_colors import alert_danger
from .electro_colors import alert_info
from .electro_colors import alert_warning
import sys


class AgentExceptionsFinder:

    def __init__(self, agent_path):
        self.agent_path = agent_path
        self.agent_content = []
        self.failure_exceptions = []
        self.compromised_exceptions = []
        self.constants_values = []
        self.exceptions_keywords = [
            ['EntityOrKillFailure', 'findLast'],
            ['EntityOrKillCompromised', 'findLast'],
            'killFailureIfNullElseGet',
            'killCompromisedIfNullElseGet',
            'killFailureIfEmptyElseGet',
            'killCompromisedIfEmptyElseGet',
            'killCustomFailureIfAnyHaveSome',
            'killCustomFailureIfAnyHasNone',
            'killCustomFailureWhenAllHaveNone',
            'killCustomFailureWhenAllHaveSome',
            'killFailureIfImageNotSaved',
            'killAsFailure',
            'killAsCompromised',
            'killFailureWithMsg',
            'killCompromisedWithMsg'
        ]
        # with open('test.php', 'r') as code:
        #     get_all_exceptions_list(''.join(list(map(lambda l: l.strip(), code.readlines()[2:]))).replace(';', ''))

    def fetch_agent_content(self):
        with open(self.agent_path, 'r') as f:
            self.agent_content.extend(f.readlines())

    def fetch_all_declared_constants(self):
        for lin in self.agent_content:
            if 'const ' in lin and ';' in lin:
                exception_line = lin
                lin = lin.strip()
                lin = lin.replace('"', '')
                lin = lin.replace(';', '')
                try:
                    var, val = list(filter(lambda x: x != '' and x != '=', lin.split(' ')))[1:]
                except:
                    print(alert_danger(self.agent_path))
                    sys.exit(alert_danger(f'Invalid Line: {exception_line}'))
                self.constants_values.append([var, val])

    def fetch_all_exceptions(self):
        temp_agent_content = self.agent_content
        while len(temp_agent_content) != 0:
            lin = temp_agent_content[0]
            temp_agent_content.pop(0)

            for exception_keyword in self.exceptions_keywords:
                code_block = []
                if isinstance(exception_keyword, list):
                    if exception_keyword[0] in lin and exception_keyword[-1] in lin:
                        code_block.append(lin)
                        while True:
                            if ';' in lin:
                                break
                            lin = temp_agent_content[0]
                            temp_agent_content.pop(0)
                            code_block.append(lin)
                        self._fetch_all_exceptions_list(''.join(list(map(lambda l: l.strip(), code_block))).replace(';', ''))
                else:
                    if exception_keyword in lin:
                        code_block.append(lin)
                        while True:
                            if ';' in lin:
                                break
                            lin = temp_agent_content[0]
                            temp_agent_content.pop(0)
                            code_block.append(lin)
                        self._fetch_all_exceptions_list(''.join(list(map(lambda l: l.strip(), code_block))).replace(';', ''))

    def _find_any_str_literals_in_str_and_remove_all_non_alpha_chars_from_those_strings(self, s: str):
        temp_list = list(s)
        count = temp_list.count('\'')
        parts = []
        if count > 0:
            for i in range(int(count / 2)):
                before_index = temp_list.index('\'')
                before_part_with_apostrophe = temp_list[:before_index + 1]
                parts.extend(before_part_with_apostrophe)

                # Find part before ending apostrophe
                temp_list = temp_list[len(before_part_with_apostrophe):]
                ending_index = temp_list.index('\'')

                parts.extend(list(map(lambda _x: '' if _x != '_' and not _x.isalpha() else _x, temp_list[:ending_index])))
                parts.append('\'')
                temp_list = temp_list[(ending_index + 1):]
                # part_after_apostrophe_without_its_ending_apostrophe = temp_list[len(before_part_with_apostrophe):]
            parts.extend(temp_list)
        else:
            return s
        return ''.join(parts)

    def _get_exceptions_function_only(self, fun_line: str):
        fun_line = fun_line.replace('()', '')
        starting_brackets_count = fun_line.count('(')
        ending_brackets_count = fun_line.count(')')
        if ending_brackets_count > starting_brackets_count:
            difference = ending_brackets_count - starting_brackets_count
            for diff in range(difference):
                last_index_of_brace = fun_line.rindex(')')
                fun_line = list(fun_line)
                fun_line.pop(last_index_of_brace)
                fun_line = ''.join(fun_line)
        fun_line = fun_line[:(fun_line.rfind(')') + 1)]
        return fun_line[:(fun_line.rfind(')') + 1)]

    def _fetch_all_exceptions_list(self, complete_line: str):
        exception_starting_lines = []

        for exception_keyword in self.exceptions_keywords:
            temp_line = complete_line
            if isinstance(exception_keyword, list):
                for i in range(temp_line.count(exception_keyword[0])):
                    if exception_keyword[-1] in temp_line:
                        prefix = exception_keyword[-1]
                        suffix = exception_keyword[0]
                        slug = temp_line[temp_line.find(prefix): (temp_line.find(suffix) + len(suffix))]
                        temp_line = temp_line[temp_line.find(slug):]
                        exception_starting_lines.append(temp_line)
                        temp_line = temp_line[len(slug):]
            else:
                for i in range(temp_line.count(exception_keyword)):
                    temp_line = temp_line[temp_line.find(exception_keyword):]
                    exception_starting_lines.append(temp_line)

        for e in list(map(lambda l: l.replace('\\\'', '').replace('\\\"', '').replace('"', '\''), exception_starting_lines)):
            luch_removed = self._find_any_str_literals_in_str_and_remove_all_non_alpha_chars_from_those_strings(e)
            ex_fun_only = self._get_exceptions_function_only(luch_removed)

            fun_name = ex_fun_only[:ex_fun_only.find('(')]

            if fun_name.startswith('findLast'):
                if fun_name.endswith('EntityOrKillFailure'):
                    if ex_fun_only[-2] == '\'':  # has custom exception
                        last_index_of_apos = ex_fun_only.rfind('\'')
                        ex_fun_only = list(ex_fun_only)
                        ex_fun_only.pop(last_index_of_apos)
                        ex_fun_only = ''.join(ex_fun_only)
                        ex = ex_fun_only[(ex_fun_only.rfind('\'') + 1):-1]
                        self.failure_exceptions.append(ex)
                    else:  # has no custom exception
                        slug = fun_name.replace('findLast', '').replace('EntityOrKillFailure', '')
                        ex = f'failed_to_find_{pascal_to_snake(slug)}_entity'
                        self.failure_exceptions.append(ex)
                elif fun_name.endswith('EntityOrKillCompromised'):
                    if ex_fun_only[-2] == '\'':  # has custom exception
                        last_index_of_apos = ex_fun_only.rfind('\'')
                        ex_fun_only = list(ex_fun_only)
                        ex_fun_only.pop(last_index_of_apos)
                        ex_fun_only = ''.join(ex_fun_only)
                        ex = ex_fun_only[(ex_fun_only.rfind('\'') + 1):-1]
                        self.compromised_exceptions.append(ex)
                    else:  # has no custom exception
                        slug = fun_name.replace('findLast', '').replace('EntityOrKillCompromised', '')
                        ex = f'data_compromised_{pascal_to_snake(slug)}_entity_must_exist_but_not_found'
                        self.compromised_exceptions.append(ex)
            elif fun_name.startswith('killFailureIfNullElseGet'):
                if ex_fun_only[-2] == '\'':  # has custom exception
                    last_index_of_apos = ex_fun_only.rfind('\'')
                    ex_fun_only = list(ex_fun_only)
                    ex_fun_only.pop(last_index_of_apos)
                    ex_fun_only = ''.join(ex_fun_only)
                    ex = ex_fun_only[(ex_fun_only.rfind('\'') + 1):-1]
                    self.failure_exceptions.append(ex)
                else:  # has no custom exception
                    slug = fun_name.replace('killFailureIfNullElseGet', '').replace('Entity', '')
                    ex = f'{pascal_to_snake(slug)}_entity_not_found'
                    self.failure_exceptions.append(ex)
            elif fun_name.startswith('killCompromisedIfNullElseGet'):
                if ex_fun_only[-2] == '\'':  # has custom exception
                    last_index_of_apos = ex_fun_only.rfind('\'')
                    ex_fun_only = list(ex_fun_only)
                    ex_fun_only.pop(last_index_of_apos)
                    ex_fun_only = ''.join(ex_fun_only)
                    ex = ex_fun_only[(ex_fun_only.rfind('\'') + 1):-1]
                    self.compromised_exceptions.append(ex)
                else:  # has no custom exception
                    slug = fun_name.replace('killCompromisedIfNullElseGet', '').replace('Entity', '')
                    ex = f'data_compromised_{pascal_to_snake(slug)}_entity_not_found'
                    self.compromised_exceptions.append(ex)
            elif fun_name.startswith('killFailureIfEmptyElseGet'):
                if ex_fun_only[-2] == '\'':  # has custom exception
                    last_index_of_apos = ex_fun_only.rfind('\'')
                    ex_fun_only = list(ex_fun_only)
                    ex_fun_only.pop(last_index_of_apos)
                    ex_fun_only = ''.join(ex_fun_only)
                    ex = ex_fun_only[(ex_fun_only.rfind('\'') + 1):-1]
                    self.failure_exceptions.append(ex)
                else:  # has no custom exception
                    slug = fun_name.replace('killFailureIfEmptyElseGet', '').replace('Entities', '')
                    ex = f'{pascal_to_snake(slug)}_entities_not_found'
                    self.failure_exceptions.append(ex)
            elif fun_name.startswith('killCompromisedIfEmptyElseGet'):
                if ex_fun_only[-2] == '\'':  # has custom exception
                    last_index_of_apos = ex_fun_only.rfind('\'')
                    ex_fun_only = list(ex_fun_only)
                    ex_fun_only.pop(last_index_of_apos)
                    ex_fun_only = ''.join(ex_fun_only)
                    ex = ex_fun_only[(ex_fun_only.rfind('\'') + 1):-1]
                    self.compromised_exceptions.append(ex)
                else:  # has no custom exception
                    slug = fun_name.replace('killCompromisedIfEmptyElseGet', '').replace('Entities', '')
                    ex = f'data_compromised_{pascal_to_snake(slug)}_entities_not_found'
                    self.compromised_exceptions.append(ex)
            elif fun_name.startswith('killCustomFailureIfAnyHaveSome'):
                lin_after_first_apos = ex_fun_only[(ex_fun_only.find('\'') + 1):]
                ex = lin_after_first_apos[:lin_after_first_apos.find('\'')]
                self.failure_exceptions.append(ex)
            elif fun_name.startswith('killCustomFailureIfAnyHasNone'):
                lin_after_first_apos = ex_fun_only[(ex_fun_only.find('\'') + 1):]
                ex = lin_after_first_apos[:lin_after_first_apos.find('\'')]
                self.failure_exceptions.append(ex)
            elif fun_name.startswith('killCustomFailureWhenAllHaveNone'):
                lin_after_first_apos = ex_fun_only[(ex_fun_only.find('\'') + 1):]
                ex = lin_after_first_apos[:lin_after_first_apos.find('\'')]
                self.failure_exceptions.append(ex)
            elif fun_name.startswith('killCustomFailureWhenAllHaveSome'):
                lin_after_first_apos = ex_fun_only[(ex_fun_only.find('\'') + 1):]
                ex = lin_after_first_apos[:lin_after_first_apos.find('\'')]
                self.failure_exceptions.append(ex)
            elif fun_name.startswith('killFailureIfImageNotSaved'):
                lin_after_first_double_colon = ex_fun_only[(ex_fun_only.find('::') + 2):]
                slug = lin_after_first_double_colon[:lin_after_first_double_colon.find(',')]
                if '::' in slug:  # has used a variable
                    print(slug)
                    print(self.constants_values)
                    slug = list(filter(lambda x: x[0] == slug, self.constants_values))
                    print(slug)
                    slug = list(filter(lambda x: x[0] == slug, self.constants_values))[0][1]
                    print("passed")
                    self.failure_exceptions.append(f'failed_to_save_{slug.lower()}_file')
                else:  # used a custom name for image request parameter
                    slug = slug.replace('\'', '')
                    self.failure_exceptions.append(f'failed_to_save_{slug.lower()}_file')
            elif fun_name.startswith('killAsFailure'):
                print(alert_warning(self.agent_path))
                print(alert_warning(f'Legacy Exception Found: {ex_fun_only}'))
                print(alert_info(f'Please Use killFailureWithMsg() function for better experience'))
                lin_after_first_apos = ex_fun_only[(ex_fun_only.find('\'') + 1):]
                ex = lin_after_first_apos[:lin_after_first_apos.find('\'')]
                self.failure_exceptions.append(ex)
            elif fun_name.startswith('killAsCompromised'):
                print(alert_warning(self.agent_path))
                print(alert_warning(f'Legacy Exception Found: {ex_fun_only}'))
                print(alert_info(f'Please Use killCompromisedWithMsg() function for better experience'))
                lin_after_first_apos = ex_fun_only[(ex_fun_only.find('\'') + 1):]
                ex = lin_after_first_apos[:lin_after_first_apos.find('\'')]
                self.compromised_exceptions.append(ex)
            elif fun_name.startswith('killFailureWithMsg'):
                lin_after_first_apos = ex_fun_only[(ex_fun_only.find('\'') + 1):]
                ex = lin_after_first_apos[:lin_after_first_apos.find('\'')]
                self.failure_exceptions.append(ex)
            elif fun_name.startswith('killCompromisedWithMsg'):
                lin_after_first_apos = ex_fun_only[(ex_fun_only.find('\'') + 1):]
                ex = lin_after_first_apos[:lin_after_first_apos.find('\'')]
                self.compromised_exceptions.append(ex)

    def get_failure_exceptions(self):
        return list(dict.fromkeys(self.failure_exceptions))

    def get_all_compromised_exceptions(self):
        return list(dict.fromkeys(self.compromised_exceptions))
