require 'securerandom'

class Review
  attr_accessor :id, :product_id, :user_id, :title, :body, :rating,
                :is_verified_purchase, :is_approved, :helpful_count,
                :not_helpful_count, :created_at, :updated_at

  def initialize(attrs = {})
    @id = attrs[:id] || SecureRandom.uuid
    @product_id = attrs[:product_id]
    @user_id = attrs[:user_id]
    @title = attrs[:title]
    @body = attrs[:body]
    @rating = attrs[:rating]
    @is_verified_purchase = attrs[:is_verified_purchase] || false
    @is_approved = attrs[:is_approved] || false
    @helpful_count = attrs[:helpful_count] || 0
    @not_helpful_count = attrs[:not_helpful_count] || 0
    @created_at = attrs[:created_at] || Time.now
    @updated_at = attrs[:updated_at] || Time.now
  end

  def helpfulness_score
    total = @helpful_count + @not_helpful_count
    return 0.0 if total == 0
    (@helpful_count.to_f / total * 100).round(2)
  end

  def to_hash
    {
      id: @id,
      product_id: @product_id,
      user_id: @user_id,
      title: @title,
      body: @body,
      rating: @rating,
      is_verified_purchase: @is_verified_purchase,
      is_approved: @is_approved,
      helpful_count: @helpful_count,
      not_helpful_count: @not_helpful_count,
      helpfulness_score: helpfulness_score,
      created_at: @created_at.iso8601,
      updated_at: @updated_at.iso8601
    }
  end
end

