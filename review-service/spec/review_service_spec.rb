require_relative 'spec_helper'

RSpec.describe ReviewService do
  let(:service) { ReviewService.new }
  let(:valid_attrs) do
    {
      product_id: 'prod-1',
      user_id: 'user-1',
      title: 'Great Product',
      body: 'This product is amazing and I love it very much!',
      rating: 5,
      is_verified_purchase: true
    }
  end

  describe '#create_review' do
    it 'creates a review successfully' do
      review = service.create_review(valid_attrs)
      expect(review.product_id).to eq('prod-1')
      expect(review.rating).to eq(5)
      expect(review.is_approved).to be false
    end

    it 'rejects missing product_id' do
      attrs = valid_attrs.merge(product_id: nil)
      expect { service.create_review(attrs) }.to raise_error(/Product ID/)
    end

    it 'rejects invalid rating' do
      attrs = valid_attrs.merge(rating: 6)
      expect { service.create_review(attrs) }.to raise_error(/between 1 and 5/)
    end

    it 'rejects short title' do
      attrs = valid_attrs.merge(title: 'AB')
      expect { service.create_review(attrs) }.to raise_error(/at least/)
    end

    it 'rejects short body' do
      attrs = valid_attrs.merge(body: 'Short')
      expect { service.create_review(attrs) }.to raise_error(/at least/)
    end

    it 'rejects duplicate review for same product by same user' do
      service.create_review(valid_attrs)
      expect { service.create_review(valid_attrs) }.to raise_error(/already reviewed/)
    end

    it 'rejects profanity in title' do
      attrs = valid_attrs.merge(title: 'This is spam content', user_id: 'user-2')
      expect { service.create_review(attrs) }.to raise_error(/prohibited/)
    end
  end

  describe '#get_review' do
    it 'returns review by id' do
      review = service.create_review(valid_attrs)
      found = service.get_review(review.id)
      expect(found).to_not be_nil
      expect(found.id).to eq(review.id)
    end

    it 'returns nil for nonexistent id' do
      expect(service.get_review('nonexistent')).to be_nil
    end
  end

  describe '#get_reviews_for_product' do
    it 'returns approved reviews only by default' do
      review = service.create_review(valid_attrs)
      review.is_approved = true
      unapproved = service.create_review(valid_attrs.merge(user_id: 'user-2'))

      reviews = service.get_reviews_for_product('prod-1')
      expect(reviews.length).to eq(1)
    end

    it 'returns all reviews when approved_only is false' do
      service.create_review(valid_attrs)
      service.create_review(valid_attrs.merge(user_id: 'user-2'))

      reviews = service.get_reviews_for_product('prod-1', approved_only: false)
      expect(reviews.length).to eq(2)
    end
  end

  describe '#update_review' do
    it 'updates review title and body' do
      review = service.create_review(valid_attrs)
      review.is_approved = true

      updated = service.update_review(review.id, { title: 'Updated Title' })
      expect(updated.title).to eq('Updated Title')
      expect(updated.is_approved).to be false # Re-approval needed
    end

    it 'returns nil for nonexistent review' do
      expect(service.update_review('nonexistent', { title: 'Test' })).to be_nil
    end
  end

  describe '#delete_review' do
    it 'deletes existing review' do
      review = service.create_review(valid_attrs)
      expect(service.delete_review(review.id)).to be true
      expect(service.get_review(review.id)).to be_nil
    end

    it 'returns false for nonexistent review' do
      expect(service.delete_review('nonexistent')).to be false
    end
  end

  describe '#vote_helpful' do
    it 'increments helpful count' do
      review = service.create_review(valid_attrs)
      service.vote_helpful(review.id, 'voter-1')
      expect(review.helpful_count).to eq(1)
    end
  end

  describe '#vote_not_helpful' do
    it 'increments not helpful count' do
      review = service.create_review(valid_attrs)
      service.vote_not_helpful(review.id, 'voter-1')
      expect(review.not_helpful_count).to eq(1)
    end
  end
end

