def isinstance_list(l, instanceof):
    return isinstance(l, list) & reduce((lambda x, y: x & isinstance(y, instanceof)), l, True)
