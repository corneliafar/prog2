""" Python interface to the C++ Person class """
import ctypes
lib = ctypes.cdll.LoadLibrary('./libperson.so')
#lib = ctypes.cdll.LoadLibrary('C:\\Users\\Asus\\OneDrive\\Dokument\\ProgTek2\\MA4_Files\\libperson.so')

class Person(object):
	def __init__(self, age):
		lib.Person_new.argtypes = [ctypes.c_int]
		lib.Person_new.restype = ctypes.c_void_p
		lib.Person_get.argtypes = [ctypes.c_void_p]
		lib.Person_get.restype = ctypes.c_int
		lib.Person_set.argtypes = [ctypes.c_void_p,ctypes.c_int]
		lib.Person_delete.argtypes = [ctypes.c_void_p]
		self.obj = lib.Person_new(age)

	# 
	def fib(self, n):
		# ctypes.c_void_p (pointer to void) ctypes.c_int (integer = n)
		lib.Person_fib.argtypes = [ctypes.c_void_p, ctypes.c_int]
		lib.Person_fib.restype = ctypes.c_int
		# self.obj tells the C++ function which object to operate on,
		# returns result to Python
		return lib.Person_fib(self.obj, n) 

	def get(self):
		return lib.Person_get(self.obj)

	def set(self, age):
		lib.Person_set(self.obj, age)
        
	def __del__(self):
		return lib.Person_delete(self.obj)