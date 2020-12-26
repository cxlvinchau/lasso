from lasso.dtmc import DTMC


def main():
    dtmc = DTMC()
    s1 = dtmc.add_state("s1")
    s2 = dtmc.add_state("s2")
    dtmc.add_transition(s1,1,s2)
    dtmc.add_transition(s2,1,s1)
    dtmc.visualize()
    print(dtmc.is_aperiodic())


if __name__ == "__main__":
    main()
