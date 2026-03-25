# main.py

- Shows the experimental impact test data
- Performs a least squares fit for the parameters $(E, c)$  minimizing the error between experimental restoring force, and force computed according to the HC model.
- The same is done with the proposed novel contact model

# exponent.py

- Identical as main, but optimizes also the exponent p

# data_comparison.py

- Computes the force-deformation loops according to several models il the literature and compares it to experimental datasets. bone present [2].

# References

M. A. Sherman, A. Seth, and S. L. Delp, “Simbody: multibody dynamics for biomedical research,” Procedia IUTAM,  2011.
P. Aerts, R. F. Ker, D. De Clercq, D. W. Ilsley, and R. McN. Alexander, “The mechanical properties of the human heel pad: A paradox resolved,” Journal of Biomechanics,1995.
P. Aerts and D. D. Clercq, “Deformation characteristics of the heel region of the shod foot during a simulated heel strike: The effect of varying midsole hardness,” Journal of Sports Sciences, 1993.
H. Kinoshita, T. Ogawa, K. Kuzuhara, and K. Ikuta, “In Vivo Examination of the Dynamic Properties of the Human Heel Pad,” Int J Sports Med, 1993.


# Data

barefoot: Aertz 1993, Fig.4
deceleration/displacement: Kinoshita 1993, Fig.3
