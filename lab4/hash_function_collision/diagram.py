from matplotlib import pyplot as plt


def construct_diagram(data: dict):
    fig = plt.figure(figsize=(12, 6))
    plt.xlabel("cores")
    plt.ylabel("time to match")
    plt.bar(data.keys(), data.values(), color="purple")
    plt.show()
