import sys
from pathlib import Path
# print(sys.executable)
# print(type(sys.executable))
path = Path(__file__)
print(path, type(path))
path2 = path.parent
print(path2, type(path2))
path3 = path2 / "ms-playwright" / "aa"
print(path3, type(path3))




