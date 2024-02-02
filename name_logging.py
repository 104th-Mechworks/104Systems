with open("names.txt", "r") as f:
    lines = f.readlines()
    lines.reverse()
    with open("names_reverse.txt", "w") as f:
        for line in lines:
            f.write(f"{line}")