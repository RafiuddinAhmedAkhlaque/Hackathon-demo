require 'sinatra/base'

module ModerationRoutes
  def self.registered(app)
    app.get '/moderation/pending' do
      content_type :json
      { reviews: [], message: 'Pending reviews' }.to_json
    end

    app.post '/moderation/:review_id/approve' do
      content_type :json
      { review_id: params[:review_id], action: 'approved' }.to_json
    end

    app.post '/moderation/:review_id/reject' do
      content_type :json
      { review_id: params[:review_id], action: 'rejected' }.to_json
    end
  end
end

