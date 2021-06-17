import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt


class Process:
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

    def to_table(processes) -> str:
        lst = ['ID', 'Ci', 'Di', 'Pi', 'pi']
        strs = map(Process.table_fmt, lst)
        header = ''.join(strs)
        return header + '\n' + '\n'.join([str(row) for row in processes])


class Scheduler:
    def static_schedule(processes: list[Process], time: int) -> list[int]:
        t = 0
        schedule = []

        while t < time:
            # Process is awaiting its next period, move to the next process
            p_index = 0
            while p_index < len(processes) and processes[p_index].release > t:
                p_index += 1

            # No available process was found, idle
            if (p_index >= len(processes)):
                schedule.append(-1)
                t += 1
                continue

            # Run the proper process to completion
            p = processes[p_index]
            p.release += p.period
            runtime = min(p.burst, time - t)

            schedule.extend([p.pid] * runtime)
            t = t + p.burst

        return schedule

    def priority(processes: list[Process], time: int) -> list[int]:
        p_sorted = sorted(deepcopy(processes), key=lambda p: p.priority)
        return Scheduler.static_schedule(p_sorted, time)

    def rate_monotonic(processes: list[Process], time: int) -> list[int]:
        # Sort by ascending period lengths
        p_sorted = sorted(deepcopy(processes), key=lambda p: p.period)
        return Scheduler.static_schedule(p_sorted, time)

    def deadline_monotonic(processes: list[Process], time: int) -> list[int]:
        # Sort by ascending deadlines
        # As relative deadlines match the initial deadline if all processes were released together at 0
        p_sorted = sorted(deepcopy(processes), key=lambda p: p.deadline)
        return Scheduler.static_schedule(p_sorted, time)

    # -1 for idle
    def plot(schedule: list[int], time: int, title: str = None):
        # Add one to include the final minor cycle
        t = np.arange(time + 1)
        plt.xticks(t)

        # Append the last scheduled process to include the final minor cycle
        # Add one to raise P0
        schedule.append(schedule[-1])
        schedule = np.array(schedule) + 1

        # Set yticks
        p = np.unique(schedule)
        if 0 in p: p = p[1:]  # Remove idle tick

        ytx = [f'P{i-1}' for i in p]
        plt.yticks(p, ytx)

        # Plot
        plt.fill_between(t, schedule, step='post', alpha=0.4)
        plt.grid(alpha=0.25)

        if title is not None:
            print(title, np.array(schedule))
            plt.title(title)
        plt.show()


ps = [
    Process(0, 2, 2, 12),
    Process(1, 1, 3, 6),
    Process(2, 1, 4, 4),
]
print(Process.to_table(ps))

time = 24
schedule = Scheduler.rate_monotonic(ps, time)
Scheduler.plot(schedule, time, 'Rate Monotonic')

schedule = Scheduler.deadline_monotonic(ps, time)
Scheduler.plot(schedule, time, 'Deadline Monotonic')
