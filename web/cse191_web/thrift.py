import thriftpy
import os.path

thrift_file = os.path.join(os.path.dirname(__file__), "lang.thrift")
lang_thrift = thriftpy.load(thrift_file, module_name="lang_thrift")
