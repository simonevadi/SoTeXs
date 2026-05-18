# RayPyNG Simulation Skill

## Purpose
Use this skill whenever the user asks to "setup simulations" in this repository.

This means creating or updating a simulation family using the standard 3-file pattern:
1. `params.py`
2. `simulation_*.py`
3. `evaluation_*.py`

and ensuring all simulation scripts read RML files from the shared repo root `rml/` folder.

## Required Folder Layout (per simulation family)
Each simulation family directory under `simulation/` must contain:
- `params.py`
- one or more `simulation_*.py`
- one or more `evaluation_*.py`

Optional helpers are allowed (for example `*_helper.py`), but the 3-file pattern is mandatory.

## Responsibilities by File

### `params.py`
Define all configurable simulation inputs and shared constants:
- scan ranges and discrete scan values (energy, cff, slit sizes, orders, etc.)
- run settings (`ncpu`, `nrays`, repeats/rounds)
- simulation naming constants
- shared paths (especially RML path constants and undulator file paths)

Rules:
- Keep values centralized in `params.py`; avoid hard-coding scan ranges in simulation/evaluation scripts.
- Use deterministic names for outputs so evaluation can consume them reliably.

### `simulation_*.py`
Define and execute ray-tracing runs:
- instantiate `Simulate(...)`
- bind beamline parameters and parameter scans
- configure exports/analyzers as needed
- run simulations with project-convention runtime settings

Rules:
- RML path must resolve from repository root `rml/`, not a local `simulation/<family>/rml/` folder.
- Prefer robust path resolution using `Path(__file__).resolve().parents[2] / 'rml' / '<file>.rml'`.
- Import run/scanning values from `params.py`.

### `evaluation_*.py`
Perform post-processing of generated results:
- read simulation outputs
- compute metrics relevant to beamline performance
- generate consistent tables/plots/files for comparison across studies

Rules:
- evaluation inputs must align with names/settings defined in `params.py`.
- keep output naming stable and comparable across repeats/studies.

## Path Policy (Mandatory)
Simulation scripts must use shared RML files from:
- `<repo-root>/rml/*.rml`

Never introduce or rely on per-family RML copies under `simulation/**/rml/` unless explicitly requested for archival purposes.

## Standard Setup Checklist
When setting up a new simulation family:
1. Create or update `params.py` with all scan and runtime parameters.
2. Create or update `simulation_*.py` and wire to shared root `rml/`.
3. Create or update `evaluation_*.py` for result post-processing.
4. Confirm imports are clean and follow existing naming conventions.
5. Ensure undulator data usage is explicit (`undulator/CPMU20.csv` when relevant).
6. Validate output naming consistency between simulation and evaluation.
7. Run minimal validation checks (import sanity, path existence assumptions, script-level dry checks if available).

## Interpretation Rule for User Requests
If the user says "setup simulations":
- apply or generate the `params.py` + `simulation_*.py` + `evaluation_*.py` pattern
- centralize simulation parameters in `params.py`
- enforce root `rml/` path usage in simulation scripts
- keep evaluation script compatible with simulation outputs

## External Reference
RayPyNG API/docs are online and should be consulted when needed:
- Official docs: https://raypyng.readthedocs.io/
- Relevant sections: `Simulate`, simulation parameters, RML API helpers, and post-processing guidance.
