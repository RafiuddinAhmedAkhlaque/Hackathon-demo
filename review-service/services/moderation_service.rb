require_relative '../models/moderation_log'

class ModerationService
  def initialize(review_service)
    @review_service = review_service
    @logs = []
  end

  def approve_review(review_id, moderator_id, reason: '')
    review = @review_service.get_review(review_id)
    raise "Review not found" unless review

    review.is_approved = true
    review.updated_at = Time.now

    log = ModerationLog.new(
      review_id: review_id,
      action: 'approve',
      reason: reason,
      moderator_id: moderator_id
    )
    @logs << log
    review
  end

  def reject_review(review_id, moderator_id, reason:)
    review = @review_service.get_review(review_id)
    raise "Review not found" unless review

    review.is_approved = false
    review.updated_at = Time.now

    log = ModerationLog.new(
      review_id: review_id,
      action: 'reject',
      reason: reason,
      moderator_id: moderator_id
    )
    @logs << log
    review
  end

  def flag_review(review_id, moderator_id, reason:)
    review = @review_service.get_review(review_id)
    raise "Review not found" unless review

    log = ModerationLog.new(
      review_id: review_id,
      action: 'flag',
      reason: reason,
      moderator_id: moderator_id
    )
    @logs << log
    log
  end

  def remove_review(review_id, moderator_id, reason:)
    review = @review_service.get_review(review_id)
    raise "Review not found" unless review

    log = ModerationLog.new(
      review_id: review_id,
      action: 'remove',
      reason: reason,
      moderator_id: moderator_id
    )
    @logs << log

    @review_service.delete_review(review_id)
    log
  end

  def get_moderation_logs(review_id: nil)
    return @logs unless review_id
    @logs.select { |l| l.review_id == review_id }
  end

  def get_pending_count
    @review_service.get_pending_reviews.length
  end

  def get_stats
    {
      total_actions: @logs.length,
      approved: @logs.count { |l| l.action == 'approve' },
      rejected: @logs.count { |l| l.action == 'reject' },
      flagged: @logs.count { |l| l.action == 'flag' },
      removed: @logs.count { |l| l.action == 'remove' },
      pending: get_pending_count
    }
  end
end

