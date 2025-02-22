import sys
import textwrap
import time

from rich.table import Table

from gui_executor.exec import exec_ui


# The reason for the two simple functions concatenate_args and compare_args is to
# be able to test that more than the first function is found.

@exec_ui(description="button function to concat arguments")
def concatenate_args(arg1, arg2):
    """Concatenates the two arguments with the '+' operator."""
    print(f"concatenate_args({arg1=}, {arg2=})")
    if arg1 is None or arg2 is None:
        raise ValueError("One of the arguments is empty and returns None, both arguments should contain a value")
    return arg1 + arg2


@exec_ui()
def compare_args(arg1, arg2):
    """Compares the two arguments with the '==' operator."""
    print(f"compare_args({arg1=}, {arg2=})")
    return arg1 == arg2


@exec_ui()
def func_with_args(x: int, y: float):
    print(f"func_with_args({x=}, {y=})")
    print(f"{type(x) = }, {type(y) = }")
    return x, y


@exec_ui()
def func_with_only_kwargs(*, a: str, b: int = 42, c):
    print(f"func_with_only_kwargs({a=}, {b=}, {c=})")
    return a, b, c


@exec_ui()
def long_duration_func():
    print("Sleeping for 10s..", flush=True)
    time.sleep(10)
    return "Done"


@exec_ui(use_gui_app=True)
def simple_plot(save: bool = False, png_dir: str = "/Users/rik/Desktop", png_filename: str = "plot.png"):
    """
    Create a simple plot and return fig, and ax.

    The figure can be inspected in the Qt Console as follows:

        fig, ax = response
        fig

    Then, you can add/change the figure to your needs:

        import numpy as np

        t = np.linspace(0,2*np.pi,100)
        h, a = 2, 2
        k, b = 2, 3
        x_2 = h + a*np.cos(t)
        y_2 = k + b*np.sin(t)
        ax.plot(x_2,y_2)
        ax.legend(['Eq 1', 'Eq 2'])
        fig

    """
    import matplotlib.pyplot as plt
    import numpy as np

    x_1 = np.linspace(-.5, 3.3, 50)
    y_1 = x_1 ** 2 - 2 * x_1 + 1

    fig, ax = plt.subplots()
    plt.title('Reusing this figure', fontsize=20)
    ax.plot(x_1, y_1)
    ax.set_xlabel('x', fontsize=18)
    ax.set_ylabel('y', fontsize=18, rotation=0, labelpad=10)
    ax.legend(['Eq 1'])
    ax.axis('equal')

    if save:
        print(f"Saving plot to {png_dir}/{png_filename} ...", flush=True)
        plt.savefig(f"{png_dir}/{png_filename}")

    print("Returning 'fig, and 'ax'...", flush=True)

    return fig, ax


@exec_ui(use_gui_app=True)
def two_simple_plots():
    import matplotlib.pyplot as plt
    import numpy as np
    import math

    # Data for plot 1

    t = np.arange(0.0, 2.0, 0.01)
    s = 1 + np.sin(2 * np.pi * t)

    fig1, ax = plt.subplots()
    ax.plot(t, s)

    ax.set(
        xlabel='time (s)', ylabel='voltage (mV)',
        title='About as simple as it gets, folks')
    ax.grid()

    # Data for plot 2

    n_points = 100
    xa = [i * 12 / 100 for i in range(n_points)]
    ya = [math.sin(x) * math.exp(-x/4) for x in xa]

    fig2, ax = plt.subplots()
    ax.plot(xa, ya)

    return fig1, fig2


@exec_ui(use_gui_app=True)
def a_simple_table():

    from faker import Faker

    table = Table(title="Configuration")

    table.add_column("Name", justify="left", style="cyan", no_wrap=True)
    table.add_column("Value", justify="right", style="green")

    faker = Faker()
    for _ in range(20):
        table.add_row(faker.name(), faker.address())

    return table


def some_text():
    from lorem_text import lorem

    return lorem.paragraphs(5)


@exec_ui(use_gui_app=True)
def a_plot_a_table_and_some_text():
    fig, ax = simple_plot()
    table = a_simple_table()
    text = some_text()
    return fig, table, text


@exec_ui(use_kernel=True)
def run_function_in_kernel(msg: str = "add your message here"):
    """
    When a function is executed in the kernel, its return value is available in
    the QtConsole in the 'response' variable (which will be overwritten).
    """
    print("Use in conjunction with qtconsole.")
    print("Return value will be available in QtConsole as 'response'...")

    return f"Message from 'run_function_in_kernel': {msg}"


@exec_ui(input_request=("Continue? > ", "Abort? > "))
def output_in_several_steps(n_steps: int = 10, sleep: float = 1.0):
    """
    This function goes through 'n_steps' steps and waits 'sleep' time between the steps.
    At each step, the step number is printed, then the functions sleeps. The intended
    use is to determine if we can catch the stdout while the function is running.

    The function asks for user input in step 3 and step 7. When the response in step 7 is 'Y'
    the process will end.

    Do not run this function in the kernel, because the kernel doesn't allow user
    interactions and the App will hang indefinitely.

    Args:
        n_steps (int): number of steps to take [default: 10]
        sleep (float): number of seconds to sleep between steps [default: 1.0]

    Returns:
        Nothing is returned.
    """
    for n in range(n_steps):
        print(f"step {n}..", flush=True)
        time.sleep(sleep)
        if n == 3:
            response = input("Continue? > ")
            print(response)
            if response.lower() == 'n':
                raise RuntimeError("No further steps requested.")
        elif n == 5:
            print(textwrap.dedent("""\
                    An error message...
                    Line two of the error message
                    ...and the last line of this error message
                """), file=sys.stderr, flush=True)
        elif n == 7:
            response = input("Abort? > ")
            print(response)
            if response.lower() == 'y':
                raise RuntimeError("Function was aborted!")


@exec_ui()
def bool_arg(x: bool = True):
    print(f"{x = }")
