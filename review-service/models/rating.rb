class RatingSummary
  attr_reader :product_id, :average_rating, :total_reviews,
              :rating_distribution, :verified_purchase_count

  def initialize(product_id:, reviews: [])
    @product_id = product_id
    @reviews = reviews
    calculate_summary
  end

  def to_hash
    {
      product_id: @product_id,
      average_rating: @average_rating,
      total_reviews: @total_reviews,
      verified_purchase_count: @verified_purchase_count,
      rating_distribution: @rating_distribution
    }
  end

  private

  def calculate_summary
    @total_reviews = @reviews.length
    @verified_purchase_count = @reviews.count(&:is_verified_purchase)

    if @total_reviews == 0
      @average_rating = 0.0
      @rating_distribution = { 1 => 0, 2 => 0, 3 => 0, 4 => 0, 5 => 0 }
      return
    end

    total = @reviews.sum(&:rating)
    @average_rating = (total.to_f / @total_reviews).round(2)

    @rating_distribution = { 1 => 0, 2 => 0, 3 => 0, 4 => 0, 5 => 0 }
    @reviews.each do |review|
      @rating_distribution[review.rating] += 1
    end
  end
end

