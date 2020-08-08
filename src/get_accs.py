def get_accs_from_txt():
    accs = []
    with open("accounts.txt", "r") as f:
        bad_accs = f.readlines()
    i = 1
    for acc in bad_accs:
        if acc == ['']:
            continue
        acc.strip('\n')
        acc_dict = dict()
        acc = acc.split(':')
        if len(acc) == 2:
            acc_dict["email"] = acc[0]
            acc_dict["password"] = acc[1]

        elif len(acc) == 5:
            acc_dict["email"] = acc[0]
            acc_dict["password"] = acc[1]
            acc_dict["questions"] = [acc[2], acc[3], acc[4].strip('\n')]
        else:
            print(f'check account #{i}.')
            continue
        accs.append(acc_dict)
        i += 1

    return accs
