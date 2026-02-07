require_relative 'spec_helper'

RSpec.describe ModerationService do
  let(:review_service) { ReviewService.new }
  let(:moderation_service) { ModerationService.new(review_service) }
  let(:review) do
    review_service.create_review(
      product_id: 'prod-1', user_id: 'user-1', title: 'Test Review',
      body: 'This is a test review body that is long enough', rating: 4
    )
  end

  describe '#approve_review' do
    it 'approves a review' do
      approved = moderation_service.approve_review(review.id, 'mod-1')
      expect(approved.is_approved).to be true
    end

    it 'creates a moderation log' do
      moderation_service.approve_review(review.id, 'mod-1')
      logs = moderation_service.get_moderation_logs(review_id: review.id)
      expect(logs.length).to eq(1)
      expect(logs.first.action).to eq('approve')
    end

    it 'raises for nonexistent review' do
      expect { moderation_service.approve_review('bad-id', 'mod-1') }.to raise_error(/not found/)
    end
  end

  describe '#reject_review' do
    it 'rejects a review with reason' do
      rejected = moderation_service.reject_review(review.id, 'mod-1', reason: 'Spam content')
      expect(rejected.is_approved).to be false
    end
  end

  describe '#flag_review' do
    it 'creates a flag log' do
      log = moderation_service.flag_review(review.id, 'mod-1', reason: 'Suspicious content')
      expect(log.action).to eq('flag')
    end
  end

  describe '#remove_review' do
    it 'removes a review and logs it' do
      moderation_service.remove_review(review.id, 'mod-1', reason: 'Violates policy')
      expect(review_service.get_review(review.id)).to be_nil
      expect(moderation_service.get_moderation_logs.length).to eq(1)
    end
  end

  describe '#get_stats' do
    it 'returns correct statistics' do
      r1 = review_service.create_review(
        product_id: 'p1', user_id: 'u1', title: 'Review One',
        body: 'First review that is long enough', rating: 5
      )
      r2 = review_service.create_review(
        product_id: 'p1', user_id: 'u2', title: 'Review Two',
        body: 'Second review that is long enough', rating: 3
      )
      moderation_service.approve_review(r1.id, 'mod-1')
      moderation_service.reject_review(r2.id, 'mod-1', reason: 'Low quality')

      stats = moderation_service.get_stats
      expect(stats[:approved]).to eq(1)
      expect(stats[:rejected]).to eq(1)
      expect(stats[:total_actions]).to eq(2)
    end
  end
end

