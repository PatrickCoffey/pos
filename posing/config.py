#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Posing - config.py
------------------

This is the database models for the ORM
"""

import ConfigParser


def_config = "config.ini"

def_config_vals = {"general": {"db_path": "sqlite:///posing.db"}}

def parse_config(conf_file=def_config):
    config_parser = load_config(conf_file)
    conf_dict = _conf_to_dict(config_parser)
    if conf_dict == {}:
        _setup_config()
        config_parser = load_config(conf_file)
        conf_dict = _conf_to_dict(config_parser)
    return conf_dict


def load_config(conf_file=def_config):
    config_parser = ConfigParser.ConfigParser()
    config_parser.read(conf_file)
    return config_parser

def setup_config(config_file=def_config):
    config_parser = ConfigParser.ConfigParser()
    _setup_config

    
def _setup_config(config_file=def_config):
    config_parser = ConfigParser.ConfigParser()
    for sect, opts in def_config_vals.iteritems():
        config_parser.add_section(sect)
        for opt, val in opts.iteritems():
            config_parser.set(sect, opt, val)
            try:
                config_parser.set(sect, opt, val)
            except:
                print("config set failed:")
                print("section: " + sect)
                print("  option: " + opt)
                print("    value: " + val)
    with open(config_file, "wb+") as f:
        config_parser.write(f)


def _conf_to_dict(config):
    conf_dict = {}
    for sect in config.sections():
        conf_dict[sect] = {}
        section = config.options(sect)
        for opt in section:
            try:
                conf_dict[sect][opt] = config.get(sect, opt)
            except:
                conf_dict[sect][opt] = None
    return conf_dict


def _print_config(config):
    for name, section in config.iteritems():
        print(name)
        for name, value in section.iteritems():
            print("  " + name + ' = ' + value)
            
            
if __name__ == '__main__':
    Config = parse_config()
    _print_config(Config)
    