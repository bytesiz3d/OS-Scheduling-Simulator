import numpy as np
import matplotlib.pyplot as plt

class Graph:
  # -1 for idle
    @staticmethod
    def _plot_single(ax, schedule: list, t: np.ndarray, title: str = None):
        # Append the last scheduled process to include the final minor cycle
        schedule.append(schedule[-1])

        unique = np.unique(schedule)
        # Insert idle tick
        if -1 not in unique:
            unique = np.insert(unique, 0, -1)

        def map_unique(p):
            idx = np.searchsorted(unique, p)
            return idx

        # Map processes to uniform heights
        mapped = np.vectorize(map_unique)(schedule)

        # Set yticks
        mapped_labels = np.unique(mapped)
        # Label @ mapped_height = index in unique values
        ytx = [f'P{unique[p]}' for p in mapped_labels]

        # Remove idle tick
        if mapped_labels[0] == 0:
            mapped_labels = mapped_labels[1:]
            ytx = ytx[1:]

        ax.set_yticks(mapped_labels)
        ax.set_yticklabels(ytx)
        ax.set_xticks(t)
        ax.set_xticklabels(t)
        ax.fill_between(t, mapped, step='post', alpha=0.4)
        ax.grid(alpha=0.25, axis='y')

        if title is not None:
            ax.set(title=title)
            print(title, np.array(schedule[:-1]))

    @staticmethod
    def plot(schedule: list, time: int, title: str = None):
        # Add one to include the final minor cycle
        t = np.arange(time + 1, dtype=int)
        fig, ax = plt.subplots()

        Graph._plot_single(ax, schedule, t, title)
        plt.show()

    '''
    Here `mp_schedule` is a list of schedules basically, one for each processors
    '''
    @staticmethod
    def plot_multiple(mp_schedule: list, time: int, title: str = None):
        processor_count = len(mp_schedule)

        # Create subplots for each processor
        ncols = min(processor_count, 2)
        nrows = (processor_count + ncols - 1) // ncols # ceil(processor_count/ncols)
        fig, axs = plt.subplots(nrows, ncols)

        # Add one to include the final minor cycle
        t = np.arange(time + 1, dtype=int)

        # Set ticks for each subplot
        for i, ax in enumerate(axs.flat):
            if i >= processor_count:
                ax.axis('off')
            else:
                Graph._plot_single(ax, mp_schedule[i], t, f'Processor #{i}')

        if title is not None:
            fig.suptitle(title)
        fig.tight_layout()
        plt.show()
