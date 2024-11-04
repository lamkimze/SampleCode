import sys
"""
Name: Kim Ze Lam
Student ID: 31860346
"""
def Boyer_Moore(text, pat):
    result = []
    bc_table = bad_char_table(pat)
    gs_table = build_gs_table(pat)
    mp_table = build_mp_table(pat)
    dot_exist = False
    end = False
    pause = -1
    resume = -1
    shift  = 0
    counter = 0

    # check accept only one wildcard
    for i in pat:
        if ord(i) == 46 and dot_exist == True:
            end = True
        elif ord(i) == 46 and dot_exist == False:
            dot_exist = True


    if end == False:
        while (len(pat) + shift <= len(text)):
            bad_detected = False
            dot_in_text = 0 
            for i in range(len(pat) -1, -1, -1):
                # do not compare previous compared character
                # galil optimization
                if not(i > resume + 1 and i < pause):
                    counter += 1
                    # refer the array where the wildcard refer to
                    if ord(pat[i]) == 46:
                        dot_in_text = ord(text[shift + i]) - 97
                    # mismatch occur
                    if ord(pat[i]) != 46 and pat[i] != text[i + shift]:
                        # shift with bad character table
                        bad_char_shift = max(1, i - max(bc_table[ord(text[shift + i])-97][i], bc_table[26][i]))
                        # shift with good suffix value when it is not 0
                        if gs_table[dot_in_text][i + 1] > 0:
                            gsmp_shift = len(pat) - gs_table[dot_in_text][i + 1]
                        #shift with matched prefix when good suffix on current index is 0
                        elif gs_table[dot_in_text][i + 1] == 0:
                            gsmp_shift =  len(pat) - mp_table[dot_in_text][i + 1]
                        # shift with the largest among bad character shift, good suffix and matched prefix
                        if bad_char_shift > gsmp_shift:
                            pause = resume = shift + i
                            shift += bad_char_shift
                        else:
                            resume = i
                            pause = i + gsmp_shift
                            shift += gsmp_shift
                        bad_detected = True
                        break
            # matched found
            if bad_detected == False:
                pause = -1
                resume = -1 
                result.append(shift + 1)
                shift += len(pat) - mp_table[dot_in_text][1]
        return result
    else:
        return -1

def bad_char_table(pat):
    """
    creating bad character table
    """
    accepted_char = 27
    bc_table = [[-1]*len(pat) for _ in range(accepted_char)]

    for i in range(len(pat)-1):
        if (ord(pat[i]) == 46):
            bc_table[accepted_char-1][i+1] = i
        else:
            bc_table[ord(pat[i]) - 97][i+1] = i
    
    for i in range(accepted_char):
        cur_val = -1
        for j in range(len(bc_table[i])):
            if bc_table[i][j] == -1:
                bc_table[i][j] = cur_val
            else:
                cur_val = bc_table[i][j]
    
    return bc_table

def build_gs_table(pat):
    # refer to lecture week 2 slide 18
    wildcard = -1

    # find the position of wildcard
    for i in range(len(pat)):
        if ord(pat[i]) == 46:
            wildcard = i
            break
    
    z_flipped = []
    gs_table = [[0]*(len(pat) + 1) for _ in range(26)]

    # there is a wildcard inside the string case
    if wildcard > -1:
        copy_arr = []
        for i in pat:
            copy_arr.append(i)
        
        # generate every single possibility of character at the position wildcard
        for j in range(26):
            copy_arr[wildcard] = chr(j + 97)
            z_flipped.append(flipped_z_algorithm(copy_arr))

        for k in range(26):
            for p in range(len(pat) - 1):
                j = len(pat) - z_flipped[k][p]
                gs_table[k][j] = p + 1
        
    # no wildcard is in the string
    else:
        z_flipped = flipped_z_algorithm(pat)

        for p in range(len(pat) - 1):
            j = len(pat) - z_flipped[p]
            gs_table[0][j] = p + 1
            
    return gs_table

def build_mp_table(pat):
    wildcard = -1

    # find the position of wildcard
    for i in range(len(pat)):
        if ord(pat[i]) == 46:
            wildcard = i
            break

    mp_table = [[0]*(len(pat)) for _ in range(26)]
    instant = []

    # wildcard exist in the string
    if wildcard > -1:
        for i in pat:
            instant.append(i)
        
        # replace the wildcard with every possible characters 
        for i in range(26):
            max_val = -1
            instant[wildcard] = chr(i + 97)
            instant_z_suffix = flipped_z_algorithm(instant)

            for j in range(len(instant_z_suffix)):
                if instant_z_suffix[j] > max_val:
                    max_val = instant_z_suffix[j]
                mp_table[i][len(instant_z_suffix) - j - 1] = max_val
    # no wildcard exist in the string
    else:
        max_val = -1
        instant_z_suffix = flipped_z_algorithm(pat)
        for j in range(len(instant_z_suffix)):
            if instant_z_suffix[j] > max_val:
                max_val = instant_z_suffix[j]
            mp_table[0][len(instant_z_suffix) - j - 1] = max_val

        
    return mp_table

def flipped_z_algorithm(pat):
    flipped_pat = []
    flipped_z_val = []
    for i in range(len(pat)):
        flipped_pat.append(pat[len(pat) - i - 1])

    z_val = z_algorithm(flipped_pat)
    
    for j in range(len(z_val)):
        flipped_z_val.append(z_val[len(z_val) - j - 1])

    return flipped_z_val

def z_algorithm(inputString):
    z_value = [0]*len(inputString)
    zbox_left = 0
    zbox_right = 0
    z_value[0] = len(inputString)
    
    i = 1
    while i < len(inputString):
        
        if i > zbox_right and i < len(inputString):
            zbox_left = zbox_right = i
            while(zbox_right < len(z_value) and (inputString[zbox_right] == inputString[zbox_right - zbox_left] )):
                zbox_right += 1
            z_value[i] = zbox_right - zbox_left
            zbox_right -= 1

        else:
             k = i - zbox_left
             remaining = zbox_right - i + 1

             if z_value[k] < remaining:
                z_value[i] = z_value[k]
             elif z_value[k] > remaining:
                    extended_value = remaining
                    x = zbox_right + 1
                    front_val = k
                    while(x < len(z_value) and (inputString[x] == inputString[front_val])):
                        x += 1
                        front_val += 1
                        extended_value += 1
                    z_value[i] = extended_value
                        
             elif z_value[k] == remaining:
                zbox_left = i
                while(zbox_right < len(z_value) and (inputString[zbox_right] == inputString[zbox_right - zbox_left])):
                    zbox_right += 1
                z_value[i] = zbox_right - zbox_left
                zbox_right -= 1

        i += 1
    return z_value

def openfile(filename):
    mystring = ""

    myfile = open(filename)
    for line in myfile:
        mystring += line.strip()

    myfile.close()
    return mystring

def writefile(result, outfile):
    for t in result:
        outfile.write(str(t) + '\n')

if __name__ == '__main__':
    # print(Boyer_Moore("abbabbababaababbaaaaabbbbbbabaaaababa", "aaabbb."))
    # print(Boyer_Moore("aabaacaadaabaaba", ".aba"))
    # print(Boyer_Moore("aababcabcdabcdeabcdef", ".aba"))
    # print(Boyer_Moore("aabaacaadaabaaba", "a.ba"))
    # print(Boyer_Moore("aababcabcdabcdeabcdef", "a.ba"))
    # print(Boyer_Moore("bbbbbababbbbbabb", "bb.bb"))

    _, filename1, filename2 = sys.argv
    
    print("Number of arguments passed : ", len(sys.argv))

    print("First argument : ", filename1)
    print("Second argument : ", filename2)

    text = openfile(filename1)
    print("\nContent of text : ", text)

    pat = openfile(filename2)
    print("\nContent of pattern : ", pat)

    outFile = open("q2_result.txt", 'w')
    writefile(Boyer_Moore(text, pat), outFile)
    outFile.close()