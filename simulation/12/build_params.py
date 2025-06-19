def make_slopes_params(param_dict):
    new_dict = {}
    for key, value in param_dict.items():
        new_dict[key] = [0]
        new_dict[key].append(value[1])  # single value for the parameter
    for key,value_tuple in param_dict.items():
        values = value_tuple[0]
        single_value = value_tuple[1]
        for index, value in enumerate(values):
            for new_key in new_dict.keys():
                if new_key == key:
                    new_dict[new_key].append(value)
                else:
                    new_dict[new_key].append(0)     
    return new_dict
