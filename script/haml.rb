require 'rubygems'
require 'active_support/core_ext/object/blank'
require 'haml'
require 'haml/filters/coffee'

template = ARGV.length > 0 ? File.read(ARGV.shift) : STDIN.read
haml_engine = Haml::Engine.new(template)
file = ARGV.length > 0 ? File.open(ARGV.shift, 'w') : STDOUT
file.write(haml_engine.render)
file.close