from proj2Lib.KMPMatcher import KMPMatcher

# UPDATE THIS CLASS TO IMPLEMENT SET MATCHING WITH THE KMP ALGORITHM
class KMPSetMatcher(object):
	def __init__(self, patterns):
		self.matchers = [KMPMatcher(patterns[i], reportFormat = 'Found match of pattern %d at position {0}' % i) for i in xrange(len(patterns))]

	def matchTarget(self, target):
		for matcher in self.matchers:
			matcher.matchTarget(target)
		
	def getTotalTime(self):
		sum = 0
		for matcher in self.matchers:
			sum += matcher.getTotalTime()
		return sum
