import sys

from fault_injection import apply_scenario, restore_network


def main():
    if len(sys.argv) != 2:
        print(
            "Usage: python fault_runner.py "
            "[latency|packet-loss|bandwidth|restore]"
        )
        return 2

    scenario = sys.argv[1]

    try:
        if scenario == "restore":
            result = restore_network()
            print("Network restored to fq_codel")
        else:
            result = apply_scenario(scenario)
            print(f"Applied fault scenario: {scenario}")

    except ValueError as error:
        print(error)
        return 2

    if result.returncode != 0:
        print("tc command failed:")
        print(result.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
