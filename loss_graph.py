import os
import matplotlib.pyplot as plt

def save_loss_graph(loss_data, filename="loss_graph.png"):
    """
    Saves a graph of the loss values to the 'graphs/' folder.

    Parameters:
    - loss_data: A list of loss values or a dictionary with lists of loss values.
    - filename: The name of the file to save the graph as (default: 'loss_graph.png').
    """
    # Ensure the 'graphs/' folder exists
    os.makedirs("graphs", exist_ok=True)

    # Plot the loss data
    plt.figure(figsize=(10, 6))
    if isinstance(loss_data, dict):
        for label, values in loss_data.items():
            plt.plot(values, label=label)
        plt.legend()
    elif isinstance(loss_data, list):
        plt.plot(loss_data, label="Loss")
        plt.legend()

    plt.title("Loss Graph")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.grid(True)

    # Save the graph to the 'graphs/' folder
    save_path = os.path.join("graphs", filename)
    plt.savefig(save_path)
    plt.close()

    print(f"Loss graph saved to {save_path}")


def parse_loss_file(filepath):
    """
    Parses the loss values from a text file and creates a dictionary with encoding methods as labels.

    Parameters:
    - filepath: Path to the text file containing loss data.

    Returns:
    - A dictionary with encoding methods as keys and loss values as lists.
    """
    loss_dict = {}
    with open(filepath, "r") as file:
        lines = file.readlines()
        current_label = None
        for line in lines:
            if line.startswith("Loss History for CNN with"):
                # Extract the encoding method
                current_label = line.split("with")[1].strip().replace(":", "")
                loss_dict[current_label] = []
            elif current_label and line.strip().startswith("["):
                # Parse the loss values
                loss_values = eval(line.strip())  # Convert string list to actual list
                loss_dict[current_label] = loss_values
    return loss_dict


if __name__ == "__main__":
    # Path to the result file
    result_file = "c:\\Users\\Not\\Documents\\Profissional\\Faculdade\\8_periodo\\quantica\\QCNN\\QCNN\\Result\\result_CNN.txt"

    # Parse the loss data
    loss_data_dict = parse_loss_file(result_file)

    # Print the parsed loss data
    for encoding, loss_values in loss_data_dict.items():
        print(f"Encoding: {encoding}, Loss Values: {loss_values}")

    # Save graphs for each encoding method
    for encoding, loss_values in loss_data_dict.items():
        save_loss_graph(loss_values, encoding)
