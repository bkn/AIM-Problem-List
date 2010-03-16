require File.expand_path("../spec_helper", __FILE__)

describe TexToJSON do
  before(:all) do
    @fixture_path = File.expand_path("../../examples/", __FILE__)
  end
  it "should accept a filename" do
    TexToJSON.new(@fixture_path + "/freeanalysisPL.tex")
  end

  # describe "parsing the loweigenvaluesPL.tex aimpl tex file" do
  #   before(:all) do
  #     @tex = TexToJSON.new(open(@fixture_path + "/loweigenvaluesPL.tex").read)
  #     @parsed = @tex.parse_aimpl
  #   end
  #   it "should have a title" do
  #     @parsed[:title].should == "Low Eigenvalues of Laplace and Schr\\\"\{o\}dinger Operator"
  #   end
  #   it "should have an intro" do
  #     @parsed[:intro].should include("MFO Oberwolfach,")
  #   end
  #   it "should have sections" do
  #     @parsed[:sections].length.should == 3
  #     @parsed[:sections][0][:title].should include("Related Inequalities")
  #     # @parsed[:sections][0][:title].should_not include("Inequalities")
  #     # @parsed[:sections][0][:author].should empty?
  #     # @parsed[:sections][1][:intro].should include("Inequalities")
  #   end
  # end

  describe "parsing the braidPL.tex aimpl tex file" do
    before(:all) do
      @tex = TexToJSON.new(open(@fixture_path + "/braidPL.tex").read)
      @parsed = @tex.parse_aimpl
    end
    it "should have a title" do
      @parsed[:title].should == "Braid Groups, Clusters, and Free Probability"
    end
    it "should have sections" do
      @parsed[:sections].length.should == 6
    end
    describe "reflection groups" do
      before(:each) do
        @rf = @parsed[:sections][2]
      end
      it "should have problems" do
        @rf[:problemblocks].length.should == 5
        @rf[:problemblocks][2][:intro].
          should include("This number is known to count many things, including labelled trees, and cacti.")
      end
      it "problems should have attribution" do
        pb = @rf[:problemblocks][0][:problems][0]
        pb[:body].should include("topology of this poset")
        pb[:by].should == "V. Reiner"
      end  
    end
  end
  
  describe "parsing the freeanalysisPL.tex aimpl tex file" do
    before(:all) do
      @tex = TexToJSON.new(open(@fixture_path + "/freeanalysisPL.tex").read)
      @parsed = @tex.parse_aimpl
    end
    it "should have a title" do
      @parsed[:title].should == "Free Analysis"
    end
    it "should have an intro" do
      @parsed[:intro].should include("Dan Voiculescu")
    end
    it "should have sections" do
      @parsed[:sections].length.should == 11
      @parsed[:sections][0][:title].should include('Poincare inequality')
      @parsed[:sections][0][:title].should_not include('Voiculescu')
      @parsed[:sections][0][:author].should include('Voiculescu')
      @parsed[:sections][3][:intro].should include('3rd day')
      @parsed[:sections][3][:intro].should_not include('begin')
    end
    it "should have problemblocks within sections" do
      @parsed[:sections][0][:problemblocks].length.should == 2
      @parsed[:sections][0][:problemblocks][0][:intro].should include("infinite-dimensional von Neumann subalgebra")
      @parsed[:sections][6][:problemblocks][0][:intro].should include("weak containment")
    end
    it "should have problems within problemblocks" do
      @parsed[:sections][0][:problemblocks][0][:problems][0].should_not be_nil
      @parsed[:sections][0][:problemblocks][0][:problems][0][:body].should include("Under what conditions")
    end
    it "should work on problems without enclosing problemblocks" do
      # this will work by upgrading them to simple problem blocks
      @parsed[:sections][2][:problemblocks].length.should == 9
      @parsed[:sections][2][:problemblocks][0][:problems][0].should_not be_nil
      @parsed[:sections][2][:problemblocks][0][:problems][0].should include("common diffuse")
    end
    it "should get comments inside the block too" do
      @parsed[:sections][2][:problemblocks][2][:comments].length.should == 1
      @parsed[:sections][2][:problemblocks][2][:comments][0][:remark].should_not be_nil
    end
  end
end
