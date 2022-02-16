def print_sum(n):
    b = str(n)
    l = list(b)
    mapped = list(map(lambda x: int(x), l))
    print(sum(mapped))

print_sum(1234567890)

