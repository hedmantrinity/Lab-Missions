"""

  Program: CSC215 Lab 5 - Big Oh No!
  CSC215, SDSM&T, Fall 2026
 ----------------------------
  Partner 1 Name:
  Partner 2 Name:

  NOTE: your tasks are marked with TODO: comments.

  The situation
  -------------
  At 1423 hours a pressure sensor in Habitat Ring 7 registered a 0.3% drop.
  Protocol requires immediate evacuation of all non-essential personnel.
  The system needs to produce a sorted list of Ring 7 residents by medical priority
  and find specific colonists by ID as fast as possible.

  Slow sorts and searches just won't cut it.

  What to do
  ----------
    1. Choose ONE task from Section A (A1 or A2) - searching.
    2. Choose ONE task from Section B (B1 or B2) - sorting.
    3. Replace each `NotImplementedError` with your implementation. Do NOT 
       change the function names or parameters - the tests depend on them.
    4. Run the tests until every test for your two tasks passes.
    5. Answer the REFLECTION question(s) for each task you completed.
    6. DELETE the two tasks you did not choose (code AND tests) before
       you submit, so that only your two tasks remain.

  Rules
  -----
    - Do not edit the test data or the test functions.
    - Do not call sorted() or .sort() inside your sort implementations.
      That defeats the purpose, and a test checks for it. Dave will know.

  Submissions
  -----------
    - Submit what you have done by the end of class
    - You can submit a more complete version by 10pm but MUST have a changelog
      comment in D2L explaining:
        - What was working at the end of class.
        - What (specifically) changed - function name, variable etc.
        - Why it was wrong the first time.

  Run the tests with:   pytest -v mission05.py


"""
import copy
import math
import pytest
import random
import time
import sys as _sys
import inspect as _inspect

# =============================================================================
# SECTION A -- Searching  (choose ONE of A1 / A2)
# =============================================================================

# -----------------------------------------------------------------------------
# Task A1 -- Colony Roster Binary Search
#
# The colony roster is kept sorted by colonist ID. Binary search brings
# lookup from O(n) to O(log n).
#   binary_search(roster, colonist_id) - sorted list of dicts, search by
#       "id". Return dict if found, None if not.
#   batch_lookup(roster, id_list) - binary search for each ID, return
#       {id: record_or_None}
#   count_steps(roster, colonist_id) - number of probes (midpoints checked)
# -----------------------------------------------------------------------------

# -- YOUR CODE -- fill in the functions marked with `NotImplementedError` -----
def binary_search(roster, colonist_id):
    """
    Search a SORTED roster for the colonist with the given id, using binary search 

    Parameters:
        roster (list[dict]): colonist records sorted ascending by "id".
            Each record is a dict with at least an "id" key.
        colonist_id (str): the id to search for, e.g. "K0042".

    Returns:
        dict: the matching record, if colonist_id is present in roster.
        None: if no record in roster has that id.
    """
    raise NotImplementedError("TODO: implement this function")


def batch_lookup(roster, id_list):
    """
    Look up several colonist ids at once, reusing binary_search() for each.

    Parameters:
        roster (list[dict]): sorted colonist records
        id_list (list[str]): the ids to look up, in any order. May contain
            ids that do not exist in roster.

    Returns:
        dict: maps each id in id_list to whatever binary_search() returned
            for it - the matching record if found, or None if that id
            doesn't exist in roster. Every id in id_list should appear as
            a key in the result, even the ones that map to None.

    Note:
        This should call binary_search() - don't duplicate the search logic here.
    """
    raise NotImplementedError("TODO: implement this function")


def count_steps(roster, colonist_id):
    """
    Run the same binary search as binary_search(), but return HOW MANY
    probes (midpoint checks) it took to find (or fail to find) colonist_id, 
    instead of the record itself.

    Parameters:
        roster (list[dict]): sorted colonist records.
        colonist_id (str): the id to search for. Does not need to exist in roster

    Returns:
        int: the number of probes - how many midpoints the search checked
            before returning. Count each pass through the loop once, even
            if that pass compares the ids more than once (== and <).
    """
    raise NotImplementedError("TODO: implement this function")


# -- Test data ----------------------------------------------------------------
ROSTER = []
for i in range(1, 501):
    ROSTER.append({"id": f"K{i:04d}", "name": f"Colonist {i}", "section": "Ring-7"})

class CountingRecord(dict):
    """dict that counts how many times any key is read."""
    reads = 0
    def __getitem__(self, key):
        CountingRecord.reads += 1
        return super().__getitem__(key)
    

# -- Tests -- already written for you; make them pass -------------------------
def test_a1_found():
    result = binary_search(ROSTER, "K0042")
    assert result is not None
    assert result["id"] == "K0042"

def test_a1_not_found():
    assert binary_search(ROSTER, "K9999") is None

def test_a1_first_element():
    result = binary_search(ROSTER, "K0001")
    assert result is not None
    assert result["id"] == "K0001"

def test_a1_last_element():
    result = binary_search(ROSTER, "K0500")
    assert result is not None
    assert result["id"] == "K0500"

def test_a1_empty_roster():
    assert binary_search([], "K0001") is None

def test_a1_batch_lookup():
    results = batch_lookup(ROSTER, ["K0001", "K0250", "K9999"])
    assert results["K0001"]["id"] == "K0001"
    assert results["K9999"] is None

def test_a1_steps_logarithmic():
    steps = count_steps(ROSTER, "K0042")
    assert steps <= math.ceil(math.log2(len(ROSTER))) + 1

def test_a1_steps_not_found_logarithmic():
    steps = count_steps(ROSTER, "K9999")
    assert steps <= math.ceil(math.log2(len(ROSTER))) + 1


GAPPY = [{"id": f"K{i:04d}"} for i in range(2, 101, 2)]      # even ids only

def test_a1_not_found_in_gap():
    assert binary_search(GAPPY, "K0051") is None

def test_a1_not_found_below_range():
    assert binary_search(ROSTER, "K0000") is None

def test_a1_single_element():
    one = [{"id": "K0007"}]
    assert binary_search(one, "K0007") is one[0]
    assert binary_search(one, "K0006") is None
    assert binary_search(one, "K0008") is None

def test_a1_returns_the_record_itself():
    assert binary_search(ROSTER, "K0042") is ROSTER[41]

def test_a1_finds_every_element():
    for rec in ROSTER:
        assert binary_search(ROSTER, rec["id"]) is rec

def test_a1_is_actually_logarithmic():
    roster = [CountingRecord(r) for r in ROSTER]
    CountingRecord.reads = 0
    binary_search(roster, "K0499")
    # each probe reads "id" at most twice
    assert CountingRecord.reads <= 2 * (math.floor(math.log2(len(roster))) + 1)

def test_a1_batch_lookup_complete():
    ids = ["K0001", "K0250", "K9999"]
    results = batch_lookup(ROSTER, ids)
    assert set(results) == set(ids)
    assert results["K0250"] is ROSTER[249]
    assert batch_lookup(ROSTER, []) == {}

def test_a1_steps_exact_values():
    assert count_steps(ROSTER, "K0250") == 1          # first midpoint
    assert count_steps([], "K0001") == 0
    n = len(ROSTER)
    assert count_steps(ROSTER, "K9999") >= math.floor(math.log2(n))

def test_a1_steps_never_exceeds_bound_for_any_id():
    bound = math.floor(math.log2(len(ROSTER))) + 1
    for rec in ROSTER:
        assert 1 <= count_steps(ROSTER, rec["id"]) <= bound


# -- REFLECTION -- answer in comments below before submitting -----------------
#
# 1. Binary search requires the roster to be sorted by id before it is
#    called. What happens if someone calls binary_search() on an unsorted
#    roster? Does it raise an error? What does it actually return, and why
#    is that dangerous?  
#    What would be the cost to check if the list is already sorted?  Is it 
#    worth it? When would we add this check and when should we not?
#
#    Your answer:
#
#
#


# -----------------------------------------------------------------------------
# Task A2 -- Sensor Stream Anomaly Detector
#
# The sensor network dumps raw unsorted readings continuously. Linear search
# is the correct tool.
#   first_anomaly(stream, threshold) - index of first reading exceeding
#       threshold, or -1
#   all_anomalies(stream, threshold) - list of (index, value) for exceeding
#       readings
#   scan_window(stream, start, end, threshold) - anomaly count in
#       stream[start:end]
#   emergency_scan(stream, threshold, fault_codes) - dict with
#       first_anomaly, fault_hits (indices matching fault_codes),
#       anomaly_count, max_value
# -----------------------------------------------------------------------------

# -- YOUR CODE -- fill in the functions marked with `NotImplementedError` -----
def first_anomaly(stream, threshold):
    """
    Scan an UNSORTED sensor stream from the beginning and return the index
    of the first reading that exceeds threshold.

    Parameters:
        stream (list[float]): sensor readings in the order they occurred.
        threshold (float): a reading counts as an anomaly if it is strictly
            greater than this value.

    Returns:
        int: the index of the first reading > threshold.
        -1: if no reading in stream exceeds threshold (including when
            stream is empty).
    """
    raise NotImplementedError("TODO: implement this function")


def all_anomalies(stream, threshold):
    """
    Find every reading in the stream that exceeds threshold, not just the
    first one.

    Parameters:
        stream (list[float]): sensor readings in order.
        threshold (float): a reading counts as an anomaly if it is strictly
            greater than this value.

    Returns:
        list[tuple[int, float]]: one (index, value) pair for every reading
            that exceeds threshold, in the order those readings occur in
            stream. Returns an empty list if there are no anomalies.
    """
    raise NotImplementedError("TODO: implement this function")


def scan_window(stream, start, end, threshold):
    """
    Like all_anomalies(), but only count anomalies within a slice of the
    stream - stream[start:end] - rather than the whole thing.

    Parameters:
        stream (list[float]): sensor readings in order.
        start (int): index where the window begins (inclusive).
        end (int): index where the window ends (exclusive), same convention
            as Python slicing: stream[start:end].
        threshold (float): a reading counts as an anomaly if it is strictly
            greater than this value.

    Returns:
        int: the number of readings within stream[start:end] that exceed
            threshold.
    """
    raise NotImplementedError("TODO: implement this function")


def emergency_scan(stream, threshold, fault_codes):
    """
    Produce one combined report about the stream instead of requiring four
    separate passes over it. A real sensor feed could be huge, so bundling
    everything this function reports into a single traversal matters.

    Parameters:
        stream (list[float]): sensor readings in order.
        threshold (float): a reading counts as an anomaly if it is strictly
            greater than this value.
        fault_codes (set[float]): specific reading VALUES that represent a
            known hardware fault code (e.g. a sensor reporting -1.0 to mean
            "disconnected") rather than a real measurement.

    Returns:
        dict: with these keys -
            "first_anomaly" (int): same meaning as first_anomaly()'s return
                value - index of the first reading > threshold, or -1.
            "fault_hits" (list[int]): indices of every reading whose VALUE
                appears in fault_codes (regardless of whether it also
                exceeds threshold).
            "anomaly_count" (int): total number of readings > threshold.
            "max_value" (float): the single largest reading in the stream.
                (Assume stream is non-empty when this is called.)
    """
    raise NotImplementedError("TODO: implement this function")


# -- Test data ----------------------------------------------------------------
STREAM = [72.1, 68.4, 91.3, 55.2, 88.7, 95.0, 62.1, 43.8, 97.2, 71.4]
FAULTS = {-1.0, 999.9, 0.0}

# -- Tests -- already written for you; make them pass -------------------------
def test_a2_first_anomaly_found():
    assert first_anomaly(STREAM, 90.0) == 2

def test_a2_first_anomaly_not_found():
    assert first_anomaly(STREAM, 100.0) == -1

def test_a2_first_anomaly_empty():
    assert first_anomaly([], 90.0) == -1

def test_a2_all_anomalies_values():
    results = all_anomalies(STREAM, 90.0)
    values = []     # values  = [v for _, v in results]
    for _, v in results:
        values.append(v)
    assert 91.3 in values
    assert 95.0 in values
    assert 97.2 in values
    assert len(results) == 3

def test_a2_all_anomalies_indices_correct():
    for idx, val in all_anomalies(STREAM, 90.0):
        assert STREAM[idx] == val

def test_a2_scan_window():
    assert scan_window(STREAM, 0, 4, 80.0) == 1

def test_a2_emergency_scan():
    report = emergency_scan(STREAM, 90.0, FAULTS)
    assert report["anomaly_count"]    == 3
    assert report["first_anomaly"]    == 2
    assert report["max_value"]        == pytest.approx(97.2)
    assert report["fault_hits"]       == []

def test_a2_emergency_scan_with_faults():
    stream = [72.1, 999.9, 68.4, -1.0]
    report = emergency_scan(stream, 80.0, FAULTS)
    assert 1 in report["fault_hits"]
    assert 3 in report["fault_hits"]


def test_a2_threshold_is_strict():
    assert first_anomaly([90.0, 90.1], 90.0) == 1
    assert all_anomalies([90.0], 90.0) == []
    assert scan_window([90.0, 90.0], 0, 2, 90.0) == 0
    assert emergency_scan([90.0], 90.0, set())["anomaly_count"] == 0

def test_a2_all_anomalies_exact_order():
    assert all_anomalies(STREAM, 90.0) == [(2, 91.3), (5, 95.0), (8, 97.2)]
    assert all_anomalies([], 90.0) == []

def test_a2_scan_window_boundaries():
    assert scan_window(STREAM, 2, 3, 90.0) == 1      # start inclusive
    assert scan_window(STREAM, 3, 5, 90.0) == 0      # end exclusive (5 is 95.0)
    assert scan_window(STREAM, 4, 4, 0.0) == 0       # empty window
    assert scan_window(STREAM, 0, len(STREAM), 90.0) == 3

def test_a2_emergency_max_all_negative():
    assert emergency_scan([-5.0, -3.0, -9.0], 0.0, set())["max_value"] == -3.0

def test_a2_emergency_with_faults_full_report():
    report = emergency_scan([72.1, 999.9, 68.4, -1.0], 80.0, FAULTS)
    assert report["fault_hits"] == [1, 3]
    assert report["first_anomaly"] == 1
    assert report["anomaly_count"] == 1
    assert report["max_value"] == pytest.approx(999.9)

def test_a2_emergency_single_pass():
    report = emergency_scan(iter(STREAM), 90.0, FAULTS)   # one-shot iterator
    assert report["anomaly_count"] == 3
    assert report["first_anomaly"] == 2
    assert report["max_value"] == pytest.approx(97.2)

def test_a2_emergency_agrees_with_helpers():
    rng = random.Random(1)
    for _ in range(50):
        s = [round(rng.uniform(-10, 110), 1) for _ in range(rng.randint(1, 40))]
        r = emergency_scan(s, 90.0, FAULTS)
        assert r["first_anomaly"] == first_anomaly(s, 90.0)
        assert r["anomaly_count"] == len(all_anomalies(s, 90.0))
        assert r["max_value"] == max(s)



# -- REFLECTION -- answer in comments below before submitting -----------------
#
# 1. The sensor stream is unsorted and arrives in real time. Explain in your
#    own words why binary search cannot be used here, even if the stream
#    were briefly sorted before each search.  
#    How would the time efficiency be affected if we used a binary search?
#
#    Your answer:
#
#
#
#


# =============================================================================
# SECTION B -- Sorting  (choose ONE of B1 / B2)
# =============================================================================

# -----------------------------------------------------------------------------
# Task B1 -- Evacuation Priority Sort (Bubble & Selection)
#
# Ring 7 residents must be evacuated in priority order (higher score =
# evacuate first). Implement BOTH bubble sort and selection sort and
# benchmark them.
#   bubble_sort_by_priority(colonists) - sort IN PLACE using an optimized
#       bubble sort (stop early when a pass makes no swaps), descending by
#       "priority", return list
#   selection_sort_by_priority(colonists) - sort IN PLACE using selection sort, 
#       descending by "priority", return list
#   benchmark_both(colonists) - runs both sorts and returns a dict with the
#       seconds of runtime for each - {"bubble": seconds, "selection": seconds}
#       Make sure to make a copy (shallow or deep?) of the colonists data 
#       before running the sorts 
# -----------------------------------------------------------------------------

# -- YOUR CODE -- fill in the functions marked with `NotImplementedError` -----
def bubble_sort_by_priority(colonists):
    """
    Sort colonists IN PLACE into descending order by "priority" (highest
    priority evacuates first), using an *optimized* bubble sort.

    Do not call Python's built-in sorted() or list.sort() here -
    the entire point of this task is to implement the comparison/swap logic
    yourself.

    Parameters:
        colonists (list[dict]): records with at least a "priority" key.
            This list is sorted IN PLACE - it is mutated directly rather
            than building a new list.

    Returns:
        list[dict]: the same list object that was passed in, now sorted
            descending by "priority".
    """
    raise NotImplementedError("TODO: implement this function")


def selection_sort_by_priority(colonists):
    """
    Sort colonists IN PLACE into descending order by "priority" (highest
    priority evacuates first), using selection sort.

    Do not call Python's built-in sorted() or list.sort() here -
    the entire point of this task is to implement the comparison/swap logic
    yourself.

    Parameters:
        colonists (list[dict]): records with at least a "priority" key.
            Sorted IN PLACE.

    Returns:
        list[dict]: the same list object, sorted descending by "priority".

    """
    raise NotImplementedError("TODO: implement this function")


def benchmark_both(colonists):
    """
    Time how long bubble_sort_by_priority() and selection_sort_by_priority()
    each take to sort a copy of colonists, and report both durations.

    IMPORTANT: each sort function mutates its input in place, so this must
    hand each one its OWN separate copy - if both sorts ran on the same list, 
    the second one would start from data that's already sorted by the first, 
    which would make the comparison meaningless (and probably make the second 
    sort look artificially fast).

    Parameters:
        colonists (list[dict]): the records to sort. Make copies before sorting.

    Returns:
        dict: {"bubble": <seconds>, "selection": <seconds>} 
            Use time library function (time.perf_counter()) each sort took to run.
    """
    raise NotImplementedError("TODO: implement this function")


# -- Test data ----------------------------------------------------------------

random.seed(7)

RING7 = []
for i in range(1, 51):
    RING7.append({"id": f"K{i:04d}", "name": f"Colonist {i}", "priority": random.randint(1, 100)})

class CountingRecord(dict):
    """dict that counts how many times any key is read."""
    reads = 0
    def __getitem__(self, key):
        CountingRecord.reads += 1
        return super().__getitem__(key)

# -- Tests -- already written for you; make them pass -------------------------
def test_b1_bubble_descending():
    data = copy.deepcopy(RING7)
    bubble_sort_by_priority(data)
    prios = []
    for c in data:
        prios.append(c["priority"])
    assert prios == sorted(prios, reverse=True)

def test_b1_selection_descending():
    data = copy.deepcopy(RING7)
    selection_sort_by_priority(data)
    prios = []
    for c in data:
        prios.append(c["priority"])
    assert prios == sorted(prios, reverse=True)

def test_b1_preserves_all_colonists():
    data = copy.deepcopy(RING7)
    orig = set()
    for c in data:
        orig.add(c["id"])
    bubble_sort_by_priority(data)
    after = set()
    for c in data:
        after.add(c["id"])
    assert after == orig

def test_b1_both_agree():
    d1 = copy.deepcopy(RING7)
    d2 = copy.deepcopy(RING7)
    bubble_sort_by_priority(d1)
    selection_sort_by_priority(d2)
    prios1 = []
    for c in d1:
        prios1.append(c["priority"])
    prios2 = []
    for c in d2:
        prios2.append(c["priority"])
    assert prios1 == prios2

def test_b1_sort_empty():
    assert bubble_sort_by_priority([]) == []
    assert selection_sort_by_priority([]) == []

def test_b1_benchmark_keys():
    result = benchmark_both(copy.deepcopy(RING7))
    assert "bubble"    in result
    assert "selection" in result

def by_priority(c):
    return c["priority"]

def test_b1_in_place_and_returns_same_object():
    for fn in (bubble_sort_by_priority, selection_sort_by_priority):
        data = copy.deepcopy(RING7)
        assert fn(data) is data

def test_b1_bubble_stable_matches_builtin():
    expected = [c["id"] for c in sorted(RING7, key=by_priority, reverse=True)]
    data = copy.deepcopy(RING7)
    bubble_sort_by_priority(data)
    assert [c["id"] for c in data] == expected

def test_b1_selection_preserves_all():
    data = copy.deepcopy(RING7)
    selection_sort_by_priority(data)
    assert sorted(c["id"] for c in data) == sorted(c["id"] for c in RING7)

def test_b1_edge_shapes():
    for fn in (bubble_sort_by_priority, selection_sort_by_priority):
        assert fn([{"id": "a", "priority": 5}]) == [{"id": "a", "priority": 5}]
        asc = [{"id": str(i), "priority": i} for i in range(10)]
        assert [c["priority"] for c in fn(asc)] == list(range(9, -1, -1))
        same = [{"id": str(i), "priority": 3} for i in range(5)]
        assert [c["id"] for c in fn(same)] == ["0", "1", "2", "3", "4"]

def test_b1_bubble_early_exit():
    data = [CountingRecord(id=str(i), priority=100 - i) for i in range(50)]  # already sorted
    CountingRecord.reads = 0
    bubble_sort_by_priority(data)
    assert CountingRecord.reads <= 2 * (len(data) - 1)     # one pass only

def test_b1_no_builtin_sort():
    import ast, textwrap
    for fn in (bubble_sort_by_priority, selection_sort_by_priority):
        data = copy.deepcopy(RING7)
        assert fn(data) is data            # must actually run and sort
        tree = ast.parse(textwrap.dedent(_inspect.getsource(fn)))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                f = node.func
                assert not (isinstance(f, ast.Name) and f.id == "sorted")
                assert not (isinstance(f, ast.Attribute) and f.attr == "sort")

def test_b1_benchmark_does_not_mutate_input():
    data = copy.deepcopy(RING7)
    before = [c["id"] for c in data]
    result = benchmark_both(data)
    assert [c["id"] for c in data] == before
    assert all(isinstance(v, float) and v >= 0 for v in result.values())



# -- REFLECTION -- answer in comments below before submitting -----------------
#
# 1. Both sorts put the colonists in correct priority order, but they list 
#    some colonists in a different order. Find an example. Why does selection 
#    sort move a colonist “past” another one with the same priority, and 
#    why doesn’t bubble sort? Does it matter for an evacuation list?
#
#    Your answer:
#
#
# 
# 


# -----------------------------------------------------------------------------
# Task B2 -- Inventory Merge Sort
#
# Supply inventory sorted by quantity ascending. The real list is 2,000
# items (tests use 100) - O(n^2) will be noticeable. Use merge sort.
#   merge(left, right) - merge two sorted lists of dicts by "quantity" ascending
#   merge_sort(inventory) - sort by "quantity" ascending using an iterative 
#       solution. return new list
#   top_n_scarce(inventory, n) - n items with lowest quantity
# -----------------------------------------------------------------------------

# -- YOUR CODE -- fill in the functions marked with `NotImplementedError` -----
def merge(left, right):
    """
    Merge two lists that are ALREADY sorted ascending by "quantity" into one
    combined list that is also sorted ascending by "quantity".

    Parameters:
        left (list[dict]): sorted ascending by "quantity".
        right (list[dict]): sorted ascending by "quantity".

    Returns:
        list[dict]: a NEW list (don't mutate left or right) containing every
            element from both inputs, sorted ascending by "quantity". Ties
            should keep left's element first 
    """
    raise NotImplementedError("TODO: implement this function")


def merge_sort(inventory):
    """
    Sort inventory ascending by "quantity" and return a NEW sorted list,
    leaving the original inventory list unmodified.

    This must be ITERATIVE - do not have merge_sort() call itself.
        1. Treat every single item as its own sorted "run" of length 1
           (a list of one element is trivially already sorted).
        2. Repeatedly call merge() on pairs of neighboring runs to combine
           them into runs twice as long (length 1 -> 2 -> 4 -> 8 -> ...).
        3. Stop once there's only one run left -- that run is the fully
           sorted result.
    If there's an odd run left over with no partner in a given pass, it
    just carries forward unmerged into the next pass.

    Parameters:
        inventory (list[dict]): records with at least a "quantity" key.
            NOT mutated - merge_sort returns a new list.

    Returns:
        list[dict]: a new list containing every record from inventory,
            sorted ascending by "quantity".
    """
    raise NotImplementedError("TODO: implement this function")


def top_n_scarce(inventory, n):
    """
    Return the n items with the LOWEST "quantity" - i.e. the scarcest
    supplies.  Use merge_sort() rather than re-implementing sorting here.

    Parameters:
        inventory (list[dict]): records with at least a "quantity" key.
        n (int): how many of the scarcest items to return.

    Returns:
        list[dict]: the n items from inventory with the smallest
            "quantity" values, in ascending order by "quantity". If
            n > len(inventory), returns all of inventory sorted.
    """
    raise NotImplementedError("TODO: implement this function")


# -- Test data ----------------------------------------------------------------
random.seed(42)

INVENTORY = []
for i in range(100):
    INVENTORY.append({"item": f"item_{i:03d}", "quantity": random.randint(0, 1000)})

# -- Tests -- already written for you; make them pass -------------------------
def test_b2_merge_basic():
    left  = [{"quantity":1},{"quantity":3},{"quantity":5}]
    right = [{"quantity":2},{"quantity":4},{"quantity":6}]
    result = merge(left, right)
    quantities = []
    for r in result:
        quantities.append(r["quantity"])
    assert quantities == [1, 2, 3, 4, 5, 6]

def test_b2_merge_empty():
    assert merge([], [{"quantity":1}]) == [{"quantity":1}]

def test_b2_merge_sort_ascending():
    data = copy.deepcopy(INVENTORY)
    result = merge_sort(data)
    q = []
    for r in result:
        q.append(r["quantity"])
    assert q == sorted(q)

def test_b2_merge_sort_preserves_all():
    data = copy.deepcopy(INVENTORY)
    result = merge_sort(data)
    assert len(result) == len(INVENTORY)

    result_items = set()
    for r in result:
        result_items.add(r["item"])
    inventory_items = set()
    for r in INVENTORY:
        inventory_items.add(r["item"])
    assert result_items == inventory_items

def test_b2_merge_sort_no_modify_original():
    data = copy.deepcopy(INVENTORY)
    orig = []
    for r in data:
        orig.append(r["item"])
    merge_sort(data)
    after = []
    for r in data:
        after.append(r["item"])
    assert after == orig

def get_quantity(item):
    return item["quantity"]

def test_b2_merge_sort_matches_builtin():
    data = copy.deepcopy(INVENTORY)
    result = merge_sort(data)
    expected = sorted(INVENTORY, key=get_quantity)
    result_q = []
    for r in result:
        result_q.append(r["quantity"])
    expected_q = []
    for r in expected:
        expected_q.append(r["quantity"])
    assert result_q == expected_q

def test_b2_top_n_scarce():
    scarce = top_n_scarce(copy.deepcopy(INVENTORY), 5)
    assert len(scarce) == 5

    all_q = []
    for r in INVENTORY:
        all_q.append(r["quantity"])
    all_q = sorted(all_q)

    scarce_q = []
    for r in scarce:
        scarce_q.append(r["quantity"])
    assert max(scarce_q) <= all_q[4]


def test_b2_merge_stable_left_first():
    left, right = [{"quantity": 1, "src": "L"}], [{"quantity": 1, "src": "R"}]
    assert [r["src"] for r in merge(left, right)] == ["L", "R"]

def test_b2_merge_left_leftovers_and_both_empty():
    assert [r["quantity"] for r in merge([{"quantity": 5}, {"quantity": 6}], 
                                         [{"quantity": 1}])] == [1, 5, 6]
    assert merge([{"quantity": 1}], []) == [{"quantity": 1}]
    assert merge([], []) == []

def test_b2_merge_does_not_mutate_inputs():
    left  = [{"quantity": 1}, {"quantity": 3}]
    right = [{"quantity": 2}]
    l0, r0 = list(left), list(right)
    merge(left, right)
    assert left == l0 and right == r0

def test_b2_merge_sort_stable_matches_builtin_by_item():
    result = merge_sort(copy.deepcopy(INVENTORY))
    expected = sorted(INVENTORY, key=get_quantity)
    assert [r["item"] for r in result] == [r["item"] for r in expected]

def test_b2_merge_sort_small_and_odd_sizes():
    assert merge_sort([]) == []
    for n in (1, 2, 3, 5, 7, 8, 9, 17):
        data = [{"item": str(i), "quantity": (i * 37) % 11} for i in range(n)]
        result = merge_sort(data)
        assert result is not data
        assert [r["item"] for r in result] == [r["item"] for r in sorted(data, key=get_quantity)]

def test_b2_merge_sort_is_iterative(monkeypatch):
    me = _sys.modules[__name__]
    original = me.merge_sort
    calls = {"n": 0}
    def spy(inv):
        calls["n"] += 1
        return original(inv)
    monkeypatch.setattr(me, "merge_sort", spy)
    me.merge_sort(copy.deepcopy(INVENTORY))
    assert calls["n"] == 1

def test_b2_top_n_scarce_exact():
    scarce = top_n_scarce(copy.deepcopy(INVENTORY), 5)
    expected = sorted(INVENTORY, key=get_quantity)[:5]
    assert [r["item"] for r in scarce] == [r["item"] for r in expected]

def test_b2_top_n_scarce_edges():
    assert top_n_scarce(INVENTORY, 0) == []
    small = copy.deepcopy(INVENTORY[:3])
    assert len(top_n_scarce(small, 10)) == 3

def test_b2_top_n_scarce_uses_merge_sort(monkeypatch):
    me = _sys.modules[__name__]
    calls = {"n": 0}
    original = me.merge_sort
    def spy(inv):
        calls["n"] += 1
        return original(inv)
    monkeypatch.setattr(me, "merge_sort", spy)
    top_n_scarce(copy.deepcopy(INVENTORY), 5)
    assert calls["n"] == 1


# -- REFLECTION -- answer in comments below before submitting -----------------
#
# 1. merge_sort() returns a new sorted list rather than sorting in place.
#    What are the trade-offs of this design? When is returning a new list
#    better than modifying the original, and when is it worse?
#
#    Your answer:
#
#


# to run this file with pytest, open a command prompt in the folder
# where the python .py file is located and type: pytest -v mission05.py
