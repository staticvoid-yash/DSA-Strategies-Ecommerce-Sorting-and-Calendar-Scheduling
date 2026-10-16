"""
============================================================
 Case Study: 
 1. E-commerce Product Sorting  -> Divide and Conquer
 2. Google Calendar Scheduling  -> Greedy Strategy
============================================================
"""

import random
import time
from datetime import datetime, timedelta

# ============================================================
# PART 1: E-COMMERCE PRODUCT SORTING (DIVIDE AND CONQUER)
# ============================================================

class Product:
    def __init__(self, pid, name, price, rating):
        self.pid = pid
        self.name = name
        self.price = price
        self.rating = rating

    def __repr__(self):
        return f"[{self.pid}] {self.name:<12} ₹{self.price:<7} ★{self.rating}"


# ---------- MERGE SORT (Divide and Conquer) ----------
def merge_sort(products, key):
    if len(products) <= 1:
        return products

    mid = len(products) // 2
    left = merge_sort(products[:mid], key)     # Divide
    right = merge_sort(products[mid:], key)    # Divide

    return merge(left, right, key)             # Conquer


def merge(left, right, key):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ---------- QUICK SORT (Divide and Conquer) ----------
def quick_sort(products, key):
    if len(products) <= 1:
        return products

    pivot = products[len(products) // 2]
    left  = [p for p in products if key(p) <  key(pivot)]
    mid   = [p for p in products if key(p) == key(pivot)]
    right = [p for p in products if key(p) >  key(pivot)]

    return quick_sort(left, key) + mid + quick_sort(right, key)


# ============================================================
# PART 2: GOOGLE CALENDAR SCHEDULING (GREEDY STRATEGY)
# ============================================================

class Event:
    def __init__(self, title, start, end):
        self.title = title
        self.start = start
        self.end = end

    def __repr__(self):
        return f"{self.title:<15} ({self.start.strftime('%H:%M')} - {self.end.strftime('%H:%M')})"


def activity_selection_greedy(events):
    """
    Greedy approach:
    1. Sort events by END time (earliest finishing first)
    2. Pick the first event
    3. For each next event, pick if start >= last_end
    """
    if not events:
        return []

    # Step 1: Sort by end time - the greedy choice
    events_sorted = sorted(events, key=lambda e: e.end)

    selected = [events_sorted[0]]
    last_end = events_sorted[0].end

    for event in events_sorted[1:]:
        if event.start >= last_end:          # Greedy: non-overlapping
            selected.append(event)
            last_end = event.end

    return selected


# ============================================================
# PART 3: DEMO / DRIVER CODE
# ============================================================

def demo_ecommerce():
    print("=" * 65)
    print("  CASE STUDY 1: E-COMMERCE PRODUCT SORTING (Divide & Conquer)")
    print("=" * 65)

    products = [
        Product(1, "Laptop",    65000, 4.5),
        Product(2, "Phone",     30000, 4.7),
        Product(3, "Headphones", 2500, 4.2),
        Product(4, "Tablet",    20000, 4.0),
        Product(5, "Smartwatch", 8000, 3.9),
        Product(6, "Camera",    45000, 4.8),
        Product(7, "Keyboard",   1500, 4.1),
        Product(8, "Monitor",   12000, 4.4),
    ]

    print("\nOriginal List:")
    for p in products:
        print(" ", p)

    # Sort by PRICE using Merge Sort
    print("\nSorted by PRICE (Merge Sort - D&C):")
    by_price = merge_sort(products.copy(), key=lambda p: p.price)
    for p in by_price:
        print(" ", p)

    # Sort by RATING using Quick Sort
    print("\nSorted by RATING (Quick Sort - D&C):")
    by_rating = quick_sort(products.copy(), key=lambda p: p.rating)
    for p in by_rating:
        print(" ", p)

    # Performance comparison
    print("\nPerformance Analysis (10,000 products):")
    big = [Product(i, f"P{i}", random.randint(100, 100000), round(random.uniform(1, 5), 1))
           for i in range(10000)]

    t1 = time.time()
    merge_sort(big.copy(), key=lambda p: p.price)
    t2 = time.time()
    print(f"  Merge Sort Time: {t2 - t1:.4f} sec")

    t1 = time.time()
    quick_sort(big.copy(), key=lambda p: p.price)
    t2 = time.time()
    print(f"  Quick Sort Time: {t2 - t1:.4f} sec")


def demo_calendar():
    print("\n" + "=" * 65)
    print("  CASE STUDY 2: GOOGLE CALENDAR SCHEDULING (Greedy Strategy)")
    print("=" * 65)

    base = datetime(2025, 1, 1, 9, 0)

    events = [
        Event("Team Standup",  base.replace(hour=9),  base.replace(hour=10)),
        Event("Code Review",   base.replace(hour=10), base.replace(hour=11)),
        Event("Client Call",   base.replace(hour=9, minute=30), base.replace(hour=10, minute=30)),
        Event("Lunch Break",   base.replace(hour=12), base.replace(hour=13)),
        Event("Sprint Planning", base.replace(hour=13), base.replace(hour=15)),
        Event("1-on-1 Meeting", base.replace(hour=11), base.replace(hour=12)),
        Event("Training",      base.replace(hour=10, minute=30), base.replace(hour=12, minute=30)),
        Event("Daily Report",  base.replace(hour=15), base.replace(hour=16)),
    ]

    print("\nAll Requested Events:")
    for e in events:
        print(" ", e)

    selected = activity_selection_greedy(events)

    print(f"\nMaximum Non-Overlapping Events (Greedy): {len(selected)}")
    for e in selected:
        print("  ✔", e)

    print(f"\nRejected Events: {len(events) - len(selected)}")
    for e in events:
        if e not in selected:
            print("  ✘", e)


if __name__ == "__main__":
    demo_ecommerce()
    demo_calendar()