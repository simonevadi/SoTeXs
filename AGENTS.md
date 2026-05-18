# Agents Notes

## Execution Environment
Use Conda environment `rp` on local machines for simulation and ANSYS-to-Ray data-handling scripts.

## Script Conventions
Do not use `if __name__ == '__main__':` in scripts.

Define functions only when reused more than once, and keep reusable functions out of script runner files.
Place reusable utilities in helper modules (for example `postprocess_optics.py`).

Unless explicitly requested by you, do not run scripts; you run them.

Generated Ray profile `.dat` files must be Git-safe: apply resampling to keep each file around 40 MB (well below GitHub limits).
