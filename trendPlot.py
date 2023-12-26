
import json
import os 
import sys
import matplotlib.pyplot as plt


def read_file(file_path):
    
    with open(file_path, 'r') as data_file:
        #print("reading file", file_path)
        dict_from_file = json.load(data_file)

        return dict_from_file


def read_all_data(path,all_sim_data):
    #Läsa in alla json filer i mappen

    if os.path.isfile(path):
        #print("path when reading file:", path)
        dict_from_file = read_file(path)

        basename = os.path.basename(path)

        file_name,_ = os.path.splitext(basename)

        all_sim_data[file_name] = dict_from_file

    elif os.path.isdir(path):
        all_dir_items = os.listdir(path)
        all_dir_items = sorted(all_dir_items, key=lambda x: int(x.split('_')[-1].split('.')[0]))
        #print("Files in dir", all_dir_items)

        for item in all_dir_items:
            next_path = path + "/" + item

            read_all_data(next_path,all_sim_data)

    else:
        print("Path provided is neither files nor directory!")

    return all_sim_data


def get_season_start_plantData(data_dict, time):
    #Skicka in alla dics, plus ev key word?, alltså "flowerdata", "pollenData", "beeData"
    #Plocka ut första elementet i varje säsong
    #Skicka in vilka element vi vill ta ut
    
    return data_dict[time]

def get_season_start_beeData(data_dict, time):
    #Plocka ut första elementet i varje säsong
    #Skicka in vilka element vi vill ta ut
    #"beeData"





    return

def fetch_data_at_season_index(data_dict,time = 0):

    dict_bee = {}
    dict_pollen = {}
    dict_flower = {}

    #season_values = ["season_0","season_1","season_2","season_3","season_4"]

    for simulation in data_dict:
        temp_list_pollen = []
        temp_list_flower = []
        temp_list_bee = []
        
        simulation_values = data_dict.get(simulation)
        #print("Simuleringsvärden:",simulation_values)
        for season in simulation_values:
            season_value = simulation_values.get(season)
            #print("\n Säsongsvärden:",season_value)
            for result_type in season_value: 
                result_list = season_value.get(result_type)
                if result_type == "beedata":
                    temp_list_bee.append(result_list[time])

                elif result_type == "pollendata":
                    temp_list_pollen.append(result_list[time])

                elif result_type == "flowerdata":
                    temp_list_flower.append(result_list[time])

                else:
                    print("Not supported result type")

        dict_bee[simulation] = temp_list_bee
        dict_flower[simulation] = temp_list_flower
        dict_pollen[simulation] = temp_list_pollen
        
    return dict_bee, dict_flower, dict_pollen


def plot(result_dict,title):
    
    seasons = [f"Season {i+1}" for i in range(5)]

    # Plotting the data
    for key, values in result_dict.items():
        plt.plot(seasons, values, label=key)

    # Adding labels and legend
    plt.xlabel('Season')
    plt.ylabel('Values')
    plt.title(title)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

    # Show the plot
    plt.show()

def subplot(dict1, dict2, dict3, title1,title2, title3):
    seasons = [f"Season {i+1}" for i in range(5)]

    # Create subplots
    fig, axes = plt.subplots(3, 1, figsize=(8, 12))

    # Plotting the data for the first dictionary
    for key, values in dict1.items():
        axes[0].plot(seasons, values, label=key)
    axes[0].set_ylabel('Values')
    axes[0].set_title(title1)
    axes[0].legend(loc='upper left', bbox_to_anchor=(1, 1))

    # Plotting the data for the second dictionary
    for key, values in dict2.items():
        axes[1].plot(seasons, values, label=key)
    axes[1].set_ylabel('Values')
    axes[1].set_title(title2)
    axes[1].legend(loc='upper left', bbox_to_anchor=(1, 1))

    # Plotting the data for the third dictionary
    for key, values in dict3.items():
        axes[2].plot(seasons, values, label=key)
    axes[2].set_xlabel('Season')
    axes[2].set_ylabel('Values')
    axes[2].set_title(title3)
    axes[2].legend(loc='upper left', bbox_to_anchor=(1, 1))

    # Adjust layout and show the plot
    plt.tight_layout()
    plt.show()

def sum_sub_dict_values(simulation_dict):
    
    result_dict = {}
    for simulation in simulation_dict:
        list_of_dictionaries = simulation_dict.get(simulation)
        
        result_list = [sum(list_item.values()) for list_item in list_of_dictionaries]
        
        result_dict[simulation] = result_list
        
    return result_dict    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    all_sim_data = {}

    data_dict = read_all_data(file_path,all_sim_data)

    dict_bee, dict_flower, dict_pollen= fetch_data_at_season_index(data_dict,time = 0)

    #print("BEE data", dict_bee)

    result_dict_bee = sum_sub_dict_values(dict_bee)
    result_dict_flower = sum_sub_dict_values(dict_flower)
    result_dict_pollen = sum_sub_dict_values(dict_pollen)

    subplot(result_dict_bee, result_dict_flower, result_dict_pollen, "Bee data","Flower data", "Pollen data")



    #Iterera genom dict först genom varje körning
    #

    #Plotta all data, total och icke total


