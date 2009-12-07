import xml.parsers.expat
import pickle


class converter:
	def __init__(self, xmlf=False, pyxf=False):
		self.xmlf = xmlf
		self.pyxf = pyxf

	def char(self):
		if self.textnode.strip():
			text = " " + self.textnode.replace("\n"," ") + " "
			while True:
				if text.find("  ") != -1:
					text = text.replace("  "," ")
				else: break
			self.pyxfo.write(("-"+text+"\n").encode('utf-8'))
			self.textnode = ""
			
	def char_data(self, data):
		self.textnode += data
		
	def start_element(self, name, attrs):
		self.char()
		self.pyxfo.write(("("+name+"\n").encode('utf-8'))
		for key, val in attrs.items():
			self.pyxfo.write(("A"+key+" "+val+"\n").encode('utf-8'))
			
	def end_element(self, name):
		self.char()
		self.pyxfo.write((")"+name+"\n").encode('utf-8'))
	
	def xml2pyx(self):
		self.textnode = ""
		self.xmlfo = open(self.xmlf, 'r')
		self.pyxfo = open(self.pyxf, 'w')
		p = xml.parsers.expat.ParserCreate()
		p.StartElementHandler = self.start_element
		p.EndElementHandler = self.end_element
		p.CharacterDataHandler = self.char_data
		p.ParseFile(self.xmlfo)
		self.xmlfo.close()
		self.pyxfo.close()

class Parser:
	def validate(self, node):
		pass
	def parse(self, fobj):
		self.fobj = fobj
		tagstack = []
		self.root = None
		line_num = 0
		for line in self.fobj.readlines():
			line = line.decode('utf-8').lstrip().rstrip("\n")
			line_num += 1
			# blank line
			if not line.strip():
				continue
			
			if line.startswith("A"):
				item = line[1:].split(" ",1)
				tagstack[-1].attributes[item[0]] = item[1]
			elif line.startswith("("):
				tag = line[1:]
				if tag.find(":") != -1:
					tag = tag.split(":",1)[-1].strip()
					node = Node(line=line_num, tag=tag)
					tagstack[-1].named_children[tag] = node
				else:
					node = Node(line=line_num, tag=tag)
					if tagstack:
						tagstack[-1].children.append(node)
				if not tagstack:
					self.root = node
				tagstack.append(node)
			elif line.startswith(")"):
				# This element is complete, time to validate it
				self.validate(tagstack.pop())
			elif line.startswith("-"):
				node = Node(line=line_num, text = line[1:])
				tagstack[-1].children.append(node)
				self.validate(node)
			elif line == "%":
				break
			else:
				raise Exception("Unparseable line %d" % line_num)
			self.fobj.close()
		if len(tagstack) != 0:
			print "Unmatched tags!"
		return self.root
	def output(self, filename):
		out = open(filename, "w")
		output = "(%s\n%s)%s\n" % (self.root.tag, self.root.output(), self.root.tag)
		out.write(output.encode('utf-8'))
		out.close()

class Node:
	def __init__(self, line, tag=False, text=False):
		self.line = line
		self.tag = tag
		self.text = text
		self.attributes = {}
		self.named_children = {}
		self.children = []
	def __len__(self):
		return len(self.children)
	def __getitem__(self, key):
		if type(key) == type(1):
			return self.children[key]
		else:
			if key in self.attributes:
				return self.attributes[key]
			elif key in self.named_children:
				return self.named_children[key]
			else:
				return []
	def __contains__(self, key):
		return key in self.attributes or key in self.named_children
	def __setitem__(self, key, value):
		if type(key) == type(1):
			self.children[key] = value
		else:
			self.named_children[key] = value
	def __iter__(self):
		return iter(self.children)
	def append(self, val):
		self.children.append(val)
	def output(self, level=1):
		space = " " * level
		if self.text:
			return space + "-" + self.text + "\n"
		else:
			text = ""
			for key, val in self.attributes.items():
				text += space + "A" + key + " " + val + "\n"
			for child in self.named_children.values():
				if child.text:
					text = child.output(level)
				else:
					tag = self.tag + ":" + child.tag
					text += space + "(" + tag + "\n"
					text += child.output(level + 1)
					text += space + ")" + tag + "\n"
			for child in self.children:
				if child.text:
					text += child.output(level)
				else:
					text += space + "(" + child.tag + "\n"
					text += child.output(level + 1)
					text += space + ")" + child.tag + "\n"
			return text






















