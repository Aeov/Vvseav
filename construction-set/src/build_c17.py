"""Rev C17 — option C2: roof to the tall wall, tip on the plants edge in line with the end of the AC box,
edge at the tall wall kept (1754 from the facade)."""
import importlib.util
import os
import build

HERE = os.path.dirname(os.path.abspath(__file__))
WALL_EDGE = 2200 + 1260 - round(1260 * 3440 / 2540)   # 1754 — edge at the tall wall from option C (kept)
AC_END = 2260 + 800                                    # end of the AC box from the facade (verify on site)

if __name__ == "__main__":
    os.environ.update(C16_VK="V1T", C16_L=str(WALL_EDGE), C16_TRI=str(AC_END - WALL_EDGE))
    spec = importlib.util.spec_from_file_location("c17", os.path.join(HERE, "preview_c17.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    print(build.to_pdf(m.sheets(), "Rev-C17_Option-C2_Tip-at-AC-line"))
