#! /usr/bin/env python3
import toml
import argparse

INDENT_STR = '    '

def generate_header(toml_file, namespace="config"):
    header = """
#ifndef CONFIG_H
#define CONFIG_H

#include <string>
#include <vector>

namespace config {
"""
    return header

def generate_bottom():
    bottom = """}

#endif
"""
    return bottom

def generate_body(name, data, indent=0):
    """
    Recursively generates C++ struct code from the given TOML data.
    """
    indent_str = INDENT_STR * indent
    struct_code = f"\n{indent_str}struct {name} {{\n"
    
    for key, value in data.items():
        if isinstance(value, dict):
            # Nested table, create a new struct
            struct_code += generate_body(key.capitalize(), value, indent + 1)
            struct_code += f"{indent_str}{INDENT_STR}{key.capitalize()} {key};\n"
        elif isinstance(value, list):
            if all(isinstance(item, dict) for item in value):
                # Array of tables (same structure)
                struct_code += generate_body(key.capitalize(), value[0], indent + 1)
                struct_code += f"{indent_str}{INDENT_STR}std::vector<{key.capitalize()}> {key};\n"
            else:
                # Array of primitive types
                cpp_type = get_cpp_type(value[0])
                struct_code += f"{indent_str}{INDENT_STR}std::vector<{cpp_type}> {key};\n"
        else:
            # Base case: a key-value pair, determine the C++ type
            cpp_type = get_cpp_type(value)
            struct_code += f"{indent_str}{INDENT_STR}{cpp_type} {key};\n"
    
    struct_code += f"{indent_str}}};\n\n"
    return struct_code

def generate_cpp_code(name, toml_data):
    """
    Generates C++ code from the given TOML data.
    """
    cpp_code = generate_header(name)
    cpp_code += generate_body(name, toml_data, 1)
    cpp_code += generate_bottom()
    return cpp_code

def get_cpp_type(value):
    """
    Returns the corresponding C++ type for a given Python value.
    """
    if isinstance(value, int):
        return "int"
    elif isinstance(value, float):
        return "double"
    elif isinstance(value, str):
        return "std::string"
    elif isinstance(value, bool):
        return "bool"
    elif isinstance(value, list):
        return "std::vector"
    else:
        raise ValueError(f"Unsupported type: {type(value)}")
    
def load_toml_file(toml_file):
    with open(toml_file, 'r') as file:
        toml_data = toml.load(file)
    return toml_data

def run(args):
    toml_data = load_toml_file(args.toml_file)
    cpp_code = generate_cpp_code("Config", toml_data)
    cpp_file = args.toml_file.split(".")[0] + "_config.h"
    with open(cpp_file, "w") as cpp_file:
        cpp_file.write(cpp_code)
    print(f"Generated {cpp_file}")

def main():
    parser = argparse.ArgumentParser(description="Generate C++ code from a TOML file")
    parser.add_argument("toml_file")

    parser.set_defaults(func=run)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
