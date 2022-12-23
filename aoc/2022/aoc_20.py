from dataclasses import dataclass
from typing import Iterable, Optional, TypeVar

T = TypeVar("T")


def unwrap(v: Optional[T]) -> T:
    assert v is not None
    return v


@dataclass
class Item:
    value: int
    prev: Optional["Item"] = None
    next: Optional["Item"] = None

    def add_right(self, item: "Item"):
        old_next = self.next
        self.next = item
        item.prev = self
        item.next = old_next
        if old_next is not None:
            old_next.prev = item

    def add_left(self, item: "Item"):
        old_prev = self.prev
        self.prev = item
        item.next = self
        item.prev = old_prev
        if old_prev is not None:
            old_prev.next = item

    def iter(self) -> Iterable["Item"]:
        curr: Optional[Item] = self
        while curr is not None:
            yield curr
            curr = curr.next
            if curr is self:
                break

    def iter_prev(self) -> Iterable["Item"]:
        curr: Optional[Item] = self
        while curr is not None:
            yield curr
            curr = curr.prev
            if curr is self:
                break

    def iter_values(self) -> Iterable[int]:
        for item in self.iter():
            yield item.value

    def iter_values_prev(self) -> Iterable[int]:
        for item in self.iter_prev():
            yield item.value

    def delete(self) -> tuple[Optional["Item"], Optional["Item"]]:
        orig_next = self.next
        orig_prev = self.prev
        if self.prev is not None:
            self.prev.next = orig_next
            self.prev = None
        if self.next is not None:
            self.next.prev = orig_prev
            self.next = None

        return (orig_prev, orig_next)

    def as_list(self) -> list[int]:
        return list(self.iter_values())

    def last(self) -> "Item":
        for idx, item in enumerate(self.iter()):
            if idx > 0 and item is self:
                raise ValueError("Loop detected")

        return item

    def start(self) -> "Item":
        for idx, item in enumerate(self.iter_prev()):
            if idx > 0 and item is self:
                raise ValueError("Loop detected")

        return item

    def make_double_ended(self):
        start = self.start()
        last = self.last()

        last.next = start
        start.prev = last


def item_from_list(numbers: list[int]) -> Optional[Item]:
    retval: Optional[Item] = None
    item: Optional[Item] = None
    for number in numbers:
        if item is None:
            item = Item(number)
            retval = item
        else:
            new_item = Item(number)
            item.add_right(new_item)
            item = new_item
    return retval


def part01(numbers: list[int]):
    start_item = unwrap(item_from_list(numbers))
    print("original", start_item.as_list())
    items_list = list(start_item.iter())

    start_item.make_double_ended()

    for item in items_list:
        print("current item", item.value)
        if item.value == 0:
            continue

        old_prev, old_next = item.delete()

        print("after delete", start_item.as_list())
        if item.value > 0:
            curr = old_next
        else:
            curr = old_prev

        assert curr is not None

        for cnt in range(abs(item.value) - 1):
            if item.value > 0:
                curr = curr.next
            else:
                curr = curr.prev
            assert curr is not None

        curr.add_right(item)

        print("after move:", start_item.as_list())

    return start_item


def test_part01():
    numbers = [
        1,
        2,
        -3,
        3,
        -2,
        0,
        4,
    ]
    start_item = part01(numbers)
    print(start_item.as_list())


def test_item():
    item = item_from_list([1, 2, 3, 4])
    assert list(item.iter_values()) == [1, 2, 3, 4]


def test_item_double_ended():
    item = item_from_list([1, 2, 3, 4])
    item.make_double_ended()
    last = unwrap(item.prev)

    assert list(item.iter_values()) == [1, 2, 3, 4]
    assert list(last.iter_values_prev()) == [4, 3, 2, 1]


def test_item_delete():
    start = item_from_list([1, 2, 3, 4])
    item_list = list(start.iter())
    assert item_list[1].value == 2
    item_list[1].delete()
    assert list(start.iter_values()) == [1, 3, 4]
    item_list[-1].delete()
    assert list(start.iter_values()) == [1, 3]


def test_item_add_right():
    start = item_from_list([1, 2, 3, 4])
    item_list = list(start.iter())
    assert item_list[1].value == 2
    item_list[1].add_right(Item(9))
    assert list(start.iter_values()) == [1, 2, 9, 3, 4]
    assert list(item_list[-1].iter_values_prev()) == [4, 3, 9, 2, 1]


def test_item_add_left():
    start = item_from_list([1, 2, 3, 4])
    item_list = list(start.iter())
    assert item_list[1].value == 2
    item_list[1].add_left(Item(9))
    assert list(start.iter_values()) == [1, 9, 2, 3, 4]
    assert list(item_list[-1].iter_values_prev()) == [4, 3, 2, 9, 1]
