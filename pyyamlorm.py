
# Small yaml orm-like contraption
# This is needed in case if you have many objects described in yaml
# and you don't want to write parser by hand

# return dictionary of fields of interest from template class
def get_orm_fields(class_or_instance):
	return {k: getattr(class_or_instance, k) for k in dir(class_or_instance) if not k.startswith('__')}

# basic field is a string, int or float
def is_basic_field(obj):
	return isinstance(obj, str) or isinstance(obj, int) or isinstance(obj, float)

# makes a new instance or reuses current one
def make_instance(class_type):
	return class_type() if callable(class_type) else class_type

# constructs object from data and class_type
def load_obj(data, class_type, strict = True):
	if strict:
		assert data, "data must be present"

	# if it's a basic field, we just return data as is, or use default type as a value
	if is_basic_field(class_type):
		return data if data else make_instance(class_type)

	# if it's a list, we will try to see what data type we have
	elif isinstance(class_type, list):
		assert len(class_type) == 1, 'template list should contain only one value'
		assert strict and isinstance(data, list), 'data for list field also must be list'
		if isinstance(data, list): # if data is also a list, we will read it
			return [load_obj(item, class_type[0]) for item in data]
		else: #if data is not a list, we just create one instance from it
			return [load_obj(data, class_type[0])]

	# if it's a set, it's very similar to list
	elif isinstance(class_type, set):
		assert len(class_type) == 1, 'template set should contain only one value'
		assert strict and isinstance(data, list), 'data for set field must be a list'
		if isinstance(data, list): # if data is also a list, we will read it
			return set([load_obj(item, next(iter(class_type))) for item in data])
		else: #if data is not a list, we just create one instance from it
			return set([load_obj(data, next(iter(class_type)))])

	# if it's a dictionary, we will use data as is
	elif isinstance(class_type, dict):
		if data or strict:
			assert isinstance(data, dict), 'data for dictionary field also must be dictionary'
			return data
		else:
			return make_instance(class_type)

	# in other cases we create an instance of class_type and iterate over its fields
	else:
		obj = class_type() if callable(class_type) else class_type
		for k, v in get_orm_fields(obj).items():
			if strict:
				assert data.get(k), "can't find value for key %s" % k
			setattr(obj, k, load_obj(data.get(k) if data else None, v))
		return obj

# dumps objects to dictionary
def dump_obj(obj):
	if is_basic_field(obj):
		return obj
	elif isinstance(obj, list) or isinstance(obj, set):
		return [dump_obj(item) for item in obj]
	elif isinstance(obj, dict):
		return {k: dump_obj(v) for k, v in obj.items()}
	else:
		d = {}
		for k, v in get_orm_fields(obj).items():
			d[k] = dump_obj(v)
		return d

import yaml

def load(yaml_string, class_type, strict = True): # loads yaml string
	return {k: load_obj(v, class_type, strict) for k, v in yaml.load(yaml_string).items()}

def dump(objs): # dumps yaml string
	return yaml.dump({k: dump_obj(v) for k, v in objs.items()})

def loadf(yaml_filename, class_type, strict = True): # loads yaml file
	with open(yaml_filename, 'r') as f:
		return load(f.read(), class_type, strict)

def dumpf(yaml_filename, objs): # dumps yaml file
	with open(yaml_filename, 'w') as f:
		f.write(dump(objs))
