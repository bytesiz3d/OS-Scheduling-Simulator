class Process:
    @staticmethod
    def table_fmt(x):
        return f'{x:^8}'  # 8 places, centered

    def __init__(self, pid: int, burst: int, deadline: int, period: int, priority: int = 0) -> None:
        self.pid = pid
        self.burst = burst
        self.deadline = deadline
        self.period = period
        self.priority = priority

        self.release = 0

    def __str__(self) -> str:
        lst = [self.pid, self.burst, self.deadline, self.period, self.priority]
        strs = map(Process.table_fmt, lst)
        return ''.join(strs)

    def __repr__(self) -> str:
        lst = [self.pid, self.burst, self.deadline, self.period, self.priority]
        strs = map(str, lst)
        return f'({" ".join(strs)})'

    @staticmethod
    def to_table(processes: list) -> str:
        lst = ['ID', 'Ci', 'Di', 'Pi', 'pi']
        strs = map(Process.table_fmt, lst)
        header = ''.join(strs)
        return header + '\n' + '\n'.join([str(row) for row in processes])

    @staticmethod
    def utilization(processes: list) -> float:
        util = 0.0
        for p in processes:
            util += p.burst / p.period

        return util




