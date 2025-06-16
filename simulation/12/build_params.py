def make_slopes_params(param_dict):
    # Start with the number of parameters
    expanded_entries = []

    # First entry is the all-zero base
    total_steps = 1 + sum(len(v) for v in param_dict.values())

    # Initialize all-zero lists of correct length
    scan_dict = {k: [0] * total_steps for k in param_dict}

    # Fill one parameter at a time (shifted by +1)
    cursor = 1  # Start after the zero baseline
    for key, values in param_dict.items():
        for v in values:
            scan_dict[key][cursor] = v
            cursor += 1

    return scan_dict
