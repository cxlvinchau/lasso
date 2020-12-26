from lasso.dtmc import DTMC


def main():
    dtmc = DTMC()
    s1 = dtmc.add_state("s1")
    s2 = dtmc.add_state("s2")
    s3 = dtmc.add_state("s3")
    dtmc.add_transition(s1,1,s2)
    dtmc.add_transition(s2,0.5,s1)
    dtmc.add_transition(s2,0.5,s3)
    dtmc.add_transition(s3,1,s1)
    dtmc.steady_state()
    dtmc.visualize()


if __name__ == "__main__":
    main()
