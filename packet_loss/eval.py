t_0 = 1
t_1 = lambda a, b, p: 1 + (a/100)*(b*1e6)*(p/1000) / 12e3

def b_1(a, b, p):
    bandwidth = t_0 / t_1(a, b, p) * b
    return f'{bandwidth:.1f}'

a_list = [0.1, 0.5, 1, 3, 10]
p_list = [1, 2, 4, 10, 20, 50, 100, 200, 500]
b_list = [
    ('Fast Ethernet', 100),
    ('Gigabit Ethernet', 1000),
    ('3G download', 7.2),
    ('4G download', 150),
]

def make_row(items):
    return '| ' + ' | '.join(items) + ' |'

for description, b in b_list:
    print(f'#### {description}, {b} Mbit/s')
    print(make_row([
        'Ping',
        *[f'Packet loss={a}%' for a in a_list]
    ]))
    print(make_row([
        '---' for _ in range(1 + len(a_list))
    ]))

    for p in p_list:
        print(make_row([
            f'{p}ms',
            *[f'{b_1(a, b, p)} Mbit/s' for a in a_list]
        ]))

    print()

