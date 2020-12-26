from lasso.dtmc import DTMC
from lasso.pctl.formulae import Atomic


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
    a1,a2 = Atomic("a1",dtmc),Atomic("a2",dtmc)
    a1.add_states(s1,s2)
    a2.add_states(s3)
    f = (-(a1))
    f.eval()
    print(f.states)



if __name__ == "__main__":
    main()
