"""Rev C22 — option E (rectangle 3.06 x 3.44) and option F (triangle, wall edge 3.06 as E, plants edge 4.37),
both to the end of the AC line with the AC above the roof; columns end flush under the roof."""
import importlib.util
import os
import build

HERE = os.path.dirname(os.path.abspath(__file__))
AC_END = 2260 + 800                                    # right end of the AC box from the facade (verify on site)


def load(vk, tri, name):
    os.environ.update(C16_VK=vk, C16_L=str(AC_END), C16_TRI=str(tri))
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, "preview_c22.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


if __name__ == "__main__":
    F = load("V1T", 1306, "c22F")
    E = load("V1", 1260, "c22E")
    print(build.to_pdf(F.sheets() + E.sheets(), "Rev-C22_Options-F-E_columns-flush"))
