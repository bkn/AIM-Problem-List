require "rubygems"
require "spec" # Satisfies Autotest and anyone else not using the Rake tasks
require "couchrest"

DB = CouchRest.database!("aimpl-test")

require File.expand_path("../../lib/tex_to_json", __FILE__)
require File.expand_path("../../lib/jtex_to_couch", __FILE__)
