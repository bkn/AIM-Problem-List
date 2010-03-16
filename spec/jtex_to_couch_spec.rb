require File.expand_path("../spec_helper", __FILE__)

describe JTexToCouch do
  before(:all) do
    DB.recreate!
    @fixture_path = File.expand_path("../../examples/", __FILE__)
    @tex = TexToJSON.new(open(@fixture_path + "/freeanalysisPL.tex").read)
    @json = JSON.parse(@tex.parse_aimpl.to_json)
    @ttc = JTexToCouch.new(@json)
  end
  describe "a problem list" do
    before(:all) do
      pl = @ttc.create_list!(:publish)
      pl['id'].should_not be_nil
      @l = DB.get(pl['id'])
      @l.id.should == pl["id"]
      @id = @l.id
      @title = @l["title"]
      DB.delete_doc(@l)
    end
    it "should have the same value for id and title" do
      @id.should == @title.downcase.gsub(/ /, "-")
    end
    it "should have a type" do
      @l["type"].should == "list"
    end
    it "should have a title" do
      @l["title"].should == "Free Analysis"
    end
    it "should have an intro" do
      @l["intro"].should_not be_nil
      @l["intro"].should include("organized by Dimitri")
    end
    it "should link to sections" do
      @l["section_ids"].length.should == @json["sections"].length
    end
    describe "section docs" do
      before(:all) do
        @sec = DB.get(@l["section_ids"][0])
        @sec2 = DB.get(@l["section_ids"][2])
        @sec3 = DB.get(@l["section_ids"][3])
        @sec["_id"].should == @l["section_ids"][0]
      end
      it "should have a type" do
        @sec["type"].should == "section"
      end
      it "should have the pl title" do
        @sec["pl_title"].should_not be_nil
        @sec["pl_title"].should == "Free Analysis"
      end
      it "should have a title" do
        @sec["title"].should_not be_nil
        @sec["title"].should include("constants and free")
      end
      it "should have a author" do
        @sec["author"].should_not be_nil
        @sec["author"].should == "Voiculescu"
      end
      it "should have an intro" do
        @sec3["intro"].should_not be_nil
        @sec3["intro"].should include("3rd day of the AIM workshop")
      end
      it "lists should link to section docs" do
        @sec["_id"].should == @l["section_ids"][0]
      end
      it "should link to list with position" do
        @sec["list_id"].should == @l.id
        @sec["list_pos"].should == 1
      end
      it "should link to pb docs" do
        @sec["pblock_ids"].should_not be_nil
        @sec["pblock_ids"].length.should == @json["sections"][0]["problemblocks"].length
      end
      describe "pb docs" do
        before(:all) do
          @pb = DB.get(@sec["pblock_ids"][0])
          @pb.id.should == @sec["pblock_ids"][0]
          @pb2 = DB.get(@sec2["pblock_ids"][2])
        end
        it "should have a type" do
          @pb["type"].should == "pblock"
        end
        it "should have a link to the section" do
          @pb["section_id"].should == @sec.id
        end
        it "should have a sec_pos" do
          @pb["sec_pos"].should == 0
        end
        it "should have a link to the list" do
          @pb["list_id"].should == @l["_id"]
        end
        it "should have remarks" do
          @pb["remarks"].should_not be_nil
          @pb2["remarks"].should_not be_nil
          @pb2["remarks"][0]["remark"].should include("free entropy")
        end
        it "should have the problem" do
          @pb["problem"].should_not be_nil
        end
      end
    end
  end
end