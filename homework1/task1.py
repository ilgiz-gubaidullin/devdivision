nums = [849, 200, 809, 164, 926, 84, 892, 666, 880, 869, 775, 707, 874, 195, 120, 275, 328, 228, 43, 445, 421, 246, 666, 324, 107, 455, 632, 666, 468, 603, 500]

do_print = True
odd_number = False

for i in nums:
    if i == 666:
        do_print = not do_print
        if not do_print:
            odd_number = not odd_number
        continue
    if do_print and i % 2 != odd_number:
        print(i, end=' ')


