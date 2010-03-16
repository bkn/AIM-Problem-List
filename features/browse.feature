@reset_db
@push_list
@push_app
Feature: Browse problem lists
  In order to use the site
  all vistors 
  should be allowed to browse lists, sections and problems

Scenario: user browses braid
   When I go to the index page
   And I follow "Braid Groups, Clusters, and Free Probability"
   And I follow "Reflection Groups"
   Then I should see "Clusters, and Free"
   Then I should see "topology of this poset"
   Then I should see "finite Coxeter group"
  
  Scenario: user browses freeanalysis
     When I go to the index page
     And I follow "Free Analysis"
     And I follow "Invariant Subspaces"
     Then I should see "Taylor spectrum"
     Then I should see "focus group"
     Then I should see "quasinilpotent operator may be"
     Then I should see "Free Analysis"
  #   And I follow "1"
  #   Then I should see "Taylor spectrum"

