from copy import deepcopy
from process import Process

class Scheduler:
    @staticmethod
    def _static_schedule(processes: list, time: int) -> list:
        if processes is None:
            return None

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

    @staticmethod
    def schedule(processes: list, time: int) -> list:
        return Scheduler._static_schedule(processes, time)

class RM_Scheduler(Scheduler):
    @staticmethod
    # RM Utilization test
    def _utilization_bound(n: int) -> float:
        return n * (2 ** (1/n) - 1)

    @staticmethod
    def schedule(processes: list, time: int) -> list:
        # Sort by ascending period lengths
        p_sorted = sorted(deepcopy(processes), key=lambda p: p.period)

        # Schedule if it passes the utilization test
        util = Process.utilization(processes)
        if util <= RM_Scheduler._utilization_bound(len(processes)):
            return Scheduler._static_schedule(p_sorted, time)

        return None

class DM_Scheduler(Scheduler):
    @staticmethod
    def schedule(processes: list, time: int) -> list:
        # Sort by ascending deadlines
        # As relative deadlines match the initial deadline if all processes were released together at 0
        p_sorted = sorted(deepcopy(processes), key=lambda p: p.deadline)
        return Scheduler._static_schedule(p_sorted, time)


class Priority_Scheduler(Scheduler):
    @staticmethod
    def schedule(processes: list, time: int) -> list:
        p_sorted = sorted(deepcopy(processes), key=lambda p: p.priority)
        return Scheduler._static_schedule(p_sorted, time)

class MP_Scheduler(Scheduler):
    @staticmethod
    def schedule(processes: list, n_processors: int, time: int) -> list:
        return Scheduler._static_schedule(processes[0], time)


class FFRM_Scheduler(MP_Scheduler, RM_Scheduler):
    @staticmethod
    def schedule(processes: list, n_processors: int, time: int) -> list:
        # Sort by ascending period lengths
        p_sorted = sorted(deepcopy(processes), key=lambda p: p.period)

        assigned_to = [[]] * n_processors
        util_info = [tuple()] * n_processors
        for process in p_sorted:
            for processor in range(n_processors):
                # Attempt to assign the process to the first processor
                p_list = deepcopy(assigned_to[processor])
                p_list.append(process)

                # Continue if the assignment passes the utilization test
                util = Process.utilization(p_list)
                util_bound = RM_Scheduler._utilization_bound(len(p_list))
                if util <= util_bound:
                    assigned_to[processor] = p_list
                    util_info[processor] = (util, util_bound)
                    break

        separator = '\r' + '\t' * 4
        for processor in range(n_processors):
            p_list = list(map(lambda p: p.pid, assigned_to[processor]))
            u, ub = util_info[processor]
            print(f'P{processor} is assigned {p_list}{separator}U = {u} <= {ub}')

        return [Scheduler._static_schedule(ps, time) for ps in assigned_to]
