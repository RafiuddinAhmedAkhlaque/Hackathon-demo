require_relative '../models/review'
require_relative '../validators/review_validator'
require_relative '../validators/profanity_filter'

class ReviewService
  def initialize
    @reviews = {}
    @product_index = Hash.new { |h, k| h[k] = [] }
    @user_index = Hash.new { |h, k| h[k] = [] }
    @validator = ReviewValidator.new
    @profanity_filter = ProfanityFilter.new
  end

  def create_review(attrs)
    @validator.validate_create!(attrs)
    @profanity_filter.check!(attrs[:title]) if attrs[:title]
    @profanity_filter.check!(attrs[:body]) if attrs[:body]

    # Check for duplicate review
    existing = @user_index[attrs[:user_id]].find do |id|
      @reviews[id]&.product_id == attrs[:product_id]
    end
    raise "User has already reviewed this product" if existing

    review = Review.new(attrs)
    @reviews[review.id] = review
    @product_index[review.product_id] << review.id
    @user_index[review.user_id] << review.id
    review
  end

  def get_review(id)
    @reviews[id]
  end

  def get_reviews_for_product(product_id, approved_only: true)
    ids = @product_index[product_id]
    reviews = ids.map { |id| @reviews[id] }.compact
    reviews = reviews.select(&:is_approved) if approved_only
    reviews.sort_by { |r| -r.created_at.to_f }
  end

  def get_reviews_by_user(user_id)
    ids = @user_index[user_id]
    ids.map { |id| @reviews[id] }.compact
  end

  def update_review(id, attrs)
    review = @reviews[id]
    return nil unless review

    @profanity_filter.check!(attrs[:title]) if attrs[:title]
    @profanity_filter.check!(attrs[:body]) if attrs[:body]

    review.title = attrs[:title] if attrs.key?(:title)
    review.body = attrs[:body] if attrs.key?(:body)
    review.rating = attrs[:rating] if attrs.key?(:rating)
    review.is_approved = false # Re-approval needed after edit
    review.updated_at = Time.now
    review
  end

  def delete_review(id)
    review = @reviews.delete(id)
    return false unless review

    @product_index[review.product_id].delete(id)
    @user_index[review.user_id].delete(id)
    true
  end

  def vote_helpful(review_id, user_id)
    review = @reviews[review_id]
    raise "Review not found" unless review
    review.helpful_count += 1
    review
  end

  def vote_not_helpful(review_id, user_id)
    review = @reviews[review_id]
    raise "Review not found" unless review
    review.not_helpful_count += 1
    review
  end

  def count
    @reviews.size
  end

  def get_pending_reviews
    @reviews.values.reject(&:is_approved)
  end
end

