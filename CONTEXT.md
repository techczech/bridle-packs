# Bridle Packs Context

This repository holds Bridle Script Packs: builder-side folders that package reviewed Skill scripts, locked environments, dependency facts, probes, managed asset declarations, and golden evidence.

Packs carry facts. Bridle Host Apps carry judgement by granting scoped Manifest capabilities to selected pack entries. Nothing in this repository is executable or downloadable for an end user by itself.

## Terms

**Script Pack**:
A folder under `packs/` with `PACK.md`, scripts, locked environments, install playbooks, and golden evidence.

**PACK.md**:
The typed manifest for a pack. It declares pack identity, source Skill, scripts, probes, dependency licence facts, managed assets, and consent text.

**Probe**:
A non-installing check for a system dependency or platform property. Probes report availability only; they never install missing tools.

**Managed Asset**:
A deferred download such as model weights. Managed assets require declared size, source, checksum, and consent text. They are not committed to this repository.

**Golden Evidence**:
Reviewed output under a pack's `golden/` folder proving a load-bearing path works on a real input.
