from proj2Lib.ExactMatcher import ExactMatcher 
from proj2Lib.ExactMatcher import ExactMatcherNode
from collections import deque

# UPDATE THIS FILE TO IMPLEMENT THE AHO-CORASICK ALGORITHM
class ACSetMatcherNode(ExactMatcherNode):
	def __init__(self, root=False):
		super(ACSetMatcherNode, self).__init__(root)
		self.output = -1
		self.outputLink = None

	def checkOutput(self, position, reportFormat):
		currentNode = self
		if not currentNode.output < 0:
			print reportFormat.format(position - self.depth, self.output)

		while not currentNode.outputLink is None and not currentNode.isRoot():
			currentNode = currentNode.outputLink
			print reportFormat.format(position - currentNode.depth, currentNode.output)

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
			return self.root, None

		w = node.failureLink
		while not w.isMatch(x) and not w.isRoot():
			w = w.failureLink
		if w.isMatch(x):
			failNode, _ = w.getTransition(x)
			outputLink = failNode if not failNode.output < 0 else failNode.outputLink
			return failNode, outputLink
		else:
			return self.root, None

	def preprocessPatterns(self, patterns):
		# use findFailureLink here to construct complete keyword tree for
		# pattern set
		self.buildKeywordTree(patterns)

		# now let's build the failure links
		d = deque([self.root])
		while len(d) > 0:
			currentNode = d.popleft()
			for (x, child) in currentNode.children.iteritems():
				failNode, outputLink = self.findFailureLink(currentNode, x)
				child.setFailureLink(failNode)
				child.outputLink = outputLink
				d.append(child)

	def matchTarget(self, target):
		assert len(target) >= self.getPatternLength()

		# start at the root
		currentNode = self.root

		# start in the first position of the target
		i = 0  
		fromMismatch = False
		while i <= len(target):
			# check if we need to output here
			if not fromMismatch:
				currentNode.checkOutput(i, self.reportFormat)
			fromMismatch = False

			if i == len(target):
				break

			c = target[i]
#			print 'i:', i, c

#			print 'curNode:', currentNode

			# get the current target character

		
			# try to matching it to an exiting edge on the current node
			# here we use isMatch first to avoid double reporting of matches
			fromMismatch = not currentNode.isMatch(c)
			(currentNode, targetShift) = currentNode.getTransition(c)

#			print 'shift', targetShift, '\n'
			i += targetShift
