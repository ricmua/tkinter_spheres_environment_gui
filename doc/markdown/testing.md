<!-- License

Copyright 2022-2023 Neuromechatronics Lab, Carnegie Mellon University (a.whit)

Contributors:
  a. whit. (nml@whit.contact)

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
-->

## Testing

A number of unit, integration, and/or regression tests are included with this 
package.

### Pytest

The [pytest] framework can be invoked directly.

```bash
python3 -m pytest path/to/tkinter_spheres_environment_gui/test
```

The `-k` and `-vv` command line flags for `pytest` might be useful. The former 
can be used to run specific tests (e.g., `-k test_object_initialization`). The 
latter requests verbose output. See the documentation for [pytest invocations] 
for further information.

```bash
python3 -m pytest path/to/tkinter_spheres_environment_gui/test/ \
  -k test_reference_images -vv
```

### README.md

As an alternative, the [doctest] framework can be directly invoked to verify 
that the package is functioning as expected -- for example, by running the 
doctests in this README.

```bash
python -m doctest path/to/tkinter_spheres_environment_gui/README.md
```

If desired, the doctests can also be run directly from a Python environment.

```python
import doctest
doctest.testfile('path/to/README.md', module_relative=False)
```


<!---------------------------------------------------------------------
   References
---------------------------------------------------------------------->

[Python path]: https://docs.python.org/3/tutorial/modules.html#the-module-search-path

[doctest]: https://docs.python.org/3/library/doctest.html

[pytest]: https://docs.pytest.org/

[pytest keyword expression]: https://docs.pytest.org/en/7.2.x/how-to/usage.html#specifying-which-tests-to-run

[pytest invocations]: https://docs.pytest.org/en/7.1.x/how-to/usage.html

