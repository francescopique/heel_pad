Code for the paper:
A cubic hunt-crossley contact law and subject-specific calibration improve ground reaction force prediction in musculoskeletal walking simulations,
Journal of Biomechanics,
2026,
113635,
ISSN 0021-9290,
https://doi.org/10.1016/j.jbiomech.2026.113635.

# main.py

- Shows the experimental impact test data
- Performs a least squares fit for the parameters $(E, c)$  minimizing the error between experimental restoring force, and force computed according to the HC model.
- The same is done with the proposed contact model

# exponent.py

- Identical as main, but optimizes also the exponent p.

# data_comparison.py

- Computes the force-deformation loops according to several models in the literature and compares it to experimental datasets.

# Data

H. Kinoshita, T. Ogawa, K. Kuzuhara, and K. Ikuta, “In Vivo Examination of the Dynamic Properties of the Human Heel Pad,” Int J Sports Med, 1993.

