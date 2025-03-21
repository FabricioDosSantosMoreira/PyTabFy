"""
PyTabFy Builds and Displays Customizable Tables

https://github.com/FabricioDosSantosMoreira/PyTabFy
"""
from typing import List, Tuple

from PyTabFy.Others import get_version
from PyTabFy.PyTConfigs import GlobalConfigs
from PyTabFy.PyTUtils import validate_obj_type

# version_tuple is a Tuple that defines the current version of PyTabFy.
# 
# Tuple Structure:
#   version_tuple = (major: int, minor: int, patch: int, stage: str)
#
# Tuple Examples:
#   version_tuple = (1, 2, 3, 'null')  -> v1.2.3
#   version_tuple = (4, 5, 6, 'beta')  -> v4.5.6 beta
#   version_tuple = (7, 8, 9, 'alpha') -> v7.8.9 alpha
version_tuple: Tuple[int, int, int, str] = (1, 0, 1, 'null')
validate_obj_type(
    obj=version_tuple, 
    obj_name='version_tuple', 
    obj_type=Tuple[int, int, int, str]
)


__version__ = get_version(version_tuple)
__all__: List[str] = [
    # NOTE: modules
    'PyTCore',
    'PyTEnums', 
    'PyTUtils', 
    'PyTConfigs', 
    'Dummy', 
    'Examples', 

    # NOTE: non-modules
    '__version__',
    '__all__',
    'get_version',
    'version_tuple',
    'global_configs',
]

global_configs = GlobalConfigs()
