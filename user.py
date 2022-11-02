from PyInquirer import prompt, print_json
user_questions = [
    {
        "type":"input",
        "name":"name",
        "message":"Enter your name"
    },
]

def add_user():
    user = prompt(user_questions)
    f = open("users.csv", "a")
    f.write(user['name'] + "\n")
    f.close()
    return True

def existing_user():
    res = []
    f = open("users.csv", "r")
    for user in f:
        res.append(user)
    f.close()
    return res

def existing_user_dict():
    res = []
    f = open("users.csv", "r")
    for u in f:
        res.append({'name': u})
    f.close()
    return res