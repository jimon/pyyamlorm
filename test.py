
import pyyamlorm

# first you define your basic classes
# they are used as templates to parse yaml

class Bar:
	a = 0
	b = 0

class Foo:
	c = '123'
	d = Bar
	e = [Bar]
	f = {"abc": Bar}
	g = set([1])

# then you write yaml file with template in mind

data = r"""
test1:
  c: well1
  d: {a: 1, b: 2}
  e: [{a: 3, b: 4}, {a: 3, b: 4}]
  f: {"k1": {a: 3, b: 4}}
  g: [1, 1, 2, 3]
test2:
  c: well2
  d: {a: 5, b: 6}
  e: [{a: 7, b: 8}]
  f: {"k2": {a: 3, b: 4}}
  g: [1, 3, 2, 3]
"""

# and we do all parsing/saving for you

objects = pyyamlorm.load(data, Foo)

print(objects)

print(pyyamlorm.dump(objects))