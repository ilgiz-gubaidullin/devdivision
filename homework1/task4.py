some_list = [1, 4, 6, 9, 2, 3, 5]
# [5, 3, 2, 9, 6, 4, 1]

# 1)
some_list.reverse()
print(some_list)

# 2)
a = some_list[::-1]
print(a)

# 3)
print(list(reversed(some_list)))

# 4)
for i in some_list[::-1]: print(i, end=' ')