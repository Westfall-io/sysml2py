# sysml2py
[![PyPI version](https://badge.fury.io/py/sysml2py.svg)](https://badge.fury.io/py/sysml2py)[![PyPI status](https://img.shields.io/pypi/status/sysml2py.svg)](https://pypi.python.org/pypi/sysml2py/)[![Coverage Status](https://coveralls.io/repos/github/Westfall-io/sysml2py/badge.svg)](https://coveralls.io/github/Westfall-io/sysml2py)![Docstring Coverage](https://raw.githubusercontent.com/Westfall-io/sysml2py/main/doc-cov.svg)[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

[![Trello](https://img.shields.io/badge/Trello-%23026AA7.svg?style=for-the-badge&logo=Trello&logoColor=white)](https://trello.com/b/xHfFUzlk/sysml2py)

## Description
sysml2py is an open source pure Python library for constructing python-based
classes consistent with the [SysML v2.0 standard](https://github.com/Systems-Modeling/SysML-v2-Release).

## Requirements
sysml2py requires the following Python packages:
- [textX](https://github.com/textX/textX)
- [pyyaml](https://github.com/yaml/pyyaml)
- [astropy](https://github.com/astropy/astropy)

## Installation

Multiple installation methods are supported by sysml2py, including:

|                             **Logo**                              | **Platform** |                                    **Command**                                    |
|:-----------------------------------------------------------------:|:------------:|:---------------------------------------------------------------------------------:|
|       ![PyPI logo](https://simpleicons.org/icons/pypi.svg)        |     PyPI     |                        ``python -m pip install sysml2py``                        |
|     ![GitHub logo](https://simpleicons.org/icons/github.svg)      |    GitHub    | ``python -m pip install https://github.com/Westfall-io/sysml2py/archive/refs/heads/main.zip`` |

## Documentation

Documentation can be found [here.](https://westfall-io.github.io/sysml2py/)

### Basic Usage

The code below will create a part called Stage 1, with a shortname of <'3.1'>
referencing a specific requirement or document. It has a mass attribute of 100
kg. It has a thrust attribute of 1000 N. These attributes are created and placed
as a child of the part. Next, we recall the part value for thrust and add 199 N.
Finally, we can dump the output from this class as grammar output and load it
into the classtree function which takes the initial grammar and converts it into
classes which correctly format the output.
```
  from sysml2py.formatting import classtree
  from sysml2py import Attribute, Part

  import astropy.units as u
  a = Attribute()._set_name('mass')
  a.set_value(100*u.kg)
  b = Attribute()._set_name('thrust')
  b.set_value(1000*u.N)
  c = Part()._set_name("Stage_1")._set_name("'3.1'", short=True)
  c._set_child(a)
  c._set_child(b)
  v = "Stage_1.thrust"
  c._get_child(v).set_value(c._get_child(v).get_value()+199*u.N)
  print(classtree(c.dump()).dump())
```

It will output the following, which isn't yet fully correct as we need to import
the SI units to be valid SysML.
```
  part <'3.1'> Stage_1 {
    attribute mass= 100.0 [kg];
    attribute thrust= 1199.0 [N];
  }
```

The package is able to handle Items, Parts, and Attributes.

```
a = Part()._set_name('camera')
b = Item()._set_name('lens')
d = Attribute()._set_name('mass')
c = Part()._set_name("sensor")
c._set_child(a)
c._set_child(b)
a._set_child(d)
print(classtree(c.dump()).dump())
```

will return:
```
part sensor {
   part camera {
      attribute mass;
   }
   item lens;
}
```

## Release Planning
Development can be tracked via [Trello.](https://trello.com/b/xHfFUzlk/sysml2py)

## License
sysml2py is released under the MIT license, hence allowing commercial use of the library.
