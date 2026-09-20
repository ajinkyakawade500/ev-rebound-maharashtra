# The EV Rebound Effect in Maharashtra

**Can cheaper electric mobility expand access while preserving environmental savings?**

An independent research project by **Ajinkya**, exploring electric two-wheelers, household rooftop solar and travel behaviour in Maharashtra, India.

**Version 1.0.0 | 20 September 2026 | Conceptual working paper and illustrative analysis**

## Choose your edition

| Edition | Intended reader | Read online | Download |
| --- | --- | --- | --- |
| Public explainer | Anyone interested in EVs and solar | [Plain-language edition](public/EV_Rebound_Explained.md) | [Public PDF](pdf/EV_Rebound_Explained.pdf) |
| Academic working paper | Research and academic audiences | [Academic edition](academic/EV_Rebound_Working_Paper.md) | [Academic PDF](pdf/EV_Rebound_Working_Paper.pdf) |

## What the project argues

Cheaper travel may encourage additional journeys. Evaluating those journeys requires separating travel growth, energy savings, emissions and the value of improved access. Rooftop solar can change charging economics, but a low bill does not automatically mean zero economic cost or zero-emission charging.

The numerical examples are **assumed scenarios**. This repository does not contain an estimated Maharashtra rebound rate, a household survey or evidence that EV adoption causes local GDP growth. The proposed field study has not been conducted.

![Impact sensitivity to additional travel under hypothetical intensity ratios](figures/impact_sensitivity.png)

## What is included

- Two complete editions in editable Markdown and PDF.
- Explicit scenario assumptions and a standard-library Python calculator.
- Generated CSV results and reproducible figures.
- A source register, claim audit and bibliographic references.
- A proposed longitudinal study with identification and measurement limitations.
- A publication guide and GitHub citation metadata.

## Reproduce the analysis

From this repository's root directory, using Python 3.10 or later:

```bash
python analysis/reproduce.py
python analysis/check_model.py
```

The calculator needs no third-party packages and makes no network requests. It writes four CSV files to `results/`. All inputs are in [assumptions.json](analysis/assumptions.json); the outputs are deterministic. The checks cover arithmetic and accounting identities, not empirical validity.

To regenerate the figures and PDFs:

```bash
python -m pip install -r requirements-build.txt
python analysis/make_figures.py
python scripts/build_pdfs.py
```

PDF building requires DejaVu Sans and DejaVu Serif fonts. See [BUILD.md](BUILD.md) for font configuration and dependency versions. The PDF build reads the Markdown source, so substantive edits should be made there first.

## Evidence and interpretation

See [the source register](references/SOURCE_REGISTER.md) for document-specific evidence, [the claim audit](references/CLAIM_AUDIT.md) for corrections to the original draft and [references.bib](references/references.bib) for citations. Policy sources are dated and scoped; no individualized tariff calculation is supplied.

The author supplied the initial concept and draft. OpenAI ChatGPT assisted substantially with research, writing, analysis code and document preparation. See [AUTHORSHIP.md](AUTHORSHIP.md). This is a working paper, not a peer-reviewed publication. No university affiliation or endorsement is claimed.

## Cite and reuse

Ajinkya. (2026). *Low-Cost Electric Mobility and Travel Rebound in Maharashtra: A conceptual framework, illustrative scenarios and a research design for electric two-wheelers and rooftop solar* (Version 1.0.0). Independent working paper.

Project repository: [ajinkyakawade500/ev-rebound-maharashtra](https://github.com/ajinkyakawade500/ev-rebound-maharashtra). GitHub citation metadata, including the repository URL, is provided in [CITATION.cff](CITATION.cff). No DOI has been assigned. Reuse terms have not been selected; see [RIGHTS.md](RIGHTS.md).

## Next research milestone

Pilot a household travel-and-charging diary, assess measurement quality, and develop a feasible comparison-group design before claiming causal effects. Suggestions or corrections should identify the relevant claim, source and proposed change.
