def make_slopes_params(param_dict):
    new_dict = {}
    for key in param_dict:
        new_dict[key] = [0]
    
    for key,values in param_dict.items():
        for value in values:
            for new_key in new_dict.keys():
                if new_key == key:
                    new_dict[new_key].append(value)
                else:
                    new_dict[new_key].append(0)       

    return new_dict
