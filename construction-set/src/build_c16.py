"""Rev C16 — build options C (triangle to the wall) and D (rectangle 2.20 to the wall) into one PDF."""
import importlib.util
import os
import build

HERE = os.path.dirname(os.path.abspath(__file__))
TRI_W = round(1260 * 3440 / 2540)          # same raked line as option A, continued to the tall wall


def load(vk, L, tri, name):
    os.environ.update(C16_VK=vk, C16_L=str(L), C16_TRI=str(tri))
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, "preview_c16.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


if __name__ == "__main__":
    C = load("V1T", 2200 + 1260 - TRI_W, TRI_W, "c16_C")
    D = load("V1", 2200, 1260, "c16_D")
    print(build.to_pdf(C.sheets() + D.sheets(), "Rev-C16_Roof-to-Wall_Options-C-D"))
