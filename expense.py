from PyInquirer import prompt
from user import existing_user, existing_user_dict

expense_questions = [
    {
        "type":"input",
        "name":"amount",
        "message":"New Expense - Amount: ",
    },
    {
        "type":"input",
        "name":"label",
        "message":"New Expense - Label: ",
    },
    {
        "type":"rawlist",
        "name":"spender",
        "message":"New Expense - Spender: ",
        'choices': existing_user()
    },
    {
        "type":"checkbox",
        "name":"payback",
        "message":"New Expense - Payback: ",
        'choices': existing_user_dict(),
    }
]

def update_expense_questions():
    expense_questions[2]['choices'] = existing_user()
    expense_questions[3]['choices'] = existing_user_dict()
    return expense_questions


def new_expense(*args):
    update_expense_questions()
    infos = prompt(expense_questions)

    res = infos['amount'] + "," + infos['label'] + "," + infos['spender'][:-1]

    nb_user_payback = len(infos['payback'])
    amount_payback = float(infos['amount']) / nb_user_payback

    f = open("expense_report.csv", "a")
    for user in infos['payback']:
        res += "," + str(amount_payback) + "," + infos['label'] + "," + user[:-1]

    f.write(res + "\n")
    f.close()
    return True

def show_status(*args):
    owes = {}
    f = open("expense_report.csv", "r")
    for line in f:
        line = line[:-1]
        infos = line.split(",")
        if infos[2] not in owes:
            owes[infos[2]] = float(infos[0])
        else:
            owes[infos[2]] += float(infos[0])
        for i in range(4, len(infos), 3):
            if infos[i + 1] not in owes:
                owes[infos[i + 1]] = -float(infos[i - 1])
            else:
                owes[infos[i + 1]] -= float(infos[i - 1])
    for user in owes:
        if owes[user] < 0:
            for user2 in owes:
                if owes[user2] > 0:
                    if owes[user2] > abs(owes[user]):
                        print(user + " owes " + str(abs(owes[user])) + "€ to " + user2)
                        owes[user2] -= abs(owes[user])
                        owes[user] = 0
                    else:
                        print(user + " owes " + str(owes[user2]) + "€ to " + user2)
                        owes[user] += owes[user2]
                        owes[user2] = 0
        else:
            print(user + " owes nothing")
    f.close()
    return True