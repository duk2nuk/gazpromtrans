import re
from pprint import pprint


def parse_asa_rules_to_dict(file_name):
	regex = (
		r"pass\s+(?P<source>\d+.\d+.\d+.\d+|any)\s+"
		r"((?P<s_mask>255.\d+.\d+.\d+)\s+)?"
		r"(?P<dst>\d+.\d+.\d+.\d+|any)\s+"
		r"((?P<dst_mask>255.\d+.\d+.\d+)\s+)?"
		r"((?P<proto>\S+)$)"
	)
	
	all_result_dict = []
	with open(file_name) as f:
		for line in f:
			result_dict = {}
			print(line)
			match = re.match(regex, line)
			if match:
				source_ip = match.group("source")
				source_mask = match.group("s_mask")
				dst_ip = match.group("dst")
				dst_mask = match.group("dst_mask")
				protocol = match.group("proto")
				result_dict={"source":source_ip, "source_mask":source_mask, "dst_ip":dst_ip, "dst_mask":dst_mask, "protocol":protocol}
				all_result_dict.append(result_dict)
	return all_result_dict

if __name__ == "__main__":
	result_uchta = parse_asa_rules_to_dict("uchta_rules.txt")
	pprint(result_uchta)