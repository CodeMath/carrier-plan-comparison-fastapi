from ..fake_db.fake_db import fake_sum_combination


def pay_range_combination(sum_pay: int) -> dict:
    taget_ranges = 0
    for i in fake_sum_combination.keys():
        if int(i) >= sum_pay:
            taget_ranges = int(i)

    get_sum_combination_target = fake_sum_combination[str(taget_ranges)]

    return get_sum_combination_target


def in_range(n, start, end=0):
    return start <= n <= end if end >= start else end <= n <= start
