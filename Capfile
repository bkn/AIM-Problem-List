load 'deploy' if respond_to?(:namespace) # cap2 differentiator
default_run_options[:pty] = true
set :application, "aimpl"
set :repository,  "git@github.com:janl/aimpl.git"
set :scm, "git"
set :ssh_options, { :forward_agent => true }
set :use_sudo, false
set :domain, "couch.yinas.org"
set :user, "couchdb"
set :branch, "master"
set :deploy_via, :remote_cache

set :deploy_to, "/var/www/#{application}"

set :normalize_asset_timestamps, false
set :git_enable_submodules, true

role :app, domain

desc 'restart'
deploy.task :restart, :roles => :app do
  # do nothing
end
