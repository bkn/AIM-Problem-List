# RSpec
require 'spec/expectations'

# Webrat
require 'webrat'

require 'test/unit/assertions'
World(Test::Unit::Assertions)

Webrat.configure do |config|
  config.mode = :mechanize
end

module Webrat
  # For extra debug info we monkeypatch this in
  module Locators  
    class Locator # :nodoc:
      def locate!
        locate || raise(NotFoundError.new(error_message))        
      rescue Webrat::NotFoundError => e
        filepath = '/tmp/webrat_debug.html'
        File.open(filepath, "w") do |file|
          file.puts @session.send(:response_body)
        end
        raise "#{e.message}\n#{@session.send(:response_body).gsub(/\n/, "\n  ")}\nURL: #{@session.current_url}\nResponse saved: #{filepath}"  
      end
    end
  end
end

World do
  session = Webrat::Session.new
  session.extend(Webrat::Methods)
  session.extend(Webrat::Matchers)
  session
end

require "couchrest"
if ENV["TARGET"] == "staging"
  DBHOST = "problemlist:riemann@couch.yinas.org"
  DBNAME = "aim"
else
  DBHOST = "127.0.0.1:5984"
  DBNAME = "aim-test"
end

DBURL = "http://#{DBHOST}/#{DBNAME}"
DB = CouchRest.database!(DBURL)
APP_ROOT = "#{DBURL}/_design/aimpl/"
