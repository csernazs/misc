#!/usr/bin/python3

from pprint import pprint
from collections import defaultdict


class Workers:
    def __init__(self, amount):
        self.workers = [0] * amount
        self.labels = [None] * amount
        self.elapsed = 0
        self.completed = []

    def assign_work(self, time, label):
        next_worker_idx = self.get_next_idle()
        if next_worker_idx is None:
            return False

        self.workers[next_worker_idx] = time
        self.labels[next_worker_idx] = label
        print("worker started working on", label, "for", time)
        return True

    def can_assign(self):
        return self.get_next_idle() is not None

    def get_next_idle(self):
        for idx, worker in enumerate(self.workers):
            if worker == 0:
                return idx
        return None

    def advance_time(self, time):
        if time == 0:
            return

        workers = []
        labels = []
        time_spent = []
        for worker, label in zip(self.workers, self.labels):
            remaining = worker - time
            if remaining < 0:
                remaining = 0
                time_spent.append(worker)
            else:
                time_spent.append(time)

            workers.append(remaining)
            if remaining == 0:
                labels.append("")
                print(label, "completed")
                self.completed.append(label)
            else:
                labels.append(label)

        self.elapsed += max(time_spent)
        self.workers = workers
        self.labels = labels

    def advance_time_to_assign(self):
        self.advance_time(min(self.workers))

    def advance_time_to_complete(self):
        self.advance_time(max(self.workers))


def get_time_required(x):
    return ord(x) - 64


def main():
    input_text = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""

    # input_text = open("aoc07.txt").read()
    requirements = defaultdict(list)

    for line in input_text.splitlines():
        line = line.strip()
        fields = line.split()
        dependency = fields[1]
        step = fields[7]

        requirements[step].append(dependency)
        requirements[dependency]

    pprint(requirements)

    workers = Workers(5)
    while len(workers.completed) < len(requirements):
        todo = []
        for step, deps in requirements.items():
            if step in workers.completed:
                continue
            for dep in deps:
                if dep not in workers.completed:
                    break
            else:  # not terminated by break
                todo.append(step)

        print(todo)
        todo.sort()
        if len(todo) == 0:
            workers.advance_time_to_assign()

        assigned = False
        while len(todo) > 0:
            workers.advance_time_to_assign()
            label = todo.pop(0)
            if label not in workers.labels:
                workers.assign_work(get_time_required(label), label)
                assigned = True

        if not assigned:
            workers.advance_time_to_complete()

    workers.advance_time_to_complete()
    print(workers.elapsed)


if __name__ == "__main__":
    main()
