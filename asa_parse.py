import re
import yaml
from pprint import pprint
from ports_dict import ports_dict
from jinja2 import Environment, FileSystemLoader

def open_asa_config(asa_config_file):
    with open(asa_config_file) as asa_file:
        output = asa_file.read()
    return output

def search_for_port_name(name,dict_with_ports):
    #return port number with port name in predefined dict from Cisco well-known ports
    port_number = None
    for i in dict_with_ports.keys():
        if name == i:
            port_number = dict_with_ports[i]
    return str(port_number)

def search_in_object_network_dict(object_name, input_dict):
    #return id-number of an single object in input_dict
    value = None
    for i in input_dict:
        if object_name == i:
            value = input_dict[object_name]["obj_num"]
    return value

def is_port_number(port):
    #check if number is word or number
    regex_port = (r"^[\d]{1,5}$")
    match_port = re.search(regex_port, port)
    if match_port:
        return True
    else:
        return False
def create_object_network_dict(input_data):
    #MAIN function for create full dict with single objects
    regex = (
        r"object network (?P<obj_net_name>\S+)\n"
        r" host (?P<obj_net_ip>\S+)\n"
        r"( sdescription (?P<obj_net_desc>.+)\n)?"
    )
    object_result_dict = {}
    result_search = re.finditer(regex,input_data)
    index=1
    for m in result_search:
        obj_name = m.group("obj_net_name")
        obj_ip = m.group("obj_net_ip")
        obj_desc = m.group("obj_net_desc")
        object_result_dict[obj_name] = {"object_ip":obj_ip, "object_desc":obj_desc, "obj_num":index}
        index+=1
    return object_result_dict

def create_object_group_dict(input_data,input_dict_1):
    #MAIN function for create 2 dicts with group ojects and group of ports
    regex_ip = (r"[\d.]{3,}")
    regex_port = (r"^[\d]{1,5}$")
    network_result_dict = {}
    service_result_dict = {}
    input_data_new = input_data.split("\n")
    net_name = None
    for line in input_data_new:
        line.strip()
        split_line = line.split()
        if "object-group" in line:
            obj_list = []
            port_list = []
            if "network" in split_line[1]:
                net_name = split_line[2]
                network_result_dict[net_name] = {}
            if "service" in split_line[1]:
                service_name = split_line[2]
                service_result_dict[service_name] = {}
        if "network-object" in line:
            if split_line[1] == "host":
                match_ip = re.search(regex_ip,split_line[2])
                if match_ip:
                    obj_list.append(split_line[2])
                else:
                    name_to_find_host = split_line[2]
                    value_host = search_in_object_network_dict(name_to_find_host,input_dict_1)
                    if value_host:
                        obj_list.append(value_host)
            if split_line[1] == "object":
                name_to_find_obj = split_line[2]
                value_obj = search_in_object_network_dict(name_to_find_obj,input_dict_1)
                obj_list.append(value_obj)
            network_result_dict[net_name].update({"hosts":obj_list})
        if "port-object" in line:
            if split_line[1] == "eq":
                match_port = is_port_number(split_line[2])
                if match_port:
                    port_list.append(split_line[2])
                else:
                    find_port = search_for_port_name(split_line[2],ports_dict)
                    port_list.append(find_port)
            if split_line[1] == "range":
                begin_port = split_line[2]
                end_port = split_line[3]
                if is_port_number(begin_port) == False:
                    begin_port = search_for_port_name(begin_port, ports_dict)
                if is_port_number(end_port) == False:
                    end_port = search_for_port_name(end_port, ports_dict)
                range_port = begin_port+"-"+end_port
                port_list.append(range_port)
            service_result_dict[service_name].update({"ports":port_list})
    return network_result_dict, service_result_dict  
   

if __name__ == "__main__":
    #
    #DEFINE ASA config file
    asa_output = open_asa_config("101-asa434._onlyobjtxt")
    #asa_output = open_asa_config("asa_short.txt")
    #
    #DEFINE OUTPUT DICT
    result_obj_net = create_object_network_dict(asa_output) #for single objects
    result_obj_gr = create_object_group_dict(asa_output,result_obj_net) #fro group objects
    #
    #WE can print our resul
    #pprint(result_obj_net, width=200)
    #pprint(result_obj_gr, width=200)
    #
    #DEFINE YAML file for output results dicts
    yaml_file_obj = "result_object_dict.yaml"     
    yaml_file_group_obj = "result_gr_object_dict.yaml"
        #with open (yaml_file_obj, "w") as yaml_obj_write:
    #    yaml.dump(result_obj_net, yaml__obj_write)
    with open (yaml_file_group_obj,"w") as yaml_obj_gr_write:
        yaml.dump(result_obj_gr, yaml_obj_gr_write)
    #with open (yaml_file_obj) as yaml_read:
    #    object_dict = yaml.safe_load(yaml_read)
    #
    #JINJA OUTPUT
    #env = Environment(loader=FileSystemLoader("templates"),trim_blocks=True, lstrip_blocks=True)
    #result_obj_xml.write(template.render(object_vars=result_obj_net))



