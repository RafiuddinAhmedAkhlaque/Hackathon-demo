require 'sinatra/base'
require 'json'
require 'logger'
require 'time'
require_relative 'routes/review_routes'
require_relative 'routes/rating_routes'
require_relative 'routes/moderation_routes'

class ReviewApp < Sinatra::Base
  configure do
    set :show_exceptions, false
    set :logger, Logger.new(STDOUT)
  end

  # JSON logging middleware
  before do
    @start_time = Time.now
  end

  after do
    duration_ms = ((Time.now - @start_time) * 1000).round(2)
    
    log_data = {
      method: request.request_method,
      path: request.path_info,
      status: response.status,
      duration_ms: duration_ms,
      timestamp: Time.now.utc.iso8601
    }
    
    puts log_data.to_json
  end

  get '/health' do
    content_type :json
    { status: 'healthy', service: 'review-service' }.to_json
  end

  register ReviewRoutes
  register RatingRoutes
  register ModerationRoutes
end

