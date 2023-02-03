def convert_session(num):
    convert = {1:"Monday morning", 
    2:"Monday afternoon", 
    3:"Tuesday morning", 
    4:"Tuesday afternoon",
    5:"Wednesday morning",
    6:"Wednesday afternoon",
    7:"Thursday morning",
    8:"Thursday afternoon",
    9:"Friday morning",
    10:"Friday afternoon"}
    return convert[num]

def convert_prof(num):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWZYZ'
    a = num // 26
    if a == 0:
        return alphabet[num-1]
    else:
        b = num % 26
        return alphabet[a-1] + alphabet[b-1]