def get_accs_from_txt():
    accs = []
    with open("accounts.txt", "r") as f:
        bad_accs = f.readlines()
    for acc in bad_accs:
        if acc == ['']:
            continue
        acc_dict = dict()
        acc = acc.split(':')
        if len(acc) == 2:
            acc_dict["email"] = acc[0]
            acc_dict["password"] = acc[1].strip("\n")
            acc_dict["questions"] = ['', '', '']

        elif len(acc) == 5:
            acc_dict["email"] = acc[0]
            acc_dict["password"] = acc[1]
            acc_dict["questions"] = [acc[2], acc[3], acc[4].strip('\n')]
        else:
            print('please check that you have entered all accounts correctly.')
            continue
        accs.append(acc_dict)

    return accs
