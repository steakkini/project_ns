"""
Instances of this class are used to store feature vectors for one login attempt.
Do not touchy touch and quickly forget about this mess :D
"""


class FeatureVector:

	def __init__(self):
		self.durations = []	 # list of delays (in milliseconds) between key strokes
		self.delays = []  # list of durations of key strokes

	def append_duration(self, time):
		self.durations.append(time)

	def append_delay(self, time):
		self.delays.append(time)

	def get_durations(self):
		return self.durations

	def get_delays(self):  # separate because during registering the first an last pause are omitted
		return self.delays[1:-1]  # remove the first and last element (i.e. the pause before and after ESC key)

	def get_features_string(self):
		features = ""
		
		for a in self.get_durations():
			if len(features) == 0:
				features = str(a)
			else:
				features = features + " " + str(a)
			
		for a in self.get_delays():
			if len(features) == 0:
				features = str(a)
			else:
				features = features + " " + str(a)

		return features

	def get_features_list(self):
		return self.get_durations() + self.get_delays()
