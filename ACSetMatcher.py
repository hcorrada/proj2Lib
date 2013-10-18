from proj2Lib.ExactMatcher import ExactMatcher 
from proj2Lib.ExactMatcher import ExactMatcherNode
from collections import deque

# UPDATE THIS FILE TO IMPLEMENT THE AHO-CORASICK ALGORITHM
class ACSetMatcherNode(ExactMatcherNode):
	def __init__(self, root=False):
		super(ACSetMatcherNode, self).__init__(root)
		self.output = -1

	def isOutput(self):
		return not self.output < 0

class ACSetMatcher(ExactMatcher):
	def __init__(self, patterns, reportFormat='Found match of pattern {1} in position {0}'):
		self.root = ACSetMatcherNode(root=True)
		self.reportFormat = reportFormat
		self.patternLengths = [len(x) for x in patterns]
		self.patternLength = min(self.patternLengths)

		# do initialization here 
		# don't use super call since that uses preprocessPattern which we don't want to do here
		self.preprocessPatterns(patterns)
		
	def reportMatch(self, i, output):
		print self.reportFormat.format(i - self.patternLengths[output], output)

	def buildKeywordTree(self, patterns):
		self.root.setFailureLink(self.root)
		self.root.targetShift = 1

		for i in xrange(len(patterns)):
			pattern = patterns[i]
			currentNode = self.root
			for x in pattern:
				if currentNode.isMatch(x):
					currentNode, _ = currentNode.getTransition(x)
				else:
					newNode = ACSetMatcherNode()
					newNode.setFailureLink(self.root)
					newNode.targetShift = 0
					currentNode.setChild(x, newNode)
					currentNode = newNode
			currentNode.output = i

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

	def matchTarget(self, target):
		assert len(target) >= self.getPatternLength()

		# start at the root
		currentNode = self.root

		# start in the first position of the target
		i = 0  
		while i <= len(target):
			# check if this is an output node
			if currentNode.isOutput():
				self.reportMatch(i, currentNode.output)
			
			if i == len(target):
				break

			c = target[i]
#			print 'i:', i, c

#			print 'curNode:', currentNode

			# get the current target character

		
			# try to matching it to an exiting edge on the current node
			# if current node is a leaf, this function updates correctly
			(currentNode, targetShift) = currentNode.getTransition(c)

#			print 'shift', targetShift, '\n'
			i += targetShift
