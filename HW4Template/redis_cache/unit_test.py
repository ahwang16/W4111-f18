import data_cache
import sys
sys.path.append("..")
import utils.utils as ut

ut.set_debug_mode(True)

t = {"playerID": "willite01", "nameLast": "Williams", "bats": "R"}
r = data_cache.compute_key("people", {"playerID": "willite01", "nameLast": "Williams", "bats": "R"}, \
                           ['nameLast', "birthCity"])


def test1():
    data_cache.add_to_cache(r, t)


def test2():
    result = data_cache.get_from_cache(r)
    print("Result = ", result)


if __name__ == "__main__":
	test1()
	test2()

