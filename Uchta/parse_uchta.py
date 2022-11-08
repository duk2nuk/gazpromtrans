import re
from pprint import pprint
from jinja2 import Environment, FileSystemLoader

def parse_asa_rules_to_dict(file_name):
	regex = (
		r"pass\s+(?P<source>\d+.\d+.\d+.\d+|any)\s+"
		r"((?P<s_mask>255.\d+.\d+.\d+)\s+)?"
		r"(?P<dst>\d+.\d+.\d+.\d+|any)\s+"
		r"((?P<dst_mask>255.\d+.\d+.\d+)\s+)?"
		r"((?P<proto>\S+)$)"
	)
	
	all_result_dict = {}
	with open(file_name) as f:
		id = 1
		for line in f:
			result_dict = {}
			#print(line)
			match = re.match(regex, line)
			if match:
				source_ip = match.group("source")
				source_mask = match.group("s_mask")
				dst_ip = match.group("dst")
				dst_mask = match.group("dst_mask")
				protocol = match.group("proto")
				result_dict[int(id)]={"source":source_ip, "source_mask":source_mask, "dst_ip":dst_ip, "dst_mask":dst_mask, "protocol":protocol}
				all_result_dict.update(result_dict)
				id+=1
	return all_result_dict

if __name__ == "__main__":
	result_uchta = parse_asa_rules_to_dict("uchta_rules.txt")
	with open("uchta_result_fw.xml", "w") as result_obj_xml:
		env = Environment(loader=FileSystemLoader("templates"),trim_blocks=True, lstrip_blocks=True)
		template = env.get_template("policy_temp.xml")
		result_obj_xml.write(template.render(object_vars=result_uchta))
	pprint(result_uchta)