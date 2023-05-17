import heapq
from heapq import nsmallest


class Bank:
    def __init__(self):
        self.txns = {}
        self.spending = {}
        self.nxt_pid = 1
        self.scheduled = {}
        self.schedule_heap = []

    def create_acct(self, acct_id, ts):
        if self.acct_exists(acct_id):
            return False
        self.txns[acct_id] = [(ts, 0)]
        self.spending[acct_id] = 0
        return True

    def acct_exists(self, acct_id):
        return acct_id in self.txns

    def transfer(self, acc1, acc2, amt, ts):
        if not self.acct_exists(acc1) or not self.acct_exists(acc2):
            return None
        if acc1 == acc2:
            return None
        bal = self.sub(acc1, amt, ts)
        if bal is None:
            return None
        self.add(acc2, amt, ts)
        return bal

    def curr_bal(self, acct_id):
        return sum(amt for _, amt in self.txns[acct_id])

    def add(self, acct_id, amt, ts):
        if self.acct_exists(acct_id):
            return None
        self.txns[acct_id].append(ts, amt)
        return self.curr_bal(acct_id)

    def sub(self, acct_id, amt, ts):
        if self.acct_exists(acct_id) or amt > self.curr_bal(acct_id):
            return None
        self.txns[acct_id].append(ts, -amt)
        self.spending[acct_id] -= amt
        return self.curr_bal(acct_id)

    def merge_accounts(self, acct1, acct2):
        if not self.acct_exists(acct1) or not self.acct_exists(acct2):
            return None
        txns = sorted(self.txns[acct1] + self.txns[acct2])
        self.txns[acct1] = txns
        self.txns.pop(acct2)
        for pid, acc in self.scheduled:
            if acc == acct2:
                self.scheduled[pid] = acct1

    def get_balance(self, current_ts, acct_id):
        if not self.acct_exists(acct_id) or self.txns[acct_id][0][0] > current_ts:
            return None
        return sum(amt for ts, amt in self.txns[acct_id] if ts <= current_ts)

    def top_spenders(self, n):
        spending_list = [(amt, acct) for acct, amt in self.spending.items()]
        topk = nsmallest(min(n, len(spending_list)), spending_list)
        return ', '.join([f"{acct}({-1 * amt})" for amt, acct in topk])

    def schedule_payment(self, ts, delay, acct_id, amt):
        if not self.acct_exists(acct_id):
            return None
        new_ts = ts + delay
        pid = f"payment{self.nxt_pid}"
        self.nxt_pid += 1
        self.scheduled[pid] = acct_id
        heapq.heappush(self.schedule_heap, (new_ts, pid, amt))
        return pid

    def execute_scheduled(self, current_ts):
        while self.schedule_heap and current_ts >= self.schedule_heap[0][0]:
            _, pid, amt = heapq.heappop(self.schedule_heap)
            if pid not in self.scheduled:
                continue
            acct = self.scheduled[pid]
            self.sub(acct, amt)
            self.scheduled.pop(pid)

    def cancel_payment(self, acct_id, pid):
        if pid not in self.scheduled or self.scheduled[pid] != acct_id:
            return False
        self.scheduled.pop(pid)
        return True


def bool_to_str(b):
    return "true" if b else "false"


def solution(queries):
    """
    Edge cases:
    - Account already exists (creation)
    - Account does not exist (deposit)
    """
    bank = Bank()
    res = []
    for query in queries:
        typ = query[0]
        ts = int(query[1])
        bank.execute_scheduled(ts)
        if typ == "CREATE_ACCOUNT":
            _, ts, acct_id = query
            created = bank.create_acct(acct_id, ts)
            res.append(bool_to_str(created))
        elif typ == "DEPOSIT":
            _, ts, acct_id, amt = query
            amt_int = int(amt)
            bal = bank.add(acct_id, amt_int)
            res.append(str(bal))
        elif typ == "TRANSFER":
            _, ts, src, target, amt = query
            amt_int = int(amt)
            bal = bank.transfer(src, target, amt_int, int(ts))
            if bal is None:
                res.append("")
            else:
                res.append(str(bal))
        elif typ == "TOP_SPENDERS":
            _, ts, n = query
            n = int(n)
            res.append(bank.top_spenders(n))
        elif typ == "SCHEDULE_PAYMENT":
            _, ts, acct_id, amt, delay = query
            pid = bank.schedule_payment(int(ts), int(delay), acct_id, int(amt))
            if pid is None:
                res.append("")
            else:
                res.append(pid)
        elif typ == "CANCEL_PAYMENT":
            _, ts, pid, acct_id = query
            canceled = bank.cancel_payment(acct_id, pid)
            res.append(bool_to_str(canceled))


if __name__ == '__main__':
    qs = [""]
    print(solution(qs))
