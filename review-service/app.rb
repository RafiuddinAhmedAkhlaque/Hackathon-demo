require 'sinatra/base'
require 'json'
require_relative 'routes/review_routes'
require_relative 'routes/rating_routes'
require_relative 'routes/moderation_routes'

class ReviewApp < Sinatra::Base
  configure do
    set :show_exceptions, false
  end

  get '/health' do
    content_type :json
    { status: 'healthy', service: 'review-service' }.to_json
  end

  register ReviewRoutes
  register RatingRoutes
  register ModerationRoutes
end

