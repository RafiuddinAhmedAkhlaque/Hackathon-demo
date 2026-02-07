require_relative '../models/rating'

class RatingService
  def initialize(review_service)
    @review_service = review_service
  end

  def get_product_rating(product_id)
    reviews = @review_service.get_reviews_for_product(product_id, approved_only: true)
    RatingSummary.new(product_id: product_id, reviews: reviews)
  end

  def get_average_rating(product_id)
    summary = get_product_rating(product_id)
    summary.average_rating
  end

  def get_rating_distribution(product_id)
    summary = get_product_rating(product_id)
    summary.rating_distribution
  end

  def compare_products(product_ids)
    product_ids.map do |pid|
      summary = get_product_rating(pid)
      {
        product_id: pid,
        average_rating: summary.average_rating,
        total_reviews: summary.total_reviews
      }
    end.sort_by { |p| -p[:average_rating] }
  end

  def get_top_rated_products(product_ids, min_reviews: 1, limit: 10)
    ratings = product_ids.map do |pid|
      summary = get_product_rating(pid)
      { product_id: pid, average_rating: summary.average_rating, total_reviews: summary.total_reviews }
    end

    ratings
      .select { |r| r[:total_reviews] >= min_reviews }
      .sort_by { |r| -r[:average_rating] }
      .first(limit)
  end
end

