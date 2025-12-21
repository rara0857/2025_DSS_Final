def get_longest_run(u):
    if not u:
        return 0
    max_run = 1
    current_run = 1
    for i in range(1, len(u)):
        if u[i] == u[i-1]:
            current_run += 1
        else:
            max_run = max(max_run, current_run)
            current_run = 1
    max_run = max(max_run, current_run)
    return max_run

def get_longest_period_2(u):
    if not u:
        return 0
    n = len(u)
    max_len = 0
    for i in range(n):
        for j in range(i, n):
            sub = u[i:j+1]
            is_period_2 = True
            if len(sub) > 2:
                for k in range(len(sub) - 2):
                    if sub[k] != sub[k+2]:
                        is_period_2 = False
                        break
            if is_period_2:
                max_len = max(max_len, len(sub))
    return max_len

def delete_bit(u, index_1based):
    if index_1based < 1 or index_1based > len(u):
        return u
    return u[:index_1based-1] + u[index_1based:]

def delete_burst(u, start_index_1based, length):
    if start_index_1based < 1:
        return u
    start = start_index_1based - 1
    end = start + length
    return u[:start] + u[end:]

def sticky_insertion(u, index_1based, length=1):
    if index_1based < 1 or index_1based > len(u):
        return u
    idx = index_1based - 1
    bit = u[idx]
    return u[:idx+1] + [bit]*length + u[idx+1:]
