require 'sinatra/base'

module RatingRoutes
  def self.registered(app)
    app.get '/products/:product_id/ratings' do
      content_type :json
      { product_id: params[:product_id], message: 'Product ratings' }.to_json
    end
  end
end

