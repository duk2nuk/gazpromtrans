import re
import yaml
from pprint import pprint
from jinja2 import Environment, FileSystemLoader

def open_asa_config(asa_config_file):
	with open(asa_config_file) as asa_file:
		output = asa_file.read()
	return output

def create_object_dict(input_data):
	regex = (
		r"(?P<obj_name>\S+)"
		r"\s+IP_Address\s+"
		r"(?P<obj_ip>\S+)"
	)
	object_result_dict = {}
	result_search = re.finditer(regex,input_data)
	index=1
	for m in result_search:
		obj_name = m.group("obj_name")
		obj_ip = m.group("obj_ip")
		object_result_dict[obj_name] = {"obj_ip":obj_ip, "obj_num":index}
		index+=1
	return object_result_dict

def search_in_object_dict(obj_name, input_dict):
	#return id-number of an single object in input_dict
	value = None
	for i in input_dict:
		if obj_name == i:
			value = input_dict[obj_name]["obj_num"]
	return value
	
def normalize_object_dict(input_dict):
	regex_group_norm = (
		r"(?P<obj_gr>[\d.])"
	)
	old_input_dict = input_dict
	for key, value in old_input_dict.items():
		obj_group_ip, obj_group_num = value.values()
		new_list_obj_ip = []
		for i in obj_group_ip:
			i = str(i)
			result_match = re.search(regex_group_norm, i)
			if result_match:
				print(i)
				new_list_obj_ip.append(i)
			else:
				for key_search_match, val_search_match in old_input_dict.items():
					obj_group_ip_match, obj_group_num_match = val_search_match.values()
					if key_search_match == i:
						search_number = obj_group_num_match
						new_list_obj_ip.append(search_number)
			input_dict[key]["obj_group_ip"]=new_list_obj_ip		
	return(input_dict)
		#result_match = re.search(regex, key_value)
	#return key

def create_object_group_dict(input_data):
	regex = (
		r"(?P<obj_group_name>\S+)"
		r"\s+IP_Group\s+"
		r"(?P<obj_group_ip>.+)\t"
        r"(?P<desc>.+)?"
	)
	#regex_find_obj_name = (
	#	r"
	#)
	object_result_dict = {}
	result_search = re.finditer(regex,input_data)
	index=1
	for m in result_search:
		#print(m)
		obj_group_name = m.group("obj_group_name")
		obj_group_ip = m.group("obj_group_ip")
		obj_group_ip = obj_group_ip.split(";")
		new_obj_group_ip = []
		for i in obj_group_ip:
			search_result = search_in_object_dict(i,obj_dict)
			if search_result == None:
				new_obj_group_ip.append(i)
			else:
				new_obj_group_ip.append(search_result)
		object_result_dict[obj_group_name] = {"obj_group_ip":new_obj_group_ip, "obj_group_num":index}
		index+=1
	
	return object_result_dict

if __name__ == "__main__":
	output_obj = open_asa_config("raw_data_replace.txt")
	obj_dict = create_object_dict(output_obj)
	obj_group_dict = create_object_group_dict(output_obj)
	normalize_obj_group_dict = normalize_object_dict(obj_group_dict)
	#with open("obj_dict.yaml", "w") as obj_dict_yaml_write:
		#yaml.dump(obj_dict,obj_dict_yaml_write)
	#with open("obj_group_dict.yaml", "w") as obj_group_dict_yaml_write:
		#yaml.dump(obj_group_dict,obj_group_dict_yaml_write)
	with open("obj_group_dict_norm.yaml", "w") as obj_group_dict_norm_yaml_write:
		yaml.dump(normalize_obj_group_dict,obj_group_dict_norm_yaml_write)
	#pprint(obj_dict, width=200)
	#pprint(obj_group_dict, width=200)
	#with open("astrachan_result_fw.xml", "w") as result_obj_xml:
	#	env = Environment(loader=FileSystemLoader("templates"),trim_blocks=True, lstrip_blocks=True)
	#	template = env.get_template("policy_temp_astrakchan.xml")
	#	result_obj_xml.write(template.render(object_vars=obj_dict))	
    #check for save
