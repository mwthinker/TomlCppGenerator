#! /usr/bin/env python3
import toml
import argparse
import os
import textwrap

def get_cpp_array_element_type(name: str, value: list) -> str:
    types = set()
    for item in value:
        if isinstance(item, dict):
            types.add(cap_first(name))
        elif isinstance(item, list):
            types.add(get_cpp_array_element_type(name, item))
        else:
            types.add(get_cpp_type(item))

    if len(types) > 1:
        raise ValueError(f"Array contains multiple types: {types}")

    return types.pop()

class MemberVariable:
    name: str
    type: str
    value: any
    initialization: str

    def __init__(self, name: str, value: any):
        self.value = value
        if isinstance(value, dict):
            self.name = name + "_"
            self.type = cap_first(name)
            self.initialization = self.name + "{data_}"
        elif isinstance(value, list):
            self.name = get_array_variable_name(name)
            element_type = get_cpp_array_element_type(name, value)
            self.type = "Vector<" + element_type + ">"
            self.initialization = f"{self.name}{{Vector<{element_type}>::create(data_[\"{name}\"])}}"
        else:
            self.name = name
            self.type = get_cpp_type(value)
            self.initialization = self.name + "{data_}"

    def get_getter_name(self):
        return cap_first(self.name[:-1])

    def get_declaration(self):
        return f"{self.type} {self.name};"

    #def __str__(self):
    #    return f"{self.name} {self.value}"

    #def __repr__(self):
    #    return f"{self.name} {self.value}"

def cap_first(s):
    return s[:1].upper() + s[1:]

def uncap_first(s):
    return s[:1].lower() + s[1:]

INDENT_STR = '    '

def indent_text(text: str, indent_level: int) -> str:
    return textwrap.indent(text, INDENT_STR * indent_level)

def generate_header(toml_file, namespace="config") -> str:
    header = """
/// This file was autogenerated do not modify it manually.
#ifndef CONFIG_H
#define CONFIG_H

#include <tomlgen/util.h>

#include <string>
#include <vector>

#include <toml.hpp>

namespace config {
"""
    return header

def generate_bottom() -> str:
    bottom = """}

#endif
"""
    return bottom

def generate_constructor(name: str, data: dict[str, any], depth: int) -> str:
    data_variable = ""
    ref = ""
    if depth == 1:
        data_variable = "        : data_{value}"
        ref = ""
    else:
        data_variable = f"        : data_{{value[\"{uncap_first(name)}\"]}}"
        ref = "&"
    constructor = """
class {name} {{
public:
    explicit {name}(toml::value{ref} value)
"""
    constructor = constructor.format(name=name, ref=ref)
    constructor += data_variable
    constructor += generate_member_variables(get_member_variables(data), 2)
    constructor += """
        if (!data_.is_table()) {
            data_ = toml::table{};
        }
    }
"""
    return constructor

def get_member_variables(data: dict[str, any]) ->  list[MemberVariable]:
    member_variables = list()
    for key, value in data.items():
        if isinstance(value, dict) or isinstance(value, list):
            member_variables.append(MemberVariable(key, value))
            
    return member_variables

def get_member_variables_str(member_variables: list[MemberVariable]) -> list[str]:
    member_variables_list = list()
    for member_variable in member_variables:
        if isinstance(member_variable.value, dict) or isinstance(member_variable.value, list):
            member_variables_list.append(member_variable.initialization)
        #elif isinstance(value, list):
            #member_variables_list.append(f"{get_array_variable_name(key)}{{value}}")

    return member_variables_list

def generate_member_variables(member_variables: dict[str, any], depth: int) -> str:
    member_variables_str = ""

    member_variables_list = get_member_variables_str(member_variables)
    index = 0
    size = len(member_variables)
    for variable_name in member_variables_list:
        if index == 0 and size > 1:
            member_variables_str += f"\n, {variable_name}\n"
        elif index == size - 1:
            member_variables_str += f"\n, {variable_name}"
        else:
            member_variables_str += f", {variable_name}\n"
        index += 1
    
    member_variables_str = indent_text(member_variables_str, depth)

    return member_variables_str + " {\n"

def generate_body(parent: str, name: str, data: dict[str, any], depth: int) -> str:
    indent_str = INDENT_STR * depth
    constructor = generate_constructor(name, data, depth)
    struct_code = indent_text(constructor, depth)

    for key, value in data.items():
        if isinstance(value, dict):
            # Nested table, create a new struct
            struct_code += generate_body(name, cap_first(key), value, depth + 1)

            getter = """
    {cpp_type}& get{cpp_type}() {{
        return {key}_;
    }}
"""
            getter = getter.format(cpp_type=cap_first(key), key=key, value=0)
            struct_code += indent_text(getter, depth)
        elif isinstance(value, list):
            memberVariable = MemberVariable(key, value)
            array_str = """
{type}& get{name}() {{
    return {variable};
}}
"""
            array_str = array_str.format(type=memberVariable.type, name=memberVariable.get_getter_name(), variable=memberVariable.name)

            if all(isinstance(item, dict) for item in value):
                # Array of tables (same structure)
                struct_code += generate_body(name, cap_first(key), value[0], depth + 1)

            
                # Array of primitive types
                #extra_arrays += f"{indent_str}{INDENT_STR}{memberVariable.type}{memberVariable.name};\n"
            struct_code += indent_text(array_str, depth + 1)
        else:
            # Base case: a key-value pair, determine the C++ type
            getter_and_setter = get_cpp_getter_and_setter(key, value)
            struct_code += indent_text(getter_and_setter, depth)

    data_getter = """
const toml::value& getData() const {
    return data_;
}
"""
    struct_code += indent_text(data_getter, depth + 1)

    toml_variable = ""
    if depth == 1:
        toml_variable = """
private:
    mutable toml::value data_;
"""
    else:
        toml_variable = """
private:
    toml::value& data_;
"""

    struct_code += indent_text(toml_variable, depth)
    member_variables = get_member_variables(data)
    for member_variable in member_variables:
        struct_code += indent_text(f"    {member_variable.type} {member_variable.name};\n", depth)

    #struct_code += indent_text(member_variables, depth - 1)
    struct_code += indent_text("    };\n", depth - 1)
    return struct_code

def get_array_name(key: str) -> str:
    if key.endswith("s"):
        key += "List"
    else:
        key += "s"
    return cap_first(key)

def get_array_variable_name(key: str) -> str:
    return uncap_first(get_array_name(key)) + "_"

def generate_cpp_code(name, toml_data) -> str:
    cpp_code = generate_header(name)
    cpp_code += generate_body("", name, toml_data, 1)
    cpp_code += generate_bottom()
    return cpp_code

def get_toml_type(value) -> str:
    """
    Returns the corresponding toml11 function type for a given Python value.
    """
    if isinstance(value, int):
        return "integer"
    elif isinstance(value, float):
        return "floating"
    elif isinstance(value, str):
        return "string"
    elif isinstance(value, bool):
        return "boolean"
    else:
        return "value"  # fallback for unsupported types
    
def is_cpp_type(value) -> bool:
    return isinstance(value, (int, float, str, bool, list))

def get_cpp_type(value) -> str:
    """
    Returns the corresponding C++ type for a given Python value.
    """
    if isinstance(value, bool):
        return "bool"
    elif isinstance(value, int):
        return "int"
    elif isinstance(value, float):
        return "double"
    elif isinstance(value, str):
        return "std::string"
    elif isinstance(value, list):
        return "std::vector"
    else:
        raise ValueError(f"Unsupported type: {type(value)}")
    
def get_cpp_getter_and_setter(key: str, value) -> str:
    """
    Returns the corresponding C++ getter using toml11 for a given Python value.
    """
    text = """
    {cpp_type} get{member_name}() const {{
        return toml::find_or(data_, "{key}", {value});
    }}

    void set{member_name}(const {cpp_type}& value) {{
        data_["{key}"] = value;
    }}
    """
    type = get_cpp_type(value)
    return text.format(member_name=cap_first(key), cpp_type=type, key=key, value=get_cpp_default_value(value))
    
def generate_table_initializer(struct_name, table) -> str:
    """
    Generates an initializer list for a C++ struct from a TOML table.
    """
    initializer = f"{struct_name}{{"
    initializer += ", ".join([get_cpp_default_value(value) for value in table.values()])
    initializer += "}"
    return initializer
    
def get_cpp_default_value(value) -> str:
    """
    Returns the default value in C++ syntax for a given Python value.
    """
    if isinstance(value, str):
        return f'"{value}"'
    elif isinstance(value, bool):
        return "true" if value else "false"
    elif isinstance(value, list):
        return "{" + ", ".join(map(str, value)) + "}"
    else:
        return str(value)
    
def load_toml_file(toml_file: str) -> dict[str, any]:
    with open(toml_file, 'r') as file:
        toml_data = toml.load(file)
    return toml_data

def run(args):
    toml_data = load_toml_file(args.toml_file)
    cpp_code = generate_cpp_code("Config", toml_data)
    cpp_file = os.path.join(args.output_dir, os.path.basename(args.toml_file).split(".")[0] + "_config.h")
    with open(cpp_file, "w", encoding="utf-8") as cpp_file:
        cpp_file.write(cpp_code)
    print(f"Generated {cpp_file}")

def main():
    parser = argparse.ArgumentParser(description="Generate C++ code from a TOML file")
    parser.add_argument("toml_file")
    parser.add_argument("output_dir")

    parser.set_defaults(func=run)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
