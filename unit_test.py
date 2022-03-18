import pytest
from Ship import *
from Container import *
from Node import *
from main import *
import os
from pathlib import Path

list_of_manifests_to_test = ['ShipCase1.txt','ShipCase2.txt','ShipCase3.txt','ShipCase4.txt','ShipCase5.txt']

"""
@pytest.mark.parametrize('manifest_for_testing', list_of_manifests_to_test)
def test_func_to_manifest_and_from_manifest(manifest_for_testing):
    filepath_of_test_manifest = manifest_for_testing
    test_ship = Ship()

    #write input file contents to the test_ship
    test_ship.from_manifest(manifest_for_testing)

    #ensure the output file exists, if not then create it
    out_file_path = Path('test_output_manifest.txt')
    out_file_path.touch(exist_ok=True)

    # write ship contents to the output file
    test_ship.to_manifest('test_output_manifest.txt')

    #get contents of the input and output files
    with open(manifest_for_testing) as input_file:
        contents_of_input_file = input_file.readlines()
    with open('test_output_manifest.txt') as output_file:
        contents_of_output_file = output_file.readlines()

    assert contents_of_input_file == contents_of_output_file
    os.remove('test_output_manifest.txt')

#only tests for manifest 4, moves containers in vertical column to other columns and back
def test_move_container():
    test_ship = Ship()
    test_ship.from_manifest('ShipCase4.txt')
    container_to_be_moved = test_ship.containers[7][4]
    test_ship.move_container(4,0)
    assert test_ship.containers[2][0].weight == 3044
    assert test_ship.containers[2][0].description == 'Pig'
    test_ship.move_container(4, 1)
    assert test_ship.containers[1][1].weight == 1100
    assert test_ship.containers[1][1].description == 'Doe'
    test_ship.move_container(4, 2)
    assert test_ship.containers[1][2].weight == 2020
    assert test_ship.containers[1][2].description == 'Owl'
    test_ship.move_container(4, 3)
    assert test_ship.containers[1][3].weight == 10000
    assert test_ship.containers[1][3].description == 'Ewe'
    test_ship.move_container(4, 0)
    assert test_ship.containers[3][0].weight == 2011
    assert test_ship.containers[3][0].description == 'Cow'
    test_ship.move_container(4, 1)
    assert test_ship.containers[2][1].weight == 2007
    assert test_ship.containers[2][1].description == 'Dog'
    test_ship.move_container(4, 2)
    assert test_ship.containers[2][2].weight == 2000
    assert test_ship.containers[2][2].description == 'Cat'

def test_swap_containers():
    test_ship = Ship()
    test_ship.from_manifest('ShipCase4.txt')
    test_ship.swap_containers_in_ship(1,4,7,4)
    assert test_ship.containers[7][4].weight == 2000
    assert test_ship.containers[7][4].description == 'Cat'
    assert test_ship.containers[1][4].weight == 3044
    assert test_ship.containers[1][4].description == 'Pig'




def test_get_heuristic():
    test_ship = Ship()
    test_ship.from_manifest('ShipCase4.txt')
    test_ship.calculate_weight_left_right_sides_of_ship()
    assert test_ship.get_heuristic_balance() > 0

def test_find_container():
    test_ship = Ship()
    test_ship.from_manifest('ShipCase4.txt')
    container_found = test_ship.find_container(1100,'Doe')
    print(container_found)
    assert container_found.weight == 1100
    assert container_found.description == 'Doe'
    assert container_found.row == 6
    assert container_found.column == 4
"""
def test_balance_ship():
    test_ship = Ship()
    #test_ship.from_manifest('ShipCaseHeuristic4.txt')
    #test_ship.from_manifest('ShipCase5.txt')
    test_ship.from_manifest('ShipCase50Containers.txt')
    test_ship.setup_top_available_container_row_indexes()
    test_ship.calculate_weight_left_right_sides_of_ship()
    solution = balance_ship(test_ship)
    #print(solution.ship)

def test_get_top_containers():
    test_ship = Ship()
    test_ship.from_manifest('ShipCase3.txt')
    test_ship.setup_top_available_container_row_indexes()
    top_containers = test_ship.get_list_of_top_containers()
    #print(top_containers)


def test_get_centermost_container():
    test_ship = Ship()
    test_ship.from_manifest('ShipCase2.txt')
    test_ship.setup_top_available_container_row_indexes()
    top_containers = test_ship.get_list_of_top_containers()
    column_left = test_ship.get_centermost_container(1)
    distance = abs(column_left - test_ship.width/2)
    column_right = test_ship.get_centermost_container(0)
    distance_right = abs(column_right - (test_ship.width/2 - 1))
    #assert column_left ==



def test_calculate_heuristic():
    test_ship = Ship()
    test_ship.from_manifest('ShipCase5.txt')
    node_for_test = Node(test_ship,0,0)
    heuristic = node_for_test.calculate_heuristic()
    print(heuristic)


