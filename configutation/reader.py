def сonfig_reader(filename):
    addresses = {}
    f = open(filename)
    for line in f:
        [pid, address, port] = line.split()
        addresses[int(pid)] = (address, int(port))
    return addresses
