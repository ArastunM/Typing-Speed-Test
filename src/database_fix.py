import keyboard

data = ""


def add_text(file):
    global data
    f = open(file, "a")
    data = input().split()
    for i in range(len(data)):
        f.write(data[i] + '\n')


def remove_char(file):
    global data
    f = open(file, "r")
    data = f.readlines()
    f.close()
    f = open(file, "w")
    for i in range(len(data)):
        data[i] = data[i].replace('”', '"')
        data[i] = data[i].replace('“', '"')
        data[i] = data[i].replace('’', "'")
        data[i] = data[i].replace('‘', "'")
        f.write(data[i].strip() + '\n')
    f.close()


def track_keyboard_to(file):
    global data
    rk = keyboard.record(until='Esc')
    keyboard.play(rk, speed_factor=10)
    data = input().split()
    f = open(file, "a")
    for i in range(len(data)):
        f.write(data[i] + '\n')


def lower_case_all(file):
    global data
    f = open(file, "r")
    data = f.readlines()
    f.close()

    f = open(file, "w")
    for i in range(len(data)):
        f.write(data[i].strip().lower() + "\n")
    f.close()


def length(file, check):
    global data
    avg_len = 0
    f = open(file, "r")
    data = f.readlines()

    if check == "average":
        for i in range(len(data)):
            avg_len += len(data[i].strip())
        avg_len = avg_len / len(data)

    elif check == "maximum":
        avg_len = 0
        for i in range(len(data)):
            if avg_len < len(data[i].strip()):
                avg_len = len(data[i].strip())

    elif check == "minimum":
        avg_len = 999
        for i in range(len(data)):
            if avg_len > len(data[i].strip()):
                avg_len = len(data[i].strip())

    print(avg_len)


def length_restriction(file, num):
    global data
    f = open(file, "r")
    data = f.readlines()
    for i in range(len(data)):
        if len(data[i].strip()) > num:
            data[i] = ""
    f.close()

    f = open(file, "w")
    for i in range(len(data)):
        if data[i] != "":
            f.write(data[i].strip() + "\n")
    f.close()


def repetition_removal(file):
    global data
    f = open(file, "r")
    data = f.readlines()
    for j in range(len(data)):
        for i in range(len(data)):
            if j != i:
                try:
                    if data[j].strip() == data[i].strip():
                        print(data[i].strip())
                        delete_word(file, data[i].strip())
                except IndexError:
                    pass


def delete_word(file, word):
    global data
    f = open(file, "r")
    data = f.readlines()
    for i in range(len(data)):
        if data[i].strip() == word:
            data[i] = ""
    f.close()
    f = open(file, "w")
    f.writelines(word + "\n")
    for i in range(len(data)):
        if data[i] != "":
            f.writelines(str(data[i]).strip() + "\n")
    f.close()


remove_char("gatsby.txt")
