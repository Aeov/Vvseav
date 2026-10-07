"""FINAL TECHNICAL DESIGN — V2T courtyard roof (triangle + 0.90 m void + 2 stainless hangers).

Shared base for every TD-xxx sheet: the agreed geometry (re-exported from the client-check module), grids, setting-out,
levels, member marks / specification, and the final title block (FinSheet).

Agreed with the client (Rev C07..C14):
  * annex side wall and low white garden wall are ONE continuous line (Y = 0); the roof's plants-edge fascia is on it;
  * roof void edge (Y = 2540) is in line with the annex wall on the passage / wooden-door side;
  * triangular roof: plants edge 3.22 + 1.26 = 4.48, void edge 3.22, raked edge 2.84, 0.90 m void to the tall wall,
    void edge hung from the tall wall on 2 Ø16 stainless hangers (H1, H2);
  * planter 0.70 inside the garden wall (0.55 soil + 0.15 white kerb), from X = 9000, continuing; paved entry 1.00 at the
    door; low planting + star jasmine on the posts and wall wires, LED uplights (planting codes P1..P4, L1);
  * columns C1 / C2: SHS 150 clad 200x200 thermo-ash, against the garden wall, fixed to it.
Axes: X along the annex (annex 0..8000, end facade + roof start at X = 8000); Y across (garden wall outer face Y = 0,
tall wall face Y = 3440); Z up from ±0.000 = paving / FFL at the door.
"""
import math
from cad import Sheet, View, break_line, MAT, _f  # noqa: F401
import preview_c13 as G  # noqa: F401  (agreed geometry + drawing helpers)
from preview_c13 import (  # noqa: F401
    HOUSE_L, HOUSE_W, WALL, STRIP, WALL_Y0, TW_T, LW, LW_H, PL, KERB, KERB_H, ENTRY, GARDEN_X0, GARDEN_X1, CY, ROOF_L,
    TRI, RX0, RX1, TIP, XM, SOFFIT, FASCIA, FTOP, COL_TOP, HOUSE_TOP, BOS, TOS, POST, CLAD, ENTR, SLIDES, SLIDE_W,
    LATTICE, HEAD, ROD_Z, ROD_WALL_Z, RODS_X, RED, VAR, roof_poly, rake_len, tip_angle, edge_x, inset_x, band, M, lab,
    adim, col, bracket, site_plan, axo_view, render_axo)

C = VAR["V2T"]
RD = C["roof_d"]                       # 2540 — roof depth = annex width (void edge in line with the passage-side wall)
XE = TIP                               # 12480 — triangle tip on the plants edge
COLS = C["cols"]                       # [("C1", 10240, 300), ("C2", 11880, 300)]
HANGERS = [("H1", RODS_X[0]), ("H2", RODS_X[1])]   # X = 9610, 11070
RAKE = rake_len(C)                     # ≈ 2835
TIP_ANG = tip_angle(C)                 # ≈ 63.6° between raked edge and plants edge
ROOF_AREA = (ROOF_L + ROOF_L + TRI) / 2 * RD / 1e6   # ≈ 9.78 m²
FALL = 70                              # roof falls 1:70 towards the box gutter on the raked edge
GREEN = "#3f6b2e"
BLUE = "#1f4e79"

# ---------------------------------------------------------------- setting out
SO = (HOUSE_L, 0)                      # setting-out origin: annex end facade x garden-wall outer face (verify on site)


def so(x, y):
    """model -> setting-out coordinates (mm) relative to SO."""
    return (x - SO[0], y - SO[1])


GRID_X = [("1", RX0), ("2", COLS[0][1]), ("3", COLS[1][1])]        # facade/ledger, C1, C2
GRID_Y = [("A", CY), ("B", RD - 100), ("C", WALL_Y0)]               # column line, void-edge beam, tall wall face

SET_OUT = [  # (point, description, X, Y)  — model coordinates
    ("R1", "roof corner — facade / plants edge (fascia outer face)", RX0, 0),
    ("R2", "roof tip — plants edge (fascia outer face)", TIP, 0),
    ("R3", "roof corner — raked edge / void edge", RX1, RD),
    ("R4", "roof corner — facade / void edge", RX0, RD),
    ("C1", "column C1 centre", COLS[0][1], COLS[0][2]),
    ("C2", "column C2 centre", COLS[1][1], COLS[1][2]),
    ("H1", "hanger H1 — lug on void-edge beam", RODS_X[0], RD - 100),
    ("H2", "hanger H2 — lug on void-edge beam", RODS_X[1], RD - 100),
    ("W1", "wall plate H1 on tall wall (+3.050)", RODS_X[0], WALL_Y0),
    ("W2", "wall plate H2 on tall wall (+3.050)", RODS_X[1], WALL_Y0),
    ("P0", "planter near-end kerb (entry 1.00 clear)", GARDEN_X0, LW[1]),
]

# ---------------------------------------------------------------- levels (mm above ±0.000)
LEVELS = [
    (0, "±0.000", "paving / FFL at the door (datum — tie to survey)"),
    (KERB_H, "+0.250", "planter kerb top"),
    (LW_H, "+1.400", "low garden wall top (round coping)"),
    (HEAD, "+2.200", "door / slider head"),
    (SOFFIT, "+2.360", "roof underside (soffit slats)"),
    (BOS, "+2.410", "bottom of steel (edge beams)"),
    (TOS, "+2.610", "top of steel (edge beams)"),
    (FTOP, "+2.790", "fascia top"),
    (COL_TOP, "+2.920", "column cap / annex roof"),
    (ROD_WALL_Z, "+3.050", "hanger wall plates (centre)"),
]

# ---------------------------------------------------------------- member marks & specification
STEEL = "S355J2H, hot-dip galvanised (EN ISO 1461) + polyester powder coat RAL 9010 (visible)"
MEMBERS = [  # mark, member, section, material / finish, length / qty, connection refs
    ("B1", "Ledger on annex end facade", "UPN 200", "S275JR HDG", "2240 · 1 no.", "D1 — M12 A4 resin anchors @ 400"),
    ("B2", "Plants-edge beam on C1 / C2", "RHS 200x100x6.3", "S355J2H HDG + PPC", "≈ 4090 · 1 no.", "D7, D9"),
    ("B3", "Void-edge beam (hung from H1/H2)", "RHS 200x100x6.3", "S355J2H HDG + PPC", "≈ 3030 · 1 no.", "D3, D9"),
    ("B4", "Raked-edge beam (gutter side)", "RHS 200x100x6.3", "S355J2H HDG + PPC", "≈ 2720 · 1 no.", "D8, D9"),
    ("J1-J3", "Roof joists, ledger -> raked beam", "C200x65x1.8 lipped", "S350GD+Z275", "3.30 / 3.56 / 3.81 m",
     "cleats 2 M12 each end"),
    ("C1, C2", "Columns against the garden wall", "SHS 150x150x8", "S355J2H HDG + PPC", "2920 · 2 no.", "D5, D6, D7"),
    ("BR", "Curved knee brackets R200", "PL 10, R 200", "S355 HDG + PPC", "3 no.", "D7 — welded / 2 M16"),
    ("H1, H2", "Hangers to the tall wall", "Ø16 rod + fork ends + turnbuckle", "stainless 1.4401 (316)",
     "≈ 1140 @ 28° · 2 no.", "D2, D3, D4"),
    ("WP", "Hanger wall plates", "PL 200x150x12", "stainless 1.4401", "2 no.", "D2 — 4 M12 A4 resin each"),
    ("WA", "Column-to-wall angles", "L 100x100x8 x 150", "stainless 1.4401", "4 no.", "D6 — 2 M12 A4 resin each"),
    ("BP", "Column base plates", "PL 250x250x15", "S355 HDG", "2 no.", "D5 — 4 M16 HD anchors"),
    ("F1, F2", "Pad footings (eccentric)", "900x800x700", "C25/30, XC2, B500C mesh", "2 no.", "D5"),
]

ROOF_BUILDUP = [  # top -> bottom
    "1.5 mm TPO membrane, light grey RAL 7035, fully adhered, welded seams",
    "18 mm WBP marine plywood deck, screwed @ 150 / 300",
    "tapered timber firrings C24 (fall 1:70 to the box gutter)",
    "C200x65x1.8 galvanised joists @ ≈ 510 between edge beams",
    "25x50 battens + 68x20 thermo-ash soffit slats @ 90 (22 open joint), black fleece behind",
]
FINISHES = [
    ("Fascia", "3 mm aluminium, PPC RAL 9010 satin, 430 high, concealed fixings, mitred at the tip"),
    ("Steel (visible)", "HDG + polyester PPC RAL 9010 satin; touch-up zinc-rich + PPC repair"),
    ("Column cladding", "25 mm thermo-ash vertical boards, concealed SS clips, oiled; 200x200 overall"),
    ("Soffit", "68x20 thermo-ash slats @ 90 mm, oiled, on 25x50 battens; black fleece"),
    ("Roof", "TPO 1.5 mm RAL 7035; aluminium PPC capping and flashings"),
    ("Hangers", "stainless 1.4401 satin, fork ends + turnbuckle + lock nuts"),
    ("LED", "24 V strip 2700 K, 10 W/m, CRI 90, IP65, in recessed aluminium profile, dimmable"),
    ("Uplights L1", "3 W 2700 K IP67 spike spots, 24 V, anthracite"),
]
PLANTING = [  # code, botanical, common, size, spacing, mature h, notes
    ("P1", "Trachelospermum jasminoides", "star jasmine", "3 L, 1.0-1.2 m", "1 / column + 1.00 m on wall",
     "climber", "on 3 mm SS wires (posts: 3 vertical; wall: +0.60 / +1.00 / +1.35)"),
    ("P2", "Pittosporum tobira 'Nana'", "dwarf pittosporum", "5 L", "0.60 m", "0.5-0.6 m", "middle row"),
    ("P3", "Lavandula ang. 'Edelweiss' / Gaura lindh. white", "white lavender / gaura", "2 L", "0.40 m",
     "0.4-0.5 m", "front row, alternating"),
    ("P4", "Erigeron karvinskianus", "Mexican daisy", "1 L", "0.30 m", "0.2-0.3 m", "kerb edge, trailing"),
    ("L1", "LED spike uplight 3 W 2700 K IP67", "uplight", "—", "1 / column + 1.20 m", "—", "24 V, driver in annex"),
]


# ---------------------------------------------------------------- project / title block
SHEETS = []          # filled by build_final: [(number, title)] — used for the register and "sheet x of N"
REVS_FINAL = [["T01", "07.10.2026", "Technical design — final issue (V2T), for tender & construction"],
              ["C14", "07.10.2026", "Client check: planting per client reference"],
              ["C13", "07.10.2026", "Client check: planter 0.70, garden wall continues"]]


def project():
    return {
        "name": "COURTYARD ROOF — V2T",
        "site": "Private residence — rear courtyard in front of the annex (site address to be inserted)",
        "client": "Owner / Client",
        "by": "Design & drawings: Claude Code",
        "date": "07.10.2026",
        "rev": "T01",
        "status": "TECHNICAL DESIGN — FINAL ISSUE FOR TENDER & CONSTRUCTION (structure subject to licensed engineer's "
                  "sign-off; verify all dimensions on site)",
        "revs": REVS_FINAL,
    }


def key_plan(s, x0, y0, w):
    """Small key plan (annex, passage, tall wall, garden wall, roof highlighted) in the title block."""
    sc = (XE + 1500 + 300) / w
    v = View(s, x0, y0, sc, origin=(-300, WALL_Y0 + TW_T))
    v.rect(-300, -400, XE + 1800, 400, w=0, fill="#e9f0e1")
    v.rect(-300, WALL_Y0, XE + 1800, TW_T, w=0.15, fill="#d9b3a0")
    v.rect(0, 0, HOUSE_L, HOUSE_W, w=0.2, fill="#efebe3")
    v.rect(HOUSE_L, 0, XE + 1500 - HOUSE_L, LW[1], w=0.15, fill="#efebe3")
    v.rect(GARDEN_X0, LW[1], XE + 1500 - GARDEN_X0, KERB[1] - LW[1], w=0.1, fill="#cfe3c0")
    v.pl(roof_poly(C), w=0.3, fill="#e0412f", opacity=0.75)
    for x in RODS_X:
        v.line(x, RD, x, WALL_Y0, w=0.2, color=RED)
    s.text(x0, y0 + (WALL_Y0 + TW_T + 400) / sc + 2.4, "KEY PLAN — roof (red), annex, garden wall, tall wall", size=1.3,
           color="#555")


class FinSheet(Sheet):
    """A3 sheet with the final-issue title block."""

    def __init__(self, number, title, scale_note="AS SHOWN", series="ARCHITECTURAL / STRUCTURAL"):
        super().__init__(number, title, scale_note, series, project=project())

    def frame(self):
        W, H = self.W, self.H
        self.rect(0, 0, W, H, lw=0, fill="#ffffff")
        self.rect(10, 5, W - 15, H - 10, lw=0.6)
        X = self.TB_X
        self.line(X, 5, X, H - 5, w=0.6)
        p = self.project
        x0 = X + 3
        w = W - 5 - X - 6
        y = 10
        self.text(x0, y + 1, p["name"], size=3.4, weight="bold")
        y += 5
        for ln in self.wrap(p["site"], w, 1.8):
            self.text(x0, y, ln, size=1.8)
            y += 2.5
        self.text(x0, y, "Client: " + p["client"], size=1.8)
        y += 2.5
        self.text(x0, y, p["by"], size=1.8)
        y += 2.6
        self.line(X, y, W - 5, y, w=0.3)
        key_plan(self, x0 + 1, y + 2.5, w - 2)
        y += 2.5 + (WALL_Y0 + TW_T + 400) / ((XE + 1800) / (w - 2)) + 4.5
        self.line(X, y, W - 5, y, w=0.3)
        y += 2.5
        notes = [
            ("B", "GENERAL NOTES"),
            "1. Do not scale. Use figured dimensions only; all dimensions in mm, levels in m above ±0.000 "
            "(paving / FFL at the door — tie to survey).",
            "2. Verify all existing dimensions, levels, walls, footings and services on site before fabrication.",
            "3. Read with TD-001 (specification & design basis) and all TD sheets; details govern over plans.",
            "4. Structure is designed to Eurocodes + Greek NA as preliminary; a licensed engineer must verify, "
            "complete and sign the structural design before fabrication.",
            "5. Setting-out origin SO = annex end facade x garden-wall outer face (TD-100).",
            "6. Report any discrepancy to the designer before proceeding.",
        ]
        y = self.textblock(x0, y, w, notes, size=1.5, gap=0.3)
        self.notes_end = y
        ry = 194
        self.line(X, ry - 4, W - 5, ry - 4, w=0.3)
        self.text(x0, ry, "REVISIONS", size=1.8, weight="bold")
        self.table(x0, ry + 1.4, [("Rev", 8), ("Date", 14), ("Description", w - 22)], p["revs"][:3], size=1.4)
        sy = 213
        self.rect(X, sy, W - 5 - X, 11, lw=0.3, fill="#111")
        for i, ln in enumerate(self.wrap(p["status"], w, 1.6)[:4]):
            self.text(x0, sy + 2.9 + i * 2.15, ln, size=1.6, weight="bold", color="#fff")
        ty = sy + 14
        self.text(x0, ty, "DRAWING TITLE", size=1.4, color="#555")
        tl = self.wrap(self.title, w, 2.9)
        for i, ln in enumerate(tl[:3]):
            self.text(x0, ty + 4.3 + i * 3.7, ln, size=2.9, weight="bold")
        fy = ty + 4.3 + 3 * 3.7 + 0.6
        self.line(X, fy, W - 5, fy, w=0.3)
        cw = (W - 5 - X) / 2
        idx = [n for n, _ in SHEETS].index(self.number) + 1 if self.number in [n for n, _ in SHEETS] else 0
        fields = [("SCALE @ A3", self.scale_note), ("DATE", p["date"]),
                  ("DRAWN / CHECKED", "CC / CC"), ("SHEET", f"{idx} of {len(SHEETS)}" if idx else "—")]
        for i, (k, v) in enumerate(fields):
            cx = X + (i % 2) * cw
            cy = fy + (i // 2) * 7.5
            self.rect(cx, cy, cw, 7.5, lw=0.2)
            self.text(cx + 1.5, cy + 2.5, k, size=1.3, color="#555")
            self.text(cx + 1.5, cy + 6.2, v, size=2.1, weight="bold")
        ny = fy + 15
        self.rect(X, ny, W - 5 - X, H - 5 - ny, lw=0.3)
        self.text(x0, ny + 3, "DRAWING No.  ·  " + self.series, size=1.3, color="#555")
        self.text(x0, ny + 12.5, self.number, size=7.2, weight="bold")
        self.text(W - 8, ny + 3, "REV", size=1.3, color="#555", anchor="end")
        self.text(W - 8, ny + 12.5, p["rev"], size=7.2, weight="bold", anchor="end")


# ---------------------------------------------------------------- shared drafting helpers
def heading(s, x, y, ref, text, scale_txt=None):
    """Bold view heading 'ref  TEXT — scale' at paper (x, y)."""
    s.text(x, y, f"{ref}  {text}" + (f" — {scale_txt}" if scale_txt else ""), size=2.1, weight="bold")
    s.line(x, y + 0.9, x + min(170, (len(ref) + len(text) + (len(scale_txt) + 3 if scale_txt else 0)) * 1.12),
           y + 0.9, w=0.35)


def grids(v, x_from, x_to, y_from, y_to, which="xy", r=2.6):
    """Grid lines + bubbles over model extents."""
    if "x" in which:
        for lb, x in GRID_X:
            v.grid(x, y_from, x, y_to, lb, end="start", r=r)
    if "y" in which:
        for lb, y in GRID_Y:
            v.grid(x_from, y, x_to, y, lb, end="start", r=r)


def legend(s, x, y, rows, size=1.4, sw=6):
    """rows: [(kind, fill/colour, text)] kind in 'box', 'line', 'dash', 'circle'. Returns end y."""
    cy = y
    for kind, col_, txt in rows:
        if kind == "box":
            s.rect(x, cy - 1.6, sw, 2.2, lw=0.2, fill=col_)
        elif kind == "line":
            s.line(x, cy - 0.5, x + sw, cy - 0.5, w=0.5, color=col_)
        elif kind == "dash":
            s.line(x, cy - 0.5, x + sw, cy - 0.5, w=0.35, color=col_, dash="2,1")
        elif kind == "circle":
            s.circle(x + sw / 2, cy - 0.5, 1.1, w=0.2, fill=col_)
        s.text(x + sw + 1.5, cy, txt, size=size)
        cy += size * 1.75
    return cy
