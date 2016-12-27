
# small yaml orm-like contraption

# TODO support list, dictionaries, tuples in fields

import yaml

def get_orm_fields(class_or_instance):
	return {k: getattr(class_or_instance, k) for k in dir(class_or_instance) if not k.startswith('__')}

#def repr_orm_fields(class_or_instance):
#	return ";".join(["%s=%s" % (str(k), repr(v)) for k, v in get_orm_fields(class_or_instance).items()])

def is_basic_field(obj):
	return isinstance(obj, str) or isinstance(obj, int) or isinstance(obj, float)

def load_obj(data, class_type):
	if is_basic_field(class_type):
		return data if data else class_type
	obj = class_type()
	for k, v in get_orm_fields(obj).items():
		setattr(obj, k, load_obj(data.get(k) if data else None, v))
	return obj

def dump_obj(obj):
	if is_basic_field(obj):
		return obj
	d = {}
	for k, v in get_orm_fields(obj).items():
		d[k] = dump_obj(v)
	return d

def load(yaml_string, class_type):
	return {k: load_obj(v, class_type) for k, v in yaml.load(yaml_string).items()}

def dump(objs):
	return yaml.dump({k: dump_obj(v) for k, v in objs.items()})
