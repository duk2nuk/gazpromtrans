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

def create_object_group_dict(input_data):
	regex = (
		r"(?P<obj_group_name>\S+)"
		r"\s+IP_Group\s+"
		r"(?P<obj_group_ip>\S+)"
	)
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
	for every in object_result_dict:
		for ip in obejct_result_dict["obj_group_ip"]:
			if ip.isdigit:
				pass
			else:
				print(ip)
	return object_result_dict

if __name__ == "__main__":
	output_obj = open_asa_config("raw_data_replace.txt")
	obj_dict = create_object_dict(output_obj)
	obj_group_dict = create_object_group_dict(output_obj)
	#pprint(obj_dict, width=200)
	#pprint(obj_group_dict, width=200)
	#with open("astrachan_result_fw.xml", "w") as result_obj_xml:
	#	env = Environment(loader=FileSystemLoader("templates"),trim_blocks=True, lstrip_blocks=True)
	#	template = env.get_template("policy_temp_astrakchan.xml")
	#	result_obj_xml.write(template.render(object_vars=obj_dict))	
