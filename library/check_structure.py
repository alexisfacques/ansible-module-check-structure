
#!/usr/bin/env python
# -*- coding: utf-8 -*


DOCUMENTATION = """
---
module: check_structure

author:
    - "Alexis Facques" (@alexisfacques)

short_description: Check typings and (dict/list) structures of variables easily

description:
    - "This module allows to check typings (python built-in types), and \
       validate structure (or schema) of Ansible dictionnaries and lists"

options:
    struct:
        description:
            - The schema that the variable should validate.
        required: true
    var:
        description:
            - The variable you want to test.
        required: true
"""

EXAMPLES = """
- name: This should pass
  check_structure:
    struct:
      - foo: str
        fooList: list
        fooDict:
          bar: int
    var:
      - foo: "foo"
        fooList:
          - "foo"
          - "bar"
        fooDict:
          bar: 1

- name: This should fail
  check_structure:
    struct:
      - foo: int
        fooList: list
        fooDict:
          bar: str
    var:
      - foo: "foo"
        fooList:
          - "foo"
          - "bar"
        fooDict:
          bar: 1
"""

from ansible.module_utils.basic import AnsibleModule
import json
import sys

def is_python_3():
     return sys.version_info > (3,0)

def check_structure(struct, conf, resolve_path=["var"]):
    if isinstance(struct, dict) and isinstance(conf, dict):
        ret = []
        for k in struct:
          ret += check_structure(struct[k], conf[k], list(resolve_path)+[k]) \
            if k in conf else [{ "path": list(resolve_path)+[k], "expected": "defined", "was": "undefined" }]
        return ret
    if isinstance(struct, list) and isinstance(conf, list):
        ret = []
        for res in (check_structure(struct[0], c, list(resolve_path) + ["0"]) for c in conf):
            ret += res
        return ret
    if isinstance(struct, type):
        # If struct is a type, check if conf is the type of struct.
        # struct is the type of conf
        return [] if isinstance(conf, struct) else [{ "path": resolve_path, "expected": struct.__name__, "was": type(conf).__name__ }]
    else:
        # struct is neither a dict, nor a list, not a type.
        # If struct is a string, get builtin type it represnts and check if
        # config is of this type.
        if struct in ("unicode", "basestring", "str"):
            conf_is_valid = isinstance(conf, str) if is_python_3() else isinstance(conf, basestring)
        else:
            conf_is_valid = isinstance(conf, getattr(__builtins__, struct))
        return [] if conf_is_valid else [{ "path": resolve_path, "expected": struct, "was": type(conf).__name__ }]

def main():
    exit_message = dict(failed=False)

    module = AnsibleModule(
        argument_spec=dict(
            struct=dict(required=True, type="json"),
            var=dict(required=True, type="json")
        ),
        # No changes will be made to this environment with this module
        supports_check_mode=True
    )

    try:
        struct = json.loads(module.params["struct"])
        var = json.loads(module.params["var"])
        wrongs = check_structure(struct, var)
        if wrongs:
            errors = list(map( lambda res: "Expected \"%s\" to be \"%s\"; was \"%s\"." % (".".join(res["path"]), res["expected"], res["was"]), wrongs ))
            exit_message = dict(failed=True, msg="Invalid \"var\" structure: %s" % " ".join(errors) )
    except AttributeError:
        exit_message = dict(failed=True, msg="Invalid structure item \"struct\".")
    except Exception, e:
        exit_message = dict(failed=True, msg="An error has occured with the \"check_structure\" module: %s" % e)

    if exit_message["failed"]:
        module.fail_json(**exit_message)
    else:
        module.exit_json()

if __name__ == "__main__":
    main()
