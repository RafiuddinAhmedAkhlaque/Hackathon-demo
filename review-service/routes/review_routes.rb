require 'sinatra/base'

module ReviewRoutes
  def self.registered(app)
    app.get '/reviews' do
      content_type :json
      { reviews: [], message: 'Reviews listing' }.to_json
    end

    app.get '/reviews/:id' do
      content_type :json
      { id: params[:id], message: 'Review detail' }.to_json
    end

    app.post '/reviews' do
      content_type :json
      status 201
      { message: 'Review created' }.to_json
    end
  end
end

