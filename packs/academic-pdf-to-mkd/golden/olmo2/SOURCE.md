---
type: golden-sample-source
paper_key: olmo2
license: CC-BY-4.0
---

# Golden sample source & attribution

This golden sample is the output of the `academic-pdf-to-mkd` pack run over a
freely-licensed academic paper, so it can ship in this public repository.

**Source paper:** *"2 OLMo 2 Furious"* by Team OLMo et al.
**arXiv:** [2501.00656](https://arxiv.org/abs/2501.00656)
**Licence:** [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)
**Attribution:** *"2 OLMo 2 Furious"* by Team OLMo et al. (Allen Institute for AI; University of Washington; New York University), arXiv:2501.00656, licensed under CC BY 4.0.

## What is committed here

- `olmo2-fulltext.md` — the extracted Markdown body (frontmatter + text).
- `tables/` — one `.md` + `.csv` per detected table (58 tables).
- `figures/` — extracted figures with per-figure caption `.md` (48 figures).

Source-page thumbnails (`pages/`) that the pack also emits are **not** committed:
they are renders of the source PDF, not conversion output, and are regenerated
on any run. Chosen deliberately as the reference case because it exercises both
**table** and **figure** extraction (unlike a slides-style talk).
