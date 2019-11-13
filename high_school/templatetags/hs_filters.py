from django import template

register = template.Library()


def split_string(val, arg):
    if str(arg) in str(val):
        splits = str(val).split(arg, 1)
        return splits
    else:
        return None


def get_req_params(val):
    # val will usually be like
    # val = "http://oneapply.com/dashboard/all_schools/
    #       ?query=q1&loc_bx=&loc_bk=on&page=2"
    splits = split_string(val, "?")
    par_val = {}
    # if query params exist
    if splits:
        req_params = splits[1]
        while req_params:
            splits = split_string(req_params, "=")
            if splits:
                # retrieve param name
                param = splits[0]
                rem_splits = split_string(splits[1], "&")
                if rem_splits:
                    # retrieve param value (other params left)
                    val = rem_splits[0]
                    if val:
                        # only save if val exists (takes care of empty params)
                        par_val[param] = val
                elif splits[1]:
                    # retrieve param value (no other params left)
                    val = splits[1]
                    par_val[param] = val
                if rem_splits:
                    req_params = rem_splits[1]
                else:
                    req_params = ""
            else:
                req_params = ""

    return par_val


@register.filter(name="get_querystring")
def get_querystring(val, arg):
    # val will usually be like
    # val = "http://oneapply.com/dashboard/all_schools/
    #       ?query=q1&loc_bx=&loc_bk=on&page=2"
    # arg will be the param we need to update
    # arg = "page"
    # returns the same path with updated arg
    path = str(val)
    splits = split_string(path, "?")
    # is no params exist in path
    if not splits:
        if str(arg):
            return (
                path + "?" + str(arg)
                if path[len(path) - 1] == "/"
                else path + "/?" + str(arg)
            )
        else:
            return None
    # params exist in path
    req_params = get_req_params(path)
    if str(arg):
        req_params[str(arg)] = ""
    # remove all params and reconstruct
    path = splits[0]
    if path[len(path) - 1] != "/":
        path += "/"
    for param, value in req_params.items():
        if value:
            if "?" in path:
                path += "&" + param + "=" + value
            else:
                path += "?" + param + "=" + value
    if "?" in path:
        return path + "&" + str(arg) if str(arg) else path
    else:
        return path + "?" + str(arg) if str(arg) else path


@register.filter(name="split_string_single")
def split_string_single(val, arg):
    if str(arg) in str(val):
        splits = str(val).split(arg, 1)
        return splits[1]
    else:
        return None
