import time
import traceback
from datetime import datetime
from typing import Any


class T:
    """
    A variable that remembers its entire life.

    Usage:
        x = T(10)       # create
        x.set(42)       # update
        print(x)        # 42  (works like a normal variable)
        x[-1]           # previous value
        x[0]            # very first value
        x.why()         # explains the last change
        x.log()         # full history timeline
        x.diff()        # shows every change + delta
    """

    __slots__ = ("_history",)

    def __init__(self, value: Any):
        self._history: list[dict] = []
        self._snapshot(value)

    # ─── private ────────────────────────────────────────────────────────────

    def _snapshot(self, value: Any) -> None:
        frame = traceback.extract_stack()[-3]
        self._history.append({
            "v": value,
            "t": time.time(),
            "at": datetime.now().strftime("%H:%M:%S.%f")[:-3],  # trim to ms
            "file": frame.filename.split("/")[-1],              # just filename
            "line": frame.lineno,
            "code": (frame.line or "").strip(),
        })

    # ─── core api ───────────────────────────────────────────────────────────

    def set(self, value: Any) -> "T":
        """Update the value. Returns self so you can chain."""
        self._snapshot(value)
        return self

    @property
    def value(self) -> Any:
        """The current value."""
        return self._history[-1]["v"]

    # ─── time travel ────────────────────────────────────────────────────────

    def __getitem__(self, index: int) -> Any:
        """
        Standard list indexing over the history.
        x[0]   → first ever value
        x[-1]  → current value  (last item)
        x[-2]  → previous value (one before current)
        """
        return self._history[index]["v"]

    @property
    def prev(self) -> Any:
        """Shortcut: the value just before the current one."""
        if len(self._history) < 2:
            raise IndexError("no previous value yet")
        return self._history[-2]["v"]

    @property
    def first(self) -> Any:
        """Shortcut: the very first value this variable ever had."""
        return self._history[0]["v"]

    def ago(self, seconds: float) -> Any:
        """x.ago(3) → what x was 3 seconds ago"""
        target = time.time() - seconds
        closest = min(self._history, key=lambda e: abs(e["t"] - target))
        return closest["v"]

    # ─── inspection ─────────────────────────────────────────────────────────

    def why(self) -> None:
        """Explains why the current value is what it is."""
        last = self._history[-1]
        prev = self._history[-2] if len(self._history) > 1 else None

        print(f"\n🔍 why is it {last['v']!r}?")
        print(f"   set at  → {last['at']}")
        print(f"   source  → {last['file']}, line {last['line']}")
        print(f"   code    → {last['code']}")
        if prev:
            print(f"   was     → {prev['v']!r}")
        print()

    def log(self) -> None:
        """Prints the full life of this variable."""
        print(f"\n📼 history — {len(self._history)} state(s)")
        print("  " + "─" * 52)
        for i, e in enumerate(self._history):
            marker = "→" if i == len(self._history) - 1 else " "
            print(f"  {marker} [{i:>2}]  {str(e['v']):<14}  {e['at']}  line {e['line']}")
        print("  " + "─" * 52 + "\n")

    def diff(self) -> None:
        """Shows every change. If numeric, shows the delta too."""
        print(f"\n📊 diffs")
        if len(self._history) < 2:
            print("  only one state so far.\n")
            return
        for i in range(1, len(self._history)):
            old = self._history[i - 1]["v"]
            new = self._history[i]["v"]
            try:
                delta = new - old
                sign = "+" if delta >= 0 else ""
                print(f"  {old!r:>10}  →  {new!r:<10}  (Δ {sign}{delta})")
            except TypeError:
                print(f"  {old!r:>10}  →  {new!r}")
        print()

    def states(self) -> int:
        """How many times this variable has changed."""
        return len(self._history)

    # ─── python builtins ────────────────────────────────────────────────────

    def __repr__(self) -> str:
        return repr(self.value)

    def __str__(self) -> str:
        return str(self.value)

    def __int__(self):     return int(self.value)
    def __float__(self):   return float(self.value)
    def __bool__(self):    return bool(self.value)
    def __len__(self):     return len(self.value)
    def __iter__(self):    return iter(self.value)

    # math operators — so x + 5 just works
    def __add__(self, o):  return self.value + o
    def __sub__(self, o):  return self.value - o
    def __mul__(self, o):  return self.value * o
    def __truediv__(self, o): return self.value / o
    def __lt__(self, o):   return self.value < o
    def __le__(self, o):   return self.value <= o
    def __gt__(self, o):   return self.value > o
    def __ge__(self, o):   return self.value >= o
    def __eq__(self, o):   return self.value == o
    def __ne__(self, o):   return self.value != o
