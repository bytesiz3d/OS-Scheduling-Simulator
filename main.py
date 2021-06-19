from process import Process
from scheduler import RM_Scheduler, FFRM_Scheduler
from graph import Graph

class Demo:
    @staticmethod
    def RM():
        ps = [
            Process(0, 2, 2, 12),
            Process(7, 1, 3, 6),
            Process(14, 1, 4, 4),
        ]
        print(Process.to_table(ps))

        time = 24
        schedule = RM_Scheduler.schedule(ps, time)
        Graph.plot(schedule, time, 'Rate Monotonic')

    @staticmethod
    def plot_first_fit_RM():
        mp_sch = [
            [ 1, 2, 4, 8 ] * 5,
            [ 1, 2, 4, 8 ] * 5,
            [ 1, 2, 4, 8 ] * 5,
            [ 1, 2, 4, 8 ] * 5,
        ]
        Graph.plot_multiple(mp_sch, 20)

    @staticmethod
    def FFRM():
        ps = [
            Process(0, 1, 0, 2),
            Process(1, 1, 0, 3),
            Process(2, 1, 0, 4),
            Process(3, 1, 0, 5),
            Process(4, 1, 0, 6),
            Process(5, 1, 0, 7),
            Process(6, 1, 0, 8),
            Process(7, 1, 0, 9),
        ]
        print(Process.to_table(ps))

        time = 24
        mp_schedule = FFRM_Scheduler.schedule(ps, 3, time)
        Graph.plot_multiple(mp_schedule, time)


# Demo.plot_first_fit_RM()
# Demo.RM()
Demo.FFRM()
