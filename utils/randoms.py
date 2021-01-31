def institution_id(name, num):
    name_split = name.split(' ')
    initials = ''

    for name in name_split:
        initials += name[0].upper()

    bind = initials + num

    return bind


def account_id(inst, fname, lname, num):
    ifn = fname[0]
    iln = lname[0]
    inst_split = inst.split(' ')
    initials = ''

    for name in inst_split:
        initials += name[0].upper()

    bind = initials + '-' + ifn + iln + num

    return bind


def payment_id(fname, lname, term, num):
    ifn = fname[0]
    iln = lname[0]
    term = term.split(" ")
    init = ""
    for t in term:
        init += t[0].upper()

    bind = init + ifn + iln + num

    return bind