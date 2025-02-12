import argparse
import timeit

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def benchmark_parser(arg_count, runs):
    parser = argparse.ArgumentParser()

    for i in range(arg_count):
        parser.add_argument(f"--arg{i}", type=int, default=0)

    # Add positional arguments
    for i in range(arg_count):
        parser.add_argument(f'pos{i}', type=int)

    # Create the list of arguments
    optional_args = [f'--arg{i}=1' for i in range(arg_count)]
    positional_args = [str(i) for i in range(arg_count)]
    args = optional_args + positional_args

    execution_time = timeit.timeit(lambda: parser.parse_args(args), number=runs)
    return execution_time

st.title("Argparse Benchmark")

arg_count = st.slider("Number of arguments", min_value=10, max_value=1000, value=10, step=10)
runs = st.number_input("Number of Runs (Higher is more accurate)", min_value=10, max_value=10000, value=1000, step=100)

if st.button("Run Benchmark"):
    execution_time = benchmark_parser(arg_count, runs)
    st.write(f"Benchmarking argparse with **{arg_count}** arguments, running **{runs}** times")

    results =[]
    for i in range(1, arg_count+1, 5):
        time_taken = benchmark_parser(i, runs)
        results.append({"Arguments": i, "Time": time_taken})
    
    df = pd.DataFrame(results)
    st.write(f"Execution time for {arg_count} args: **{df.iloc[-1]['Time']:.6f}** seconds")

    print(df)

    fig, ax = plt.subplots()
    ax.plot(df["Arguments"], df["Time"], marker='o')
    ax.set_xlabel("Number of Arguments")
    ax.set_ylabel("Time (s)")
    ax.set_title("Argparse Benchmark")
    st.pyplot(fig)