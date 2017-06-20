import glob


def anylaze_file(path):
    with open(path) as f:
        prev_type, prev_system_time, prev_logic_time = 'request', 0., 0
        for line in f:
            [_, _, _, type, system_time, logic_time, _] = line.split()
            system_time, logic_time = float(system_time), int(logic_time)
            assert system_time >= prev_system_time, 'system time'
            assert logic_time >= prev_logic_time, 'log time'
            if type == 'request':
                assert prev_type == 'request' or prev_type == 'release', 'action'
            elif type == 'acquire':
                assert prev_type == 'request', 'action'
            elif type == 'release':
                assert prev_type == 'acquire', 'action'
            prev_type, prev_system_time, prev_logic_time = type, system_time, logic_time
        else:
            print('Ok')

for filename in glob.glob('*.log'):
    anylaze_file(filename)
