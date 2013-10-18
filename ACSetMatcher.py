from proj2Lib.ExactMatcher import ExactMatcher 
from proj2Lib.ExactMatcher import ExactMatcherNode
from collections import deque

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
					newNode.targetShift = 0
					currentNode.setChild(x, newNode)
					currentNode = newNode

	def findFailureLink(self,node,x):
		# implement algorithm of section 3.4.5
		# consult KMPMatcher to see how it uses the automata representation 
		# in that case
		
		# this function determines the failure link of child of 'node' with edge labeled 'x'
		if node.isRoot():
			return self.root

		w = node.failureLink
		while not w.isMatch(x) and not w.isRoot():
			w = w.failureLink
		if w.isMatch(x):
			failNode, _ = w.getTransition(x)
			return failNode
		else:
			return self.root

	def preprocessPatterns(self, patterns):
		# use findFailureLink here to construct complete keyword tree for
		# pattern set
		self.buildKeywordTree(patterns)

		# now let's build the failure links
		d = deque([self.root])
		while len(d) > 0:
			currentNode = d.popleft()
			for (x, child) in currentNode.children.iteritems():
				failNode = self.findFailureLink(currentNode, x)
				child.setFailureLink(failNode)
				d.append(child)

	# def matchTarget(self, target):
	# 	# For testing purposes, note that this method as defined by ExactMatcher
	# 	# implements the AC Search Algorithm of Section 3.4.4
	# 	#
	# 	# However, for the project you need to implement full AC Search Algorithm of Section 3.4.6
	# 	pass