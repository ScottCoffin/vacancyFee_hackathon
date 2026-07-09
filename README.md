# Sacramento Vacancy Fee — Data & Analysis

Supporting data, analysis, and reporting for [vacancyfee.org](https://vacancyfee.org/), a campaign to strengthen Sacramento's Vacant Lot and Vacant Building Monitoring and Enforcement Program. This repo turns county parcel and 311 service-call data into evidence for that policy fight: how many parcels sit vacant, what they're worth, and how vacancy shows up in the city's own complaint data.

## Objectives

1. **Identify vacant/underused parcels** in Sacramento County from assessor land-use codes, improvement values, and known vacant-use types (parking lots, abandoned service stations).
2. **Correlate vacancy with 311 service calls** (code enforcement, blight, homeless encampments) to show that unmanaged vacancy generates cascading costs to the city, not just to the parcel owner.
3. **Quantify the revenue case** for a graduated vacancy fee (Sacramento currently charges a flat $70/year regardless of parcel value) versus tiered fee structures used by comparable cities.
4. **Produce public-facing artifacts** — maps, charts, and a written report — usable in public comment, committee testimony, and social media, and low enough on the skill floor that hackathon volunteers (many first-time GIS/data users) could build on it in a single afternoon.

## Workflow

```
Raw county data (data/, not in git — see below)
        │
        ▼
scripts/build_hackathon_data.py  (external — produces hackathon_data/*)
        │
        ▼
hackathon_data/  ── trimmed CSV/GeoJSON/KML/GPKG + vacancy_tier classification
        │
        ▼
hackathon_data/311_analysis.ipynb   ◄── PRIMARY ANALYSIS NOTEBOOK
  Step 1-2   load 311 calls (SacCounty_SalesForce311_calls.gpkg), build a
             reproducible 50K-row beta subset for fast iteration
  Step 3-7   clean data, join council districts + parcel attributes,
             engineer "likely vacancy indicator" flags (board-up, abandoned)
  Step 8-14  interactive maps (Folium), ZIP/street-level rankings,
             seasonality, category correlation analysis
  Step 15    binomial GLM: which 311 categories predict high-likelihood
             vacancy indicators
  Step 16-18 export outputs to hackathon_data/311_analysis_outputs/,
             assert artifacts were written, build the combined
             abandoned+blight heatmap
        │
        ▼
hackathon_data/311_analysis_outputs/   (checkpoints, CSVs, PNGs, HTML maps)
        │
        ▼
march17_vacant_lot_tax_support_report.qmd   ◄── STANDALONE REPORT ARTIFACT
  Reformats the March 17 committee public comment into a
  Methods / Results / Discussion / Conclusion report, reading directly
  from the notebook's checkpoint (step6_full_joined_checkpoint.gpkg)
  and exported figures. Renders to
  march17_vacant_lot_tax_support_report.html (Quarto).
```

The notebook is the source of truth for the 311/vacancy analysis; the `.qmd` is a presentation layer on top of it and does not re-derive data independently — it reads the notebook's own checkpoint file, so re-running the notebook before rendering the report keeps the two in sync.

## Sitemap

| Path | What it is |
|---|---|
| `hackathon_data/311_analysis.ipynb` | **Primary analysis notebook.** 311 calls × parcels × council districts → vacancy indicators, maps, GLM. |
| `hackathon_data/311_analysis_outputs/` | Notebook outputs: checkpoint GeoPackage, correlation CSVs/heatmaps, ZIP/street/time-series charts, Folium HTML maps, GLM interpretation. |
| `hackathon_data/reference_data/` | Council district shapefile and a parcel reference extract used as notebook join inputs. |
| `hackathon_data/starter_notebook.ipynb` | Simplified notebook for the hackathon's "Interactive Dashboard" track (loads data, basic maps/fee calcs). |
| `hackathon_data/style_*.qml` | QGIS layer styles for parcels by vacancy tier, land use, assessed value, lot size, owner. |
| `hackathon_data/SETUP_GUIDE.md` | QGIS / Google Earth Pro / Google My Maps / Python setup instructions for hackathon participants. |
| `hackathon_data/DATA_DOWNLOAD.md` | Google Drive links for the large hackathon data files (too big for git). |
| `311_heatmap/` | Standalone exploration of which 311 `CategoryName` values are the strongest vacancy/blight signals (`ANALYSIS_NOTES.md`), plus correlation scripts/figures. |
| `parcel_actualValue/` | Market-value estimation experiments for vacant parcels (separate from the assessed land value used elsewhere). |
| `march17_vacant_lot_tax_support_report.qmd` / `.html` | **Standalone report artifact.** Methods/Results/Discussion/Conclusion writeup built from the notebook's checkpoint, for the March 17 Law & Legislation Committee hearing. |
| `Resources/` | Source material for the March 17 hearing: the county's own program discussion memo (PDF), the submitted public comment, and committee responses. |
| `hackathon_plan.md` / `.pdf` | Hackathon run-of-show: schedule, five project tracks (story map, social kit, fee calculator, heat map, dashboard), data file guide. |
| `hackathon_questions.md` | Planning Q&A that shaped the hackathon's scope and the vacancy-tier definitions. |
| `storymap_idea.md` | Notes toward a public-facing story map layout (interactive heatmap, commercial/residential sections, walking tours, empty lots). |
| `311_data.gpkg`, `311_data_beta_50k.gpkg` | Raw and subsampled 311 call GeoPackages (duplicated at repo root and in `hackathon_data/`; large, git-ignored). |
| `resources.md` | Link to vacancyfee.org. |

Root-level data referenced in `CLAUDE.md` (`data/sac_county_parcel_assessors.gpkg`, `data/sacramento_identified_parcels.csv`, etc.) is the raw upstream source for `hackathon_data/` and is not committed to this repo — see `CLAUDE.md` for schema/join details and `hackathon_data/DATA_DOWNLOAD.md` for the Google Drive copy.

## Vacancy Classification

Parcels are tagged into three tiers (`vacancy_tier` column) — see `CLAUDE.md` for full rules:

- **Tier 1 — Coded Vacant** (19,364 parcels): land use code starts with "I".
- **Tier 2 — Zero Improvement** (9,151): $0 improvement value, excluding infrastructure/parks/agriculture/government.
- **Tier 3 — Parking/Abandoned** (155): parking lots and abandoned service stations.

## Status

- **Done:** vacancy-tier parcel classification, hackathon data exports (CSV/GeoJSON/KML/GPKG), the March 17, 2026 committee hearing and submitted written comment (`Resources/march17_vacant_lot_tax_support_comment.md`, committee responses captured in `Resources/march17_committee_responses.md`), the `311_analysis.ipynb` pipeline through GLM + exported outputs, and the standalone `.qmd` report (rendered `.html` checked in).
- **In progress:** `hackathon_data/311_analysis.ipynb` and two of its exported HTML maps have local uncommitted changes as of this writing — check `git status`/`git diff` before assuming the checked-in outputs match the notebook's current state.
- **Not yet started / open:** the `storymap_idea.md` layout has not been built; `parcel_actualValue/` market-value estimation is exploratory and not yet wired into the main report; no automated regeneration (the `.qmd` depends on manually re-running the notebook first).
