with open("raw_data.txt") as input, open("raw_data_replace.txt", "w") as output:
	for line in input:
		line=line.replace(";\n", ";")
		line=line.replace("; ", ";")
		line=line.replace("Ip адрес", "IP_Address")
		line=line.replace("IP адрес", "IP_Address")
		line=line.replace("Группа ip адресов", "IP_Group")
		line=line.replace("Группа IP адресов", "IP_Group")
		line=line.replace("Группа IP_Addressов", "IP_Group")
		output.write(line)