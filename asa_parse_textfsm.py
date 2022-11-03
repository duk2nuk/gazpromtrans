import sys
import textfsm
from tabulate import tabulate

asa_config_file = "asa_short.txt"
asa_template_file = "asa_config_template_textfsm.txt"
with open (asa_config_file) as asa_config_read:
    asa_config_output = asa_config_read.read()

with open(asa_template_file) as asa_template_read:
    re_table = textfsm.TextFSM(asa_template_read)
    header = re_table.header
    result = re_table.ParseText(asa_config_output)
print(tabulate(result, headers = header))
