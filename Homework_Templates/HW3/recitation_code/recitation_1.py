from src import CSVCatalog_Template_3 as CSVCatalog

import time
import json
import os

# The directory path containing data files.
data_dir = "../Data/core/"

def cleanup():
    """
    Deletes previously created information to enable re-running tests.
    :return: None
    """
    cat = CSVCatalog.CSVCatalog()
    cat.drop_table("people")
    cat.drop_table("batting")
    cat.drop_table("teams")

def test_create_1():
    cat = CSVCatalog.CSVCatalog()
    result = cat.create_table("awardsplayers", "../Data/core/AwardsPlayers.csv")

def test_get_table_1():
    cat = CSVCatalog.CSVCatalog()
    result = cat.get_table("awardsplayers")
    print("T = ", result)

def test_column_1():
    cd = CSVCatalog.ColumnDefinition("playerID", "mouse", True)

def test_column_2():
    cat = CSVCatalog.CSVCatalog()
    result = cat.get_table("awardsplayers")
    cd = CSVCatalog.ColumnDefinition("playerID", "text", True)
    result.add_column_definition(cd)

def test_get_table_3():
    cat = CSVCatalog.CSVCatalog()
    result = cat.get_table("awardsplayers")
    print("People = ", result)

def test_create_table_4():
    cat = CSVCatalog.CSVCatalog()
    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameLast", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameFirst", "text", True))
    result = cat.create_table(
        "people",
        "../Data/People.csv",
        cds
    )
    print("People = ", result)

def test_index_1():
    cat = CSVCatalog.CSVCatalog()
    pt = cat.get_table("people")
    pt.define_index("name_idx",  ['nameLast', 'nameFirst'], "INDEX")
    print("PT = ", pt)



#cleanup()
#test_create_1()
#est_get_table_1()
#test_column_2()
#test_get_table_3()
#test_create_table_4()
test_index_1()



