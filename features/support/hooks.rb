require File.expand_path("../../../lib/jtex_to_couch", __FILE__)

Before ('@reset_db') do
  CouchRest.database(DBNAME).recreate!
end

Before ('@push_app') do
  push_couchapp(DBURL)
end

Before('@push_list') do
  @fixture_path = File.expand_path("../../../examples/", __FILE__)

  filename = ["freeanalysisPL.tex", "loweigenvaluesPL.tex", "braidPL.tex"].each do |filename|
    @tex = TexToJSON.new(open(File.join(@fixture_path, filename)).read)
    @json = JSON.parse(@tex.parse_aimpl.to_json)
    @ttc = JTexToCouch.new(@json)
    pl = @ttc.create_list!    
  end

end