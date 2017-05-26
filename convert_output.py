import os
import math

class Paper():
	def __init__(self, i, esession, duration, starting_time):
		self.id = i
		self.esession = esession
		self.duration = duration
		self.starting_time = starting_time	


allPapers = []
allEsession = []


def import_file():
	global allPapers, allEsession
	with open("data.out", "r") as f:
		line = f.readline()
		while (line):
			i, esession, duration, starting_time = line.split(",")
			cur_es = int(esession)
			p = Paper(int(i), cur_es, int(duration), int(starting_time))

			if cur_es not in allEsession:
				allEsession.append(cur_es)

			allPapers.append(p)
			line = f.readline()


def minutesToHourString(minutes):
	hour = minutes / 60
	minu  = minutes % 60

	hourSring = str(int(hour))
	if len(hourSring) == 1:
		hourSring = "0" + hourSring

	minString = str(minu)
	if len(minString) == 1:
		minString = "0" + minString

	return hourSring + ":" + minString


def print_esessions():
	global allEsession, allPapers
	for i, v in enumerate(allEsession):
		list_esession = list(filter(lambda x: int(x.esession)==int(v), allPapers))
		list_esession.sort(key=lambda x: x.starting_time)
		with open("final.out", "a") as f:
			for i, v in enumerate(list_esession):
				start = ""
				if (v.starting_time < 24*60):
				 	start = "30/09/2015 " + minutesToHourString(v.starting_time)
				elif (v.starting_time < 24*60*2):
			 		start = "01/10/2015 " + minutesToHourString(v.starting_time-(24*60))
				else:
					start = "02/10/2015 " + minutesToHourString(v.starting_time-(24*60*2))
				f.write("PaperId: {}, Esession: {}, Duration: {}, Position: {}, Start: {}\n".format(v.id, v.esession, v.duration, i+1, start))


def main():
	try:
		os.remove("final.out")
	except OSError:
		pass

	import_file()
	print_esessions()


if __name__ == '__main__':
    main()
