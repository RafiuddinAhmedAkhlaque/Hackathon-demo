require_relative 'spec_helper'

RSpec.describe RatingService do
  let(:review_service) { ReviewService.new }
  let(:rating_service) { RatingService.new(review_service) }

  def create_approved_review(attrs)
    review = review_service.create_review(attrs)
    review.is_approved = true
    review
  end

  describe '#get_product_rating' do
    it 'returns correct average for multiple reviews' do
      create_approved_review(product_id: 'p1', user_id: 'u1', title: 'Good stuff',
                             body: 'Really enjoyed this product', rating: 5)
      create_approved_review(product_id: 'p1', user_id: 'u2', title: 'Okay product',
                             body: 'It was decent but not great', rating: 3)

      summary = rating_service.get_product_rating('p1')
      expect(summary.average_rating).to eq(4.0)
      expect(summary.total_reviews).to eq(2)
    end

    it 'returns zero for products with no reviews' do
      summary = rating_service.get_product_rating('no-reviews')
      expect(summary.average_rating).to eq(0.0)
      expect(summary.total_reviews).to eq(0)
    end

    it 'shows correct rating distribution' do
      create_approved_review(product_id: 'p1', user_id: 'u1', title: 'Five stars',
                             body: 'Absolutely amazing product!', rating: 5)
      create_approved_review(product_id: 'p1', user_id: 'u2', title: 'Five stars too',
                             body: 'Also think this is amazing', rating: 5)
      create_approved_review(product_id: 'p1', user_id: 'u3', title: 'Three stars',
                             body: 'Average product nothing special', rating: 3)

      summary = rating_service.get_product_rating('p1')
      expect(summary.rating_distribution[5]).to eq(2)
      expect(summary.rating_distribution[3]).to eq(1)
      expect(summary.rating_distribution[1]).to eq(0)
    end
  end

  describe '#compare_products' do
    it 'returns products sorted by rating' do
      create_approved_review(product_id: 'p1', user_id: 'u1', title: 'Good product',
                             body: 'Pretty good I think so too', rating: 3)
      create_approved_review(product_id: 'p2', user_id: 'u1', title: 'Great product',
                             body: 'This was the best purchase ever', rating: 5)

      comparison = rating_service.compare_products(['p1', 'p2'])
      expect(comparison.first[:product_id]).to eq('p2')
    end
  end

  describe '#get_top_rated_products' do
    it 'filters by minimum reviews' do
      create_approved_review(product_id: 'p1', user_id: 'u1', title: 'Amazing wow!',
                             body: 'Really love this product very much', rating: 5)
      create_approved_review(product_id: 'p1', user_id: 'u2', title: 'Great stuff',
                             body: 'Another great review of this item', rating: 4)

      top = rating_service.get_top_rated_products(['p1'], min_reviews: 3)
      expect(top).to be_empty
    end
  end
end

