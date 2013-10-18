from proj2Lib.ExactMatcher import ExactMatcher 
from proj2Lib.ExactMatcher import ExactMatcherNode

# UPDATE THIS FILE TO IMPLEMENT THE AHO-CORASICK ALGORITHM
class ACSetMatcher(ExactMatcher):
	def __init__(self, patterns, reportFormat='Found match of pattern in position {0}'):
		self.root = ExactMatcherNode()
		self.reportFormat = reportFormat
		self.patternLengths = [len(x) for x in patterns]
		self.patternLength = min(self.patternLengths)

		# do initialization here 
		# don't use super call since that uses preprocessPattern which we don't want to do here
		self.preprocessPatterns(patterns)
		
	def buildKeywordTree(self, patterns):
		self.root.setFailureLink(self.root)
		self.root.targetShift = 1

		for pattern in patterns:
			currentNode = self.root
			for x in pattern:
				if currentNode.isMatch(x):
					currentNode, _ = currentNode.getTransition(x)
				else:
					newNode = ExactMatcherNode()
					newNode.setFailureLink(self.root)
					newNode.targetShift = currentNode.targetShift - 1
					currentNode.setChild(x, newNode)
					currentNode = newNode

	def findFailureLink(self,node,x):
		# implement algorithm of section 3.4.5
		# consult KMPMatcher to see how it uses the automata representation 
		# in that case
		pass

	def preprocessPatterns(self, patterns):
		# use findFailureLink here to construct complete keyword tree for
		# pattern set
		self.buildKeywordTree(patterns)


	# def matchTarget(self, target):
	# 	# For testing purposes, note that this method as defined by ExactMatcher
	# 	# implements the AC Search Algorithm of Section 3.4.4
	# 	#
	# 	# However, for the project you need to implement full AC Search Algorithm of Section 3.4.6
	# 	pass