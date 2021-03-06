from os import path
from timer import Timer
import os

"""
All data is stored little-endian (easier to use on intel chips)
File structure
	- Header 128 bytes (this size in case its needed in the future)
		- [0:7] - number of entries
		- [8:9] - number of bytes per entry
		- rest of 128 bytes unused
	- Array
"""

"""
Current implementation uses a big'ol python array that is written to / read from memory
Future implementation may require dynamic bz2 style file chunked writing with a cache
"""

class BigArray :
	
	def __init__(self, name, size=None, bytes_per_entry = 1) :
		if(name[-5:] != ".egtb") :
			name += ".egtb"
		if(name[0:5] != "data/") :
			name = "data/" + name
		self.name = name 
		if(path.exists(name)) : # read in database
			self.writable = False
			with open(name, 'rb') as file :
				head = file.read(128)
				self.size = int.from_bytes(head[0:8], 'little')
				assert self.bytes_per_entry == head[8]
				self.data = file.read()
		else : # create database
			if size == None :
				raise ValueError("size must be specified when making an array")
			self.writable = True
			self.size = size
			self.data = bytearray(size * bytes_per_entry)

	def flush(self) :
		if not os.path.isdir('data/'):
			os.mkdir('data/')
		if not self.writable :
			raise Exception("Attempting flush read-only BigArray: " + self.name)
		head = bytearray(128)
		head_size = self.size.to_bytes(8, 'little')
		head_bpe = self.bytes_per_entry.to_bytes(1, 'little')
		for i in range(0, 8) :
			head[i] = head_size[i]
		head[8] = head_bpe[0]
		with open(self.name, "wb") as file :
			file.write(head)
			file.write(self.data)
		self.writable = False

	def __getitem__(self, index):
		if self.bytes_per_entry == 1 :
			return self.data[index]
		else :
			b_index = index * self.bytes_per_entry
			value = self.data[b_index : b_index + self.bytes_per_entry]
			return int.from_bytes(value, 'little')

	def __setitem__(self, index, value):
		if(not self.writable) :
			raise Exception("Attempting write to read-only BigArray: " + self.name)
		if self.bytes_per_entry == 1 :
			self.data[index] = value
		else :
			b_index = index * self.bytes_per_entry
			value = value.to_bytes(self.bytes_per_entry, 'little')
			for i in range(self.bytes_per_entry) :
				self.data[b_index + i] = value[i]

	def __len__(self) :
		return self.size

