"""Build proposal sets B, C, D: PDF + SVG + PNG previews."""
import os, subprocess
import build
import prop_b, prop_c, prop_d

OUT = build.OUT


def main():
    allp = []
    for mod, name in ((prop_b, "Proposal-B_Bioclimatic-Pergola"), (prop_c, "Proposal-C_Garden-Room-Kitchen"),
                      (prop_d, "Proposal-D_Green-Canopy-Water")):
        ss = mod.sheets()
        allp += ss
        pdf = build.to_pdf(ss, name)
        build.to_svgs(ss, name + "_svg")
        d = os.path.join(OUT, name + "_png")
        os.makedirs(d, exist_ok=True)
        subprocess.run(["pdftoppm", "-r", "110", "-png", pdf, os.path.join(d, "sheet")], check=True)
        for i, s in enumerate(ss, 1):
            src = os.path.join(d, f"sheet-{i}.png")
            if not os.path.exists(src):
                src = os.path.join(d, f"sheet-{i:02d}.png")
            os.replace(src, os.path.join(d, s.number + ".png"))
        print(pdf)
    build.to_pdf(allp, "Proposals-B-C-D_All")


if __name__ == "__main__":
    main()
