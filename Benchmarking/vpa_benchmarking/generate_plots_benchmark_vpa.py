import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import matplotlib as mpl


def clear_cex_data(pickle_filename, cex_to_remove):
    """
    Loads a single data object (a dictionary) from the pickle file,
    removes the entry with the specified key (cex_to_remove),
    and writes back the updated dictionary.

    Parameters:
      pickle_filename (str): The name of the pickle file.
      cex_to_remove: The key to remove from the dictionary.
    """
    # Load the existing data (assumed to be a dictionary)
    with open(pickle_filename, 'rb') as f:
        data_obj = pickle.load(f)

    # Remove the specified key if it exists
    if cex_to_remove in data_obj:
        print(f"Removing key: {cex_to_remove}")
        del data_obj[cex_to_remove]
    else:
        print(f"Key '{cex_to_remove}' not found in the data.")

    # Write the updated dictionary back to the file
    with open(pickle_filename, 'wb') as f:
        pickle.dump(data_obj, f)


# Example usage:
# clear_cex_data('alphabet_increasing.pickle', cex_to_remove="linear_bwd")


def plot_bar_graphs(filename, measure_name):
    mpl.rcParams['font.family'] = 'serif'

    measure_index_map = {
        "learning_rounds": 0,
        "automaton_size": 1,
        "queries_learning": 2,
        "steps_learning": 3,
        "queries_eq_oracle": 4,
        "steps_eq_oracle": 5,
        "learning_time": 6,
        "eq_oracle_time": 7,
        "total_time": 8,
        "cache_saved": 9
    }

    measure_names_list = [
        "Number of learning rounds",
        "Size of the automaton",
        "Number of membership queries",
        "Number of steps for membership queries",
        "Number of equivalence queries",
        "Number of steps for equivalence queries",
        "Seconds needed in the learning phase",
        "Seconds needed for conformance testing",
        "Total seconds to learn the automaton",
        "Number of saved queries by caching"
    ]

    measure_idx = measure_index_map[measure_name]

    with open(filename, 'rb') as file:
        data_dict_pickle = pickle.load(file)

    keys = list(data_dict_pickle.keys())
    vpa_values = []
    dfa_values = []

    for key in keys:
        # Each key maps to a list of tuples. Get the tuple at the specified measure index.
        # Each tuple is (data_vpa, data_dfa)
        measure_tuple = data_dict_pickle[key][measure_idx]
        vpa_values.append(measure_tuple[0])
        dfa_values.append(measure_tuple[1])

    # Creating the bar graph.
    bar_width = 0.35
    index = np.arange(len(keys))

    plt.figure()
    plt.bar(index, vpa_values, bar_width, label='KV for VPA', align='center')
    plt.bar(index + bar_width, dfa_values, bar_width, label='KV for DFA', align='center')

    plt.xlabel("Languages")
    plt.ylabel(measure_names_list[measure_idx])
    plt.title(f"Comparison for {measure_names_list[measure_idx]}")
    keys = [label.replace('VPA ', '') for label in keys]
    plt.xticks(index + bar_width / 2, keys)
    plt.legend()

    # Save the figure.
    save_path = os.path.join("vpa_vs_dfa", f"{measure_name}_bar.png")
    plt.savefig(save_path)
    plt.close()


def plot_line_graphs(filename, folder, xlabel, title, measure_name):
    mpl.rcParams['font.family'] = 'serif'

    measure_index_map = {
        "learning_rounds": 0,
        "automaton_size": 1,
        "queries_learning": 2,
        "steps_learning": 3,
        "queries_eq_oracle": 4,
        "steps_eq_oracle": 5,
        "learning_time": 6,
        "eq_oracle_time": 7,
        "total_time": 8,
        "cache_saved": 9
    }

    measure_names_list = [
        "Number of learning rounds",
        "Size of the automaton",
        "Number of membership queries",
        "Number of steps for membership queries",
        "Number of equivalence queries",
        "Number of steps for equivalence queries",
        "Seconds needed in the learning phase",
        "Seconds needed for conformance testing",
        "Total seconds to learn the automaton",
        "Number of saved queries by caching"
    ]

    if measure_name not in measure_index_map:
        raise ValueError("Invalid measure name. Choose from: " + ", ".join(measure_index_map.keys()))

    measure_idx = measure_index_map[measure_name]

    # Load the pickle file.
    with open(filename, 'rb') as file:
        data_dict_pickle = pickle.load(file)

    plt.figure()

    # Process data for each cex processing method.
    for cex, data_list in data_dict_pickle.items():
        # Group the chosen measure's values by the state size.
        grouped = defaultdict(list)
        # Since the code appends 10 items per experiment, select items where the index modulo 10 equals measure_idx.
        for i, (state, rep, value) in enumerate(data_list):
            if i % 10 == measure_idx:
                grouped[state].append(value)

        # Sort state sizes and compute the median for each.
        states = sorted(grouped.keys())
        medians = [np.median(grouped[state]) for state in states]

        plt.plot(states, medians, marker='o', label=cex)

    plt.xlabel(xlabel)
    plt.ylabel(measure_names_list[measure_idx])
    plt.title(f"{measure_names_list[measure_idx]} {title}")

    # Remove the grid from the background.
    plt.grid(False)

    # Set x-axis ticks for every natural number from 1 to 15.
    # plt.xticks(range(0  , 50))

    plt.legend()

    plt.subplots_adjust(left=0.15)

    save_path = os.path.join(folder, f"{measure_name}.png")
    plt.savefig(save_path)
    # plt.savefig(f"{measure_name}.png")
    plt.close()


measure_name_list = ["learning_rounds", "automaton_size", "queries_learning", "steps_learning", "queries_eq_oracle", "steps_eq_oracle",
                     "learning_time", "eq_oracle_time", "total_time", "cache_saved"]
for measure_name in measure_name_list:
    plot_line_graphs("state_increasing.pickle", measure_name=measure_name, folder="inc_nr_states", xlabel="Number of states in the VPA", title="for growing number of states")

for measure_name in measure_name_list:
    plot_line_graphs("alphabet_increasing.pickle", measure_name=measure_name, folder="inc_size_alphabet", xlabel="Size of alphabet", title="for growing size of the alphabet")

for measure_name in measure_name_list:
    plot_bar_graphs("benchmark_vpa_dfa.pickle", measure_name=measure_name)