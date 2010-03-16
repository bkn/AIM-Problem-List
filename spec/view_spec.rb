require File.expand_path("../spec_helper", __FILE__)

describe "views" do
  before(:all) do
    @fixture_path = File.expand_path("../../examples/", __FILE__)
    @tex = TexToJSON.new(open(@fixture_path + "/freeanalysisPL.tex").read)
    @json = JSON.parse(@tex.parse_aimpl.to_json)
    @ttc = JTexToCouch.new(@json)
    @pl = @ttc.create_list!
    sleep 1 # FIXME, _ensure_full_commit
    @l = DB.get(@pl["id"])
    ddoc_path = File.expand_path("../../src/aimpl", __FILE__)
    push = "cd #{ddoc_path} && ../../bin/couchapp push . #{DB.name}"
    system push
  end
  after(:all) do
    DB.delete_doc(@l)
  end
  describe "with a section range" do
    before(:all) do
      # section_id = @l["section_ids"][0];
      DB.view("aimpl/pl_full", :include_docs => true)["rows"].each do |r|
        puts r.inspect
      end
      @v = DB.view("aimpl/pl_full", :startkey => [@pl["id"]], :endkey => [@pl["id"], 2], :inclusive_end => false, :include_docs => true)
      @rs = @v["rows"]
    end
    it "should have rows" do
      (@rs.length > 0).should be_true
    end
    it "should have the problems" do
      puts @rs[1].inspect
      @rs[0]["doc"]["type"].should == "list"
      @rs[1]["doc"]["type"].should == "section"
      @rs[2]["doc"]["type"].should == "pblock"
    end
  end
  describe "with a list view" do
    before(:all) do
      @v = DB.view("aimpl/pl_full", :startkey => [@l.id], :endkey => [@l.id, {}], :include_docs => true)
      @rs = @v["rows"]
    end
    it "should have rows" do
      (@rs.length > 0).should be_true
    end
    it "should show up in proper order" do
      # @rs[0]["value"]["_id"].should == @l.id
      # @rs[1]["value"]["_id"].should == @l["section_ids"][0]
      # sec = DB.get(@l["section_ids"][0])
      # @rs[2]["value"]["_id"].should == sec["pblock_ids"][0]
    end
    it "should include correct docs" do
      # @rs[0]["doc"]["_id"].should == @l.id
      # @rs[1]["doc"]["_id"].should == @l["section_ids"][0]
      # sec = DB.get(@l["section_ids"][0])
      # @rs[2]["doc"]["_id"].should == sec["pblock_ids"][0]
    end
  end
  
  it "should have the metadata"
  it "should list problems" do
    
  end
end
