# Given ASCII input mode, validates & parses file of moves
def returnParsedStr(str_Mixup):
    str_permitted = "URFDLB'2" # String of valid characters in file
    ls_Mixup = [] # Defines initial empty list to store moves into
    isValid = True # Sets default validation output
    for i in range(len(str_Mixup)):
        # Given file contains only solver-compatible characters
        if str_Mixup[i] in str_permitted:
            # Passes if final character reached, or current character is single-quote or 2
            if (i >= len(str_Mixup)) or ((str_Mixup[i] == "'") or (str_Mixup[i] == "2")): continue
            # Appends dual characters (i.e. single-quote or 2) if such follows current character
            if (i < (len(str_Mixup) - 1)) and ((str_Mixup[i + 1] == "'") or (str_Mixup[i + 1] == "2")):
                ls_Mixup.append(str_Mixup[i] + str_Mixup[i + 1])
            else: # Appends only current character
                ls_Mixup.append(str_Mixup[i])
        else: # Otherwise, declare invalid file & terminate early
            isValid = False; break
    return ls_Mixup, isValid