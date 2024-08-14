# input goal 0 lose 1 gain, level 0 beginner 1 intermediate
def detect(goal, level):
    if level == 0:
        if goal == 0:
            return "one.pdf"
        else: return "two.pdf"
    else:
        if goal == 0:
            return "three.pdf"
        else: return "four.pdf"