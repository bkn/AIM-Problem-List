module NavigationHelpers
  
  def list_url db, ddoc, list, view, params = {}
    CouchRest.paramify_url "#{db.root}/_design/#{ddoc}/_list/#{view}/#{list}", params
  end
  
  def path_to(page_name)
    case page_name
    
    when /the index page/i
      APP_ROOT + "_list/index/pls"
    when /the section page for a list/i
      new_user_path
    when /the sign in page/i
      new_session_path
    when /the password reset request page/i
      new_password_path
    when /the account page/i
      account_path
    # Add more page name => path mappings here
    
    else
      raise "Can't find mapping from \"#{page_name}\" to a path."
    end
  end
end
 
World(NavigationHelpers)