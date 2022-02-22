import sys
import os
import re
import ast


class Analyzer:
    error_dict = {
        'S001': 'Too long',
        'S002': 'Indentation is not a multiple of four',
        'S003': 'Unnecessary semicolon after a statement',
        'S004': 'Less than two spaces before inline comments',
        'S005': 'TODO found ',
        'S006': 'More than two blank lines preceding a code line ',
        'S007': 'Too many spaces after construction_name (def or class)',
        'S008': 'Class name class_name should be written in CamelCase',
        'S009': 'Function name function_name should be written in snake_case',
        'S010': 'Argument name arg_name should be written in snake_case',
        'S011': 'Variable var_name should be written in snake_case',
        'S012': 'The default argument value is mutable'
    }

    def __init__(self, file_name):
        self.file_name = file_name
        self.error_result = {}

    def check_line_length(self, line_number, line: str):
        if len(line) > 79:
            self.error_result.update({f'{line_number+1}:S001': f'{self.file_name}: Line {line_number+1}: S001 {Analyzer.error_dict["S001"]}'})

    def check_indent(self, line_number, line: str):
        count = 0
        for a in line:
            if a != ' ':
                break
            count += 1
        if count % 4 != 0:
            self.error_result.update({f'{line_number+1}:S002': f'{self.file_name}: Line {line_number+1}: S002 {Analyzer.error_dict["S002"]}'})

    def check_semicolon(self, line_number, line: str):
        line = line.strip('\n\r')
        if len(line) > 0:
            if (line[-1] == ';' and '#' not in line) or (';' in line and '#' in line and line.find(';') < line.find('#')):
                self.error_result.update({f'{line_number+1}:S003': f'{self.file_name}: Line {line_number+1}: S003 {Analyzer.error_dict["S003"]}'})

    def check_space_before_comment(self, line_number, line: str):
        if '#' in line:
            pos = line.find('#')
            if pos > 0 and (line[pos-1] != " " or line[pos-2] != " "):
                self.error_result.update({f'{line_number+1}:S004': f'{self.file_name}: Line {line_number+1}: S004 {Analyzer.error_dict["S004"]}'})

    def check_todo(self, line_number, line: str):
        if '#' in line:
            split_line = line.split()
            try:
                pos = split_line.index('#')
                if split_line[pos + 1].lower() == 'todo':
                    self.error_result.update({f'{line_number+1}:S005': f'{self.file_name}: Line {line_number+1}: S005 {Analyzer.error_dict["S005"]}'})
            except (ValueError, IndexError):
                pass

    def check_empty_lines(self):
        with open(self.file_name, 'r') as f:
            count = 0
            line_number = 0
            for line in f:
                line = line.strip(' \n\r')
                if line:
                    if count > 2:
                        self.error_result.update({f'{line_number+1}:S006': f'{self.file_name}: Line {line_number+1}: S006 {Analyzer.error_dict["S006"]}'})
                    count = 0
                else:
                    count += 1
                line_number += 1

    def check_space_before_class(self, line_number, line: str):
        if re.match("\s*class\s{2,}", line) is not None or re.match("\s*def\s{2,}", line) is not None:
            self.error_result.update({f'{line_number + 1}:S007': f'{self.file_name}: Line {line_number + 1}: S007 {Analyzer.error_dict["S007"]}'})

    def check_class_camel_case(self, line_number, line: str):
        template = "[A-Z][A-Za-z0-9\)\(]+"
        in_line = re.split(r'\s+',line.strip())
        if in_line[0] == 'class':
            if re.match(template, in_line[1]) is None:
                self.error_result.update({f'{line_number + 1}:S008': f'{self.file_name}: Line {line_number + 1}: S008 {Analyzer.error_dict["S008"]}'})

    def check_func_snake_case(self, line_number, line: str):
        template = "[a-z0-9_]+"
        in_line = re.split(r'\s+',line.strip())
        if in_line[0] == 'def':
            if re.match(template, in_line[1]) is None:
                self.error_result.update({f'{line_number + 1}:S009': f'{self.file_name}: Line {line_number + 1}: S009 {Analyzer.error_dict["S009"]}'})

    def check_ast(self, line_number, line: str):
        tree = ast.parse(line)
        




    def get_sorted_error(self):
        result = [
            self.error_result[key]
            for key in sorted(
                self.error_result.keys(),
                key=lambda x: int(x.split(':')[0])
            )
        ]
        return result

    def complex_check(self):
        with open(self.file_name, 'r') as f:
            for n, line in enumerate(f.readlines()):
                self.check_line_length(n, line)
                self.check_indent(n, line)
                self.check_semicolon(n, line)
                self.check_space_before_comment(n, line)
                self.check_todo(n, line)
                self.check_space_before_class(n, line)
                self.check_class_camel_case(n, line)
                self.check_func_snake_case(n, line)
        self.check_empty_lines()


work_dir = sys.argv[1]
if os.path.isdir(work_dir):
    for file in os.listdir(work_dir):
        split_name = file.split('.')
        if len(split_name) >= 2 and split_name[1] == 'py':
            path = work_dir + '\\' + file if sys.platform == 'win32' else work_dir + '/' + file
            analyzer = Analyzer(path)
            analyzer.complex_check()
            print(*(analyzer.get_sorted_error()), sep='\n')
else:
    analyzer = Analyzer(work_dir)
    analyzer.complex_check()
    print(*(analyzer.get_sorted_error()), sep='\n')
