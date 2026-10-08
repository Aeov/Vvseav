"""Rev C21 — option E, column tops painted like the fascia: rectangle to the tall wall, right edge at the end of the AC line (3.06 x 3.44), AC above."""
import importlib.util
import os
import build

HERE = os.path.dirname(os.path.abspath(__file__))
AC_END = 2260 + 800                                    # right end of the AC box from the facade (verify on site)

if __name__ == "__main__":
    os.environ.update(C16_VK="V1", C16_L=str(AC_END), C16_TRI="1260")
    spec = importlib.util.spec_from_file_location("c21", os.path.join(HERE, "preview_c21.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    print(build.to_pdf(m.sheets(), "Rev-C21_Option-E_Column-tops-white"))
