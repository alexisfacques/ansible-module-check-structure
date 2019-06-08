# ansible-module-check-structure

`ansible-module-check-structure` is a handy custom Ansible module allowing you
assert the type of Ansible facts, and validate
the structure (or schema) of dictionaries and lists.

This is done by crafting an Ansible fact in which each hierarcherical element
is a string representing one of [python's built-in types](https://docs.python.org/3/library/stdtypes.html), apply
this structure to a fact you want to check.

You may for instance want to check that each element of a list is a dictionary
in which the `foo` key defined, and paired to a string value...
```yaml
struct:
  - foo: str
```

... or check that each element of a list is an integer:
```yaml
struct:
  - int
```

Possibilities are endless!

## Getting started

### Installing

#### The "Ansible role" way

- Clone this repository to your Ansible `role_path`, or install via `ansible-galaxy`;
  ```sh
  ansible-galaxy install alexisfacques.ansible_module_check_structure
  ```

- Import the role in your playbooks before running any role or task that require the `check_structure` module:
  ```yaml
  - hosts: all
    roles:
      - alexisfacques.ansible_module_check_structure
    tasks:
      - name: Ensure variable is a string
        check_structure:
          struct:
            - str
          var:
            -"{{ is_this_a_str }}"
  ```

#### The "Ansible library" way

Alternatively, if importing a role is too much of a hassle, you can store this
module in the `library` directory defined in your `ansible.cfg` file
(Default is a sub-directory called `library` in the directory that contains
your playbooks):
```
[defaults]
library = /path/to/your/library
```

## Usage

### Parameters

<table>
  <tr>
    <th>Parameter</th>
    <th>Choices/Defaults</th>
    <th>Comments</th>
  </tr>
  <tr>
    <td>struct<br> - / required</td>
    <td></td>
    <td>The schema that the variable should validate.</td>
  </tr>
  <tr>
    <td>var<br> - / required</td>
    <td></td>
    <td>The variable you want to test.</td>
  </tr>
</table>

### Example of use

Examples of use can be found [here](./examples/demo.yml).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
