module CouchappHelpers
  def push_couchapp dbname
    ddoc_path = File.expand_path("../../../couchapp/aimpl", __FILE__)
    push = "cd #{ddoc_path} && couchapp push . #{dbname}"
    puts "pushing couchapp"
    puts push
    system push
  end
end

World(CouchappHelpers)