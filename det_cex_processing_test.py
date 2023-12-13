from aalpy.utils import generate_random_deterministic_automata, bisimilar, get_Angluin_dfa, visualize_automaton
from aalpy.SULs import MealySUL
from aalpy.oracles import RandomWMethodEqOracle
from aalpy.learning_algs import run_KV, run_Lstar

# fails for exponential_bwd moore & dfa
# fails for

# rs:
# moore: warning (/Users/moritz/Documents/Thesis/AALpy_fork/AALpy/aalpy/base/Automaton.py:367: UserWarning: Automaton is non-canonical: could not compute characterization set.Returning None.
#   warnings.warn("Automaton is non-canonical: could not compute characterization set.")
# error bisimilar

for x in ['rs']:
    print(x)
    for model_type in ['moore', 'dfa']:
        print(model_type)
        for i in range(200):
            print(i)

            # for random dfa's you can also define num_accepting_states
            random_model = generate_random_deterministic_automata(automaton_type=model_type, num_states=100,
                                                                  input_alphabet_size=3, output_alphabet_size=4)

            # random_model = get_Angluin_dfa()
            # model_type = 'dfa'
            # visualize_automaton(random_model, 'LearnedModel')

            input_alphabet = random_model.get_input_alphabet()

            sul = MealySUL(random_model)

            # select any of the oracles
            eq_oracle = RandomWMethodEqOracle(input_alphabet, sul, walks_per_state=10, walk_len=20)
            #
            learned_model_KV = run_KV(input_alphabet, sul, eq_oracle, model_type, cex_processing=x, print_level=0)
            # visualize_automaton(learned_model_KV, 'LearnedModel_KV')
            assert bisimilar(random_model, learned_model_KV)

            learned_model_Lstar = run_Lstar(input_alphabet, sul, eq_oracle, model_type, cex_processing=x, print_level=0)
            # visualize_automaton(learned_model_Lstar, 'LearnedModel_Lstar')
            assert bisimilar(random_model, learned_model_Lstar)
            assert bisimilar(learned_model_KV, learned_model_Lstar)
