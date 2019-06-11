[![Build Status](https://travis-ci.org/kangwonlee/build_utils.svg?branch=master)](https://travis-ci.org/kangwonlee/build_utils)

# Build Utilities

Build (and run) C/C++ files using iPython / Jupyter magic commands

## How to use

* In one cell

```
load_ext build_util
```

* In a cell later

```
%% cpp

#include <iostream>
int main(int argn, char* argv[])
{
    std::cout << "{msg}" << '\\n';
    return 0;
}
```
