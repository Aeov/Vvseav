# Courtyard Canopy & Garden Terrace — Construction Drawings

Drawings for the rear courtyard shown in the client renders: a timber-soffit canopy, a raised planter, three-tone paving and lattice joinery. Three alternative proposals follow.

## Deliverables (`output/`)

| File | What it is |
|---|---|
| `Design-A_Construction-Set.pdf` | **Design A (as rendered)**: 20 A3 sheets, construction issue |
| `Design-A_CAD-1to1.dxf` | Plans, elevations, sections and framing at 1:1 in mm, on named layers, for CAD |
| `BOQ_Design-A.xlsx` | Bill of quantities with blank rate and total columns ready for tender |
| `Design-A_png/` and `Design-A_svg/` | Each sheet as an image or vector file |
| `Proposal-B_Bioclimatic-Pergola.pdf` | B: freestanding motorised louvre pergola, built-in bench, porcelain paving |
| `Proposal-C_Garden-Room-Kitchen.pdf` | C: glulam garden room with a glass roof and an outdoor kitchen |
| `Proposal-D_Green-Canopy-Water.pdf` | D: sedum green-roof canopy, reflecting pool, living wall, rainwater harvesting |
| `Proposals-B-C-D_All.pdf` | All three proposals in one file |

## Design A sheet list

A-000 cover and 3D axonometric · A-001 notes and specification · A-002 construction sequence and hold points ·
A-100 setting-out plan · A-101 paving colour map, levels and drainage (1,302 pavers counted) · A-102 canopy roof plan ·
A-103 reflected ceiling plan, lighting and power · A-104 planting and irrigation · A-200 Elevation A 1:25 · A-201 Elevations B and C ·
A-300 Section A-A 1:20 · A-301 Section B-B 1:25 · A-302 planter section and drainage details · A-500 and A-501 details ·
A-600 doors and screens · S-001 structural design basis and calcs · S-100 framing plan · S-101 connections, foundations and member schedule · Q-001 BOQ

## Before building

- **Survey first.** Existing dimensions, levels, the annex ring beam and slab, and buried services are assumed values. They are marked "verify" on the drawings.
- **Engineer sign-off.** Steel sizes and calcs are preliminary; they use Eurocode loads, with snow and wind assumed. A licensed local engineer must confirm them and stamp the drawings.
- **Choose the corner support.** For the east front corner of the canopy, choose **S1** (cantilever, as in the render, which needs the annex slab and pier to be verified) or **S2** (one extra post P3, which is simpler and cheaper).

## Regenerating

```bash
cd construction-set/src
python3 build_all.py     # Design A: PDF + SVG + DXF + XLSX
python3 build_props.py   # Proposals B, C, D
```

All dimensions come from `src/design.py`. Change a value there and rebuild to update every sheet.
