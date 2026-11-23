"""Numbers reported in the manuscript, with their locations.

Each entry is (key, location, description, reported value as printed).
run_all.py rounds the reproduced value to the number of decimals printed in
the manuscript and compares. Entries printed as fractions (e.g. "1/4") are
compared exactly; "yes"/"no" entries are logical statements in the text.
"""

T52 = "Sec. 5.2, grid table (unnumbered)"

VALUES = [
    # Section 3.2 and Table 1
    ("sec32_probit_logit_shift", "Sec. 3.2, text before Table 1", "probit-to-logit shift log(2.20/1.28) (nats)", "0.54"),
    ("table1_normal", "Table 1, row 1", "G^{-1}(0.9), standard normal", "1.28"),
    ("table1_logistic", "Table 1, row 3", "G^{-1}(0.9), standard logistic", "2.20"),
    ("table1_t3", "Table 1, row 4", "G^{-1}(0.9), Student t3", "1.64"),
    ("table1_cauchy", "Table 1, row 5", "G^{-1}(0.9), Cauchy", "3.08"),
    ("table1_uniform", "Table 1, row 6", "G^{-1}(0.9), uniform on [-1,1]", "0.80"),
    ("table1_large_market", "Table 1, row 7", "G^{-1}(0.9), large market (limiting normal)", "1.28"),
    # Section 5.2 grid table
    ("grid_N2_eps", T52, "N=2: tick size eps", "0.500"),
    ("grid_N2_Khom", T52, "N=2: K*_hom", "1.332"),
    ("grid_N2_acc", T52, "N=2: correct-choice probability", "0.979"),
    ("grid_N2_excl", T52, "N=2: Delta_excl", "0.0417"),
    ("grid_N2_T", T52, "N=2: T", "0.0013"),
    ("grid_N2_sum", T52, "N=2: Delta_excl + T", "0.0429"),
    ("grid_N3_eps", T52, "N=3: tick size eps", "0.333"),
    ("grid_N3_Khom", T52, "N=3: K*_hom", "2.871"),
    ("grid_N3_acc", T52, "N=3: correct-choice probability", "0.804"),
    ("grid_N3_excl", T52, "N=3: Delta_excl", "0.0185"),
    ("grid_N3_T", T52, "N=3: T", "0.0118"),
    ("grid_N3_sum", T52, "N=3: Delta_excl + T", "0.0303"),
    ("grid_N4_eps", T52, "N=4: tick size eps", "0.250"),
    ("grid_N4_Khom", T52, "N=4: K*_hom", "4.784"),
    ("grid_N4_acc", T52, "N=4: correct-choice probability", "0.685"),
    ("grid_N4_excl", T52, "N=4: Delta_excl", "0.0104"),
    ("grid_N4_T", T52, "N=4: T", "0.0189"),
    ("grid_N4_sum", T52, "N=4: Delta_excl + T", "0.0293"),
    ("grid_N5_eps", T52, "N=5: tick size eps", "0.200"),
    ("grid_N5_Khom", T52, "N=5: K*_hom", "6.973"),
    ("grid_N5_acc", T52, "N=5: correct-choice probability", "0.622"),
    ("grid_N5_excl", T52, "N=5: Delta_excl", "0.0067"),
    ("grid_N5_T", T52, "N=5: T", "0.0227"),
    ("grid_N5_sum", T52, "N=5: Delta_excl + T", "0.0293"),
    ("grid_N6_eps", T52, "N=6: tick size eps", "0.167"),
    ("grid_N6_Khom", T52, "N=6: K*_hom", "9.377"),
    ("grid_N6_acc", T52, "N=6: correct-choice probability", "0.587"),
    ("grid_N6_excl", T52, "N=6: Delta_excl", "0.0046"),
    ("grid_N6_T", T52, "N=6: T", "0.0248"),
    ("grid_N6_sum", T52, "N=6: Delta_excl + T", "0.0294"),
    ("grid_opt_local", "Sec. 5.2, text after table", "unconstrained minimiser of Delta_excl+T over N=2..6", "4"),
    ("grid_N2_feasible", "Sec. 5.2, text after table", "N=2 feasible at Kbar=2 (K_hom <= 2)", "yes"),
    ("grid_N3_feasible", "Sec. 5.2, text after table", "N=3 feasible at Kbar=2", "no"),
    ("grid_finest_feasible", "Sec. 5.2, text after table", "finest feasible grid N", "2"),
    ("grid_eps_starstar", "Sec. 5.2, text after table", "constrained solution eps**", "1/2"),
    # Section 7.2 and Table 2
    ("ss_p_S", "Sec. 7.2 text; Table 2 row 1", "p_S", "1/4"),
    ("ss_g_S", "Sec. 7.2 text; Table 2 row 1", "g_S", "0.20"),
    ("ss_Delta_S", "Sec. 7.2 text; Table 2 row 1", "Delta_S", "0.05"),
    ("ss_Krep_S", "Sec. 7.2 text; Table 2 row 1", "K_S^rep", "5.47"),
    ("ss_p_L", "Sec. 7.2 text; Table 2 row 2", "p_L", "3/4"),
    ("ss_g_L", "Sec. 7.2 text; Table 2 row 2", "g_L", "0.20"),
    ("ss_Delta_L", "Sec. 7.2 text; Table 2 row 2", "Delta_L", "0.15"),
    ("ss_Krep_L", "Sec. 7.2 text; Table 2 row 2", "K_L^rep", "3.32"),
    ("ss_Krep_diff", "Sec. 7.2 text", "K_S^rep - K_L^rep", "2.15"),
    ("darsd_Delta_DA", "Sec. 7.2, DA/RSD example", "Delta_DA", "0.4"),
    ("darsd_Delta_RSD", "Sec. 7.2, DA/RSD example", "Delta_RSD", "0.2"),
    ("darsd_K_DA", "Sec. 7.2, DA/RSD example", "K*_DA", "1.64"),
    ("darsd_K_RSD", "Sec. 7.2, DA/RSD example", "K*_RSD", "2.79"),
    ("darsd_diff", "Sec. 7.2, DA/RSD example", "K*_RSD - K*_DA", "1.15"),
    # Appendix B.1
    ("pigou_tau_1", "App. B.1, numerical example", "tau*(1)", "1.094"),
    ("pigou_tau_2", "App. B.1, numerical example", "tau*(2)", "1.035"),
    ("pigou_tau_3", "App. B.1, numerical example", "tau*(3)", "1.013"),
]
