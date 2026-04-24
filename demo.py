import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from chronos import T


print("=" * 55)
print("  CHRONOS — variables that remember everything")
print("=" * 55)


# ── 1. basic usage ──────────────────────────────────────────
print("\n[ 1 ] basic usage\n")

score = T(0)
score.set(10)
score.set(25)
score.set(100)

print("current :", score)           # 100  — prints like a normal variable
print("first   :", score.first)    # 0
print("previous:", score.prev)     # 25
print("states  :", score.states()) # 4


# ── 2. full history ─────────────────────────────────────────
score.log()


# ── 3. why ──────────────────────────────────────────────────
score.why()


# ── 4. diffs ────────────────────────────────────────────────
score.diff()


# ── 5. works with strings too ───────────────────────────────
print("[ 5 ] strings\n")

status = T("idle")
status.set("loading")
status.set("done")

status.log()


# ── 6. math still works normally ────────────────────────────
print("[ 6 ] math works normally\n")

health = T(100)
health.set(80)
health.set(55)

print("health       :", health)
print("health - 10  :", health - 10)   # 45  — math just works
print("health > 50  :", health > 50)   # True
print("health == 55 :", health == 55)  # True


# ── 7. time travel ──────────────────────────────────────────
print("\n[ 7 ] time travel — .ago(seconds)\n")

budget = T(1000)
time.sleep(0.5)
budget.set(800)
time.sleep(0.5)
budget.set(600)

print("now       :", budget)
print("0.6s ago  :", budget.ago(0.6))   # 800
print("1.5s ago  :", budget.ago(1.5))   # 1000


print("\n" + "=" * 55)
print("  done. that's chronos.")
print("=" * 55 + "\n")
