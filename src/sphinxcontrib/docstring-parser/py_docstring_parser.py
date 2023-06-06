import os
import json
import re
import warnings
from sphinx_needs.api import add_need
from sphinx.util.docutils import SphinxDirective


class docstrings_parser(SphinxDirective):
    # configs and init routine
    # this enables content in the directive
    has_content = True

    def parse_file(self, file_path: str, file_name: str) -> None:
        with open(file_path, "r") as file_reader:
            file_lines = file_reader.readlines()
        interest = False
        in_docstring = False
        indent = 0
        in_SphinxNeeds = False
        in_Need = False
        for line_number, line in enumerate(file_lines, 1):
            if line.strip().startswith("class") or line.strip().startswith("def"):
                interest = True
                indent = line.index(line.strip()[0])
            else:
                if len(line.strip()) > 0:  # not empty line
                    if line.index(line.strip()[0]) < indent:
                        interest = False
                        indent = 0
            if in_docstring and ('"""' in line or "'''" in line):
                in_docstring = False
                interest = False
                in_SphinxNeeds = False
            if interest and ('"""' in line or "'''" in line):
                in_docstring = True
            if in_SphinxNeeds and ".. " in line and "::" in line:
                in_Need = True
                n_t_l = line.index(".. ") + 3
                n_t_r = line.index("::", n_t_l)
                need_type = line[n_t_l:n_t_r]
                title = line[n_t_r + 2 :].strip()
                need_indent = line.index(".. ")
                lineno = line_number
            if in_docstring and "@SphinxNeeds" in line:
                in_SphinxNeeds = True
            if in_Need:
                if len(line.strip()) > 0:  # not empty line
                    if line.index(line.strip()[0]) < need_indent or (
                        '"""' in line or "'''" in line
                    ):
                        in_Need = False
                        need_indent = 0
                        need_data = {
                            "id": "BAD_PARSING",
                            "content": "",
                            "status": "",
                            "test_platform": "python",
                        }
                        additional_data = {}
                        need_content = file_lines[lineno : line_number - 1]
                        for data in need_content:
                            attribute = re.search(r"\:([a-z]+)\:\s(.*)", data)
                            if attribute:
                                if attribute.group(1) in need_data:
                                    need_data[attribute.group(1)] = attribute.group(2)
                                else:
                                    link_names = [
                                        x["option"]
                                        for x in self.env.app.config.needs_extra_links
                                    ]
                                    if attribute.group(1) in link_names:
                                        warnings.warn(
                                            "The use of extra_links through extension doesn't seem to work!"
                                        )
                                    if (
                                        attribute.group(1)
                                        in self.env.app.config.needs_extra_options
                                    ):
                                        additional_data[
                                            attribute.group(1)
                                        ] = attribute.group(2)
                            else:
                                need_data["content"] += data
                        self.main_section += add_need(
                            self.env.app,
                            self.state,
                            file_name,
                            lineno=lineno,
                            need_type=need_type,
                            title=title,
                            **need_data,
                            **additional_data,
                        )

    def walkthrough_folder(self, folder_path: str) -> None:
        walk = os.walk(folder_path)
        for dirpath, _, files in walk:
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(dirpath, file)
                    self.parse_file(file_path, file)

    def run(self):
        self.main_section = []
        folders_list = []
        folders_str = [argus for argus in self.content if ":folders:" in argus][0]
        if folders_str.find("["):
            folders_str = folders_str[
                folders_str.index("[") : folders_str.rindex("]") + 1
            ]
            folders_list = json.loads(folders_str)
        if len(folders_list) != 0:
            # check that every folder exists
            for folder_path in folders_list:
                folder_path = os.path.abspath(folder_path)
                if not os.path.exists(folder_path):
                    raise ValueError(f"The folder :{folder_path} doesn't exist !")
                else:
                    self.walkthrough_folder(folder_path)
        return self.main_section
