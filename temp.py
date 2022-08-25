from rich import print
from rich.tree import Tree


# Abstract
abstract_tree = Tree("Data Pulls")

month = abstract_tree.add("YYYY-mm")
month.add("Data Pull Title")
month.add("Data Pull Title")
month.add("Data Pull Title")

month = abstract_tree.add("YYYY-mm")
month.add("Data Pull Title")

month = abstract_tree.add("YYYY-mm")
month.add("Data Pull Title")
month.add("Data Pull Title")

print(abstract_tree)
print()


# Concrete
concrete_tree = Tree("Data Pulls")

month = concrete_tree.add("2022-08")
month.add("ORO_Training_Infant_Toddler_Coding")

month = concrete_tree.add("2022-07")
month.add("TA_Time_Per_Network")

month = concrete_tree.add("2022-06")
month.add("Capacity_Year_Over_Year")
month.add("County_Desired_Capacity_Vs_Licensed")
month.add("Licensed_Year_Over_Year")

month = concrete_tree.add("2022-05")
month.add("Facilites_Per_County_Per_Year")

print(concrete_tree)
print()


# Abstract
abstract_tree = Tree("Reports")

rep = abstract_tree.add("Report_Title")
rep.add("Temporal_Data")
rep.add("Temporal_Data")
rep.add("Temporal_Data")
rep = abstract_tree.add("Report_Title")
rep.add("Temporal_Data")
rep = abstract_tree.add("Report_Title")
rep.add("Temporal_Data")
rep.add("Temporal_Data")
rep = abstract_tree.add("Report_Title")
rep.add("Temporal_Data")

print(abstract_tree)
print()


# Concrete
concrete_tree = Tree("Reports")

rep = concrete_tree.add("Market Price Study")
rep.add("2022")
rep = concrete_tree.add("Quarterly Reporting")
year = rep.add("2021-23")
year.add("Q8")
year.add("Q7")
year.add("Q6")
year.add("Q5")
year.add("Q4")
year.add("Q3")
year.add("Q2")
year.add("Q1")
year = rep.add("2018-20")
year.add("Q8")
year.add("Q7")
year.add("Q6")
year.add("Q5")

print(concrete_tree)
print()


project = Tree("Report Title")
project.add("Project File")
project.add("Project File")
project.add("Project File")
project.add("Project File")
data = project.add("Data")
group = data.add("Data Group (year, etc)")
group.add("Data File")
group.add("Data File")
group.add("Data File")
group = data.add("Data Group (year, etc)")
group.add("Data File")
group = data.add("Data Group (year, etc)")
group.add("Data File")
group = data.add("Data Group (year, etc)")
group.add("Data File")
group.add("Data File")

print(project)
print()

project = Tree("Quarterly Reporting")
project.add("action_logs.py")
project.add("file_prompt.py")
project.add("quarterly_reporting.py")
project.add("requirements.txt")
project.add("setup.py")

data = project.add("Input")
data.add("2022-07-05.xlsx")
data.add("2022-07-25.xlsx")
data.add("2022-07-27.xlsx")

data = project.add("Output")
data.add("2022-07-05_out.xlsx")
data.add("2022-07-05.log")
data.add("2022-07-25_out.xlsx")
data.add("2022-07-25.log")
data.add("2022-07-27_out.xlsx")
data.add("2022-07-27.log")

data = project.add("Review")
rev = data.add("2022-07-05")
rev.add("2022-07-05_all_removed.xlsx")
rev.add("2022-07-05_duplicate_in_license.xlsx")
rev.add("2022-07-05_early_learning_hub.xlsx")
rev.add("2022-07-05_missing_regulation.xlsx")
rev.add("2022-07-05_test_in_license.xlsx")
rev = data.add("2022-07-27")
rev.add("2022-07-27_all_removed.xlsx")
rev.add("2022-07-27_duplicate_in_license.xlsx")
rev.add("2022-07-27_early_learning_hub.xlsx")
rev.add("2022-07-27_missing_regulation.xlsx")
rev.add("2022-07-27_test_in_license.xlsx")

print(project)
print()
