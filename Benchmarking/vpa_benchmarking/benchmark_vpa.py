from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np
import pickle
import os

from aalpy import WMethodEqOracle
from aalpy.SULs.AutomataSUL import SevpaSUL, DfaSUL, VpaSUL
from aalpy.automata import SevpaAlphabet
from aalpy.learning_algs import run_KV
from aalpy.oracles import RandomWordEqOracle
from aalpy.utils import generate_random_sevpa, visualize_automaton
from aalpy.utils.BenchmarkVpaModels import *


def state_increasing():
    print("Benchmarking for increasing state size")
    max_number_states = 50
    step_size = 10
    repeats = 10

    cex_processing = ['rs', 'linear_fwd', 'linear_bwd', 'exponential_fwd', 'exponential_bwd']
    # cex_processing = ['rs']
    data_dict = defaultdict(tuple)
    data_dict_pickle = defaultdict(list)

    for cex in cex_processing:
        states_data_median = []
        query_data_median = []
        for number_states in range(10, max_number_states + 1, step_size):
            print(number_states)
            states_data = []
            query_data = []
            for x in range(repeats):
                random_svepa = generate_random_sevpa(num_states=number_states, internal_alphabet_size=3,
                                                     call_alphabet_size=3,
                                                     return_alphabet_size=3,
                                                     acceptance_prob=0.4,
                                                     return_transition_prob=0.5)

                alphabet = random_svepa.input_alphabet

                sul = SevpaSUL(random_svepa)

                eq_oracle = RandomWordEqOracle(alphabet=alphabet.get_merged_alphabet(), sul=sul, num_walks=10000,
                                               min_walk_len=10, max_walk_len=30)

                model, data = run_KV(alphabet=alphabet, sul=sul, eq_oracle=eq_oracle, automaton_type='vpa',
                                     print_level=0, cex_processing=cex, return_data=True)

                states_data.append(number_states)
                query_data.append(data['queries_learning'])
                data_dict_pickle[cex].append((number_states, x, data['learning_rounds']))
                data_dict_pickle[cex].append((number_states, x, data['automaton_size']))
                data_dict_pickle[cex].append((number_states, x, data['queries_learning']))
                data_dict_pickle[cex].append((number_states, x, data['steps_learning']))
                data_dict_pickle[cex].append((number_states, x, data['queries_eq_oracle']))
                data_dict_pickle[cex].append((number_states, x, data['steps_eq_oracle']))
                data_dict_pickle[cex].append((number_states, x, data['learning_time']))
                data_dict_pickle[cex].append((number_states, x, data['eq_oracle_time']))
                data_dict_pickle[cex].append((number_states, x, data['total_time']))
                data_dict_pickle[cex].append((number_states, x, data['cache_saved']))

            states_data_median.append(np.median(states_data))
            query_data_median.append(np.median(query_data))

        data_dict[cex] = (states_data_median, query_data_median)

    # Save data_dict to a pickle file
    with open('state_increasing.pickle', 'wb') as file:
        pickle.dump(data_dict_pickle, file)

    # plot
    plt.figure()
    plt.xlabel('Number of states')
    plt.ylabel('Number of membership queries')
    plt.title('Query growth of a random SEVPA with increasing state size')
    for key in data_dict:
        plt.plot(data_dict[key][0], data_dict[key][1], label=key)
    plt.legend()
    plt.savefig('state_increasing.png')


def alphabet_increasing():
    print("Benchmarking for increasing alphabet size")
    repeats = 10
    max_alphabet_size = 5

    # cex_processing = ['rs', 'linear_fwd', 'linear_bwd', 'exponential_fwd', 'exponential_bwd']
    cex_processing = ['exponential_bwd']

    # uncomment to restart clear the file
    # with open('alphabet_increasing.pickle', 'wb') as file:
    #     pass

    new_data_dict_pickle = defaultdict(list)
    data_dict = defaultdict(tuple)

    filename = 'alphabet_increasing.pickle'
    if os.path.exists(filename):
        try:
            with open(filename, 'rb') as file:
                existing_data = pickle.load(file)
        except (EOFError, pickle.UnpicklingError):
            existing_data = defaultdict(list)
    else:
        existing_data = defaultdict(list)

    for cex in cex_processing:
        print(cex)
        states_data_median = []
        query_data_median = []
        for alphabet_size in range(1, max_alphabet_size + 1):
            print(f"Alphabet size: {alphabet_size}")
            for x in range(repeats):
                print(f'Rep: {x}')
                random_svepa = generate_random_sevpa(
                    num_states=50,
                    internal_alphabet_size=alphabet_size,
                    call_alphabet_size=alphabet_size,
                    return_alphabet_size=alphabet_size,
                    acceptance_prob=0.4,
                    return_transition_prob=0.5
                )

                alphabet = random_svepa.input_alphabet
                sul = SevpaSUL(random_svepa)
                eq_oracle = RandomWordEqOracle(
                    alphabet=alphabet.get_merged_alphabet(),
                    sul=sul,
                    num_walks=10000,
                    min_walk_len=10,
                    max_walk_len=30
                )

                states_data = []
                query_data = []
                model, data = run_KV(
                    alphabet=alphabet,
                    sul=sul,
                    eq_oracle=eq_oracle,
                    automaton_type='vpa',
                    print_level=2,
                    cex_processing=cex,
                    return_data=True
                )
                states_data.append(alphabet_size * 3)
                query_data.append(data['queries_learning'])

                new_data_dict_pickle[cex].append((alphabet_size * 3, x, data['learning_rounds']))
                new_data_dict_pickle[cex].append((alphabet_size * 3, x, data['automaton_size']))
                new_data_dict_pickle[cex].append((alphabet_size * 3, x, data['queries_learning']))
                new_data_dict_pickle[cex].append((alphabet_size * 3, x, data['steps_learning']))
                new_data_dict_pickle[cex].append((alphabet_size * 3, x, data['queries_eq_oracle']))
                new_data_dict_pickle[cex].append((alphabet_size * 3, x, data['steps_eq_oracle']))
                new_data_dict_pickle[cex].append((alphabet_size * 3, x, data['learning_time']))
                new_data_dict_pickle[cex].append((alphabet_size * 3, x, data['eq_oracle_time']))
                new_data_dict_pickle[cex].append((alphabet_size * 3, x, data['total_time']))
                new_data_dict_pickle[cex].append((alphabet_size * 3, x, data['cache_saved']))

            states_data_median.append(np.median(states_data))
            query_data_median.append(np.median(query_data))

        data_dict[cex] = (states_data_median, query_data_median)

    for cex in new_data_dict_pickle:
        existing_data[cex].extend(new_data_dict_pickle[cex])

    # Write the updated dictionary back to the file (using 'wb' to overwrite the previous content)
    with open(filename, 'wb') as file:
        pickle.dump(existing_data, file)

    # plot
    # plt.figure()
    # plt.xlabel('Size of the input alphabet')
    # plt.ylabel('Number of membership queries')
    # plt.title('Query growth of a random SEVPA with increasing alphabet size')
    # for key in data_dict:
    #     plt.plot(data_dict[key][0], data_dict[key][1], label=key)
    # plt.legend()
    # plt.savefig('alphabet_increasing.png')


def alphabet_increasing_variable():
    print("Benchmarking for variably increasing alphabet size")
    repeats = 10
    max_alphabet_size = 10

    data_dict = defaultdict(tuple)
    data_dict_pickle = defaultdict(list)
    alphabet_types = ['int', 'call', 'ret']

    for alphabet_type in alphabet_types:
        print(alphabet_type)
        states_data_median = []
        query_data_median = []
        for alphabet_size in range(1, max_alphabet_size + 1):
            print(alphabet_size)
            for x in range(repeats):
                if alphabet_type == 'int':
                    random_svepa = generate_random_sevpa(num_states=75, internal_alphabet_size=alphabet_size,
                                                         call_alphabet_size=1,
                                                         return_alphabet_size=1,
                                                         acceptance_prob=0.4,
                                                         return_transition_prob=0.5)
                elif alphabet_type == 'call':
                    random_svepa = generate_random_sevpa(num_states=75, internal_alphabet_size=alphabet_size,
                                                         call_alphabet_size=1,
                                                         return_alphabet_size=1,
                                                         acceptance_prob=0.4,
                                                         return_transition_prob=0.5)
                elif alphabet_type == 'ret':
                    random_svepa = generate_random_sevpa(num_states=75, internal_alphabet_size=alphabet_size,
                                                         call_alphabet_size=1,
                                                         return_alphabet_size=1,
                                                         acceptance_prob=0.4,
                                                         return_transition_prob=0.5)

                alphabet = random_svepa.input_alphabet

                sul = SevpaSUL(random_svepa)

                eq_oracle = RandomWordEqOracle(alphabet=alphabet.get_merged_alphabet(), sul=sul, num_walks=10000,
                                               min_walk_len=10, max_walk_len=30)

                states_data = []
                query_data = []
                model, data = run_KV(alphabet=alphabet, sul=sul, eq_oracle=eq_oracle, automaton_type='vpa',
                                     print_level=0, cex_processing='rs', return_data=True)
                states_data.append(alphabet_size)
                query_data.append(data['queries_learning'])
                data_dict_pickle[alphabet_type].append((alphabet_size, x, data['learning_rounds']))
                data_dict_pickle[alphabet_type].append((alphabet_size, x, data['automaton_size']))
                data_dict_pickle[alphabet_type].append((alphabet_size, x, data['queries_learning']))
                data_dict_pickle[alphabet_type].append((alphabet_size, x, data['steps_learning']))
                data_dict_pickle[alphabet_type].append((alphabet_size, x, data['queries_eq_oracle']))
                data_dict_pickle[alphabet_type].append((alphabet_size, x, data['steps_eq_oracle']))
                data_dict_pickle[alphabet_type].append((alphabet_size, x, data['learning_time']))
                data_dict_pickle[alphabet_type].append((alphabet_size, x, data['eq_oracle_time']))
                data_dict_pickle[alphabet_type].append((alphabet_size, x, data['total_time']))
                data_dict_pickle[alphabet_type].append((alphabet_size, x, data['cache_saved']))

            states_data_median.append(np.median(states_data))
            query_data_median.append(np.median(query_data))

            # Save data_dict to a pickle file
            with open('alphabet_increasing_variable.pickle', 'wb') as file:
                pickle.dump(data_dict_pickle, file)

        data_dict[alphabet_type] = (states_data_median, query_data_median)

    # plot
    plt.figure()
    plt.xlabel('Size of the input alphabet')
    plt.ylabel('Number of membership queries')
    plt.title('Query growth of a random SEVPA with increasing alphabet size')
    for key in data_dict:
        plt.plot(data_dict[key][0], data_dict[key][1], label=key)
    plt.legend()
    plt.savefig('alphabet_increasing_variable.png')


def benchmark_vpa_dfa():
    max_learning_rounds = 200
    data_dict = defaultdict(tuple)
    data_dict_pickle = defaultdict(list)
    label_data = []

    labels = ['1', '2', '3.1', '3.2', '4', '6', '8', '9', '10', '11', '12']

    for i, vpa in enumerate(
            [vpa_L1(), vpa_L2(), vpa_for_L3(), vpa_L3(), vpa_L4(), vpa_L6(),
             vpa_L8(), vpa_L9(), vpa_L10(), vpa_L11(), vpa_L12()]):
    # for i, vpa in enumerate(
    #         [vpa_for_L3(), vpa_L3(), vpa_L4(), vpa_L6(),
    #          vpa_L8(), vpa_L9(), vpa_L10(), vpa_L11(), vpa_L12()]):
        label = f'CFG {labels[i]}'
        print(f'--- {label} ---')
        label_data.append(label)

        model_under_learning = vpa

        alphabet_sevpa = SevpaAlphabet(list(model_under_learning.internal_set),
                                       list(model_under_learning.call_set),
                                       list(model_under_learning.return_set))

        alphabet_dfa = model_under_learning.input_alphabet.get_merged_alphabet()

        sul_vpa = VpaSUL(vpa)
        sul_dfa = DfaSUL(vpa)

        eq_oracle_vpa = RandomWordEqOracle(alphabet=alphabet_sevpa.get_merged_alphabet(), sul=sul_vpa, num_walks=10000,
                                       min_walk_len=2, max_walk_len=200)
        eq_oracle_dfa = RandomWordEqOracle(alphabet=alphabet_sevpa.get_merged_alphabet(), sul=sul_dfa, num_walks=100000,
                                       min_walk_len=2, max_walk_len=500)

        eq_oracle_w = WMethodEqOracle(alphabet=alphabet_sevpa.get_merged_alphabet(),sul=sul_dfa, max_number_of_states=50)

        model_vpa, data_vpa = run_KV(alphabet=alphabet_sevpa, sul=sul_vpa, eq_oracle=eq_oracle_vpa, automaton_type='vpa',
                                     print_level=0, cex_processing='rs', return_data=True,
                                     max_learning_rounds=max_learning_rounds)

        model_dfa, data_dfa = run_KV(alphabet=alphabet_dfa, sul=sul_dfa, eq_oracle=eq_oracle_w, automaton_type='dfa',
                                     print_level=3, cex_processing='rs', return_data=True,
                                     max_learning_rounds=50)

        # visualize_automaton(model_dfa)

        # print(data_dfa['l'])

        data_dict[label] = (data_vpa['automaton_size'], data_dfa['automaton_size'])

        data_dict_pickle[label].append((data_vpa['learning_rounds'], data_dfa['learning_rounds']))
        data_dict_pickle[label].append((data_vpa['automaton_size'], data_dfa['automaton_size']))
        data_dict_pickle[label].append((data_vpa['queries_learning'], data_dfa['queries_learning']))
        data_dict_pickle[label].append((data_vpa['steps_learning'], data_dfa['steps_learning']))
        data_dict_pickle[label].append((data_vpa['queries_eq_oracle'], data_dfa['queries_eq_oracle']))
        data_dict_pickle[label].append((data_vpa['steps_eq_oracle'], data_dfa['steps_eq_oracle']))
        data_dict_pickle[label].append((data_vpa['learning_time'], data_dfa['learning_time']))
        data_dict_pickle[label].append((data_vpa['eq_oracle_time'], data_dfa['eq_oracle_time']))
        data_dict_pickle[label].append((data_vpa['total_time'], data_dfa['total_time']))
        data_dict_pickle[label].append((data_vpa['cache_saved'], data_dfa['cache_saved']))

        # Save data_dict to a pickle file
        with open('benchmark_vpa_dfa_w_method.pickle', 'wb') as file:
            pickle.dump(data_dict_pickle, file)

    #plotting
    keys = list(data_dict.keys())
    values = list(data_dict.values())
    data1, data2 = zip(*values)

    # Creating bar graph
    bar_width = 0.35
    index = np.arange(len(keys))
    plt.bar(index, data1, bar_width, label='Data VPA', align='center')
    plt.bar(index + bar_width, data2, bar_width, label='Data DFA', align='center')

    plt.xlabel('VPA Instances')
    plt.ylabel('Number of Queries')
    plt.title('Bar Graph of Queries for VPA and DFA')
    plt.xticks(index + bar_width / 2, label_data)
    plt.legend()
    plt.savefig('benchmark_vpa_dfa_all_L.png')


# choose which benchmark to execute
# state_increasing()
# alphabet_increasing()
# alphabet_increasing_variable()
benchmark_vpa_dfa()
