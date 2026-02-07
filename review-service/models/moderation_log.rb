require 'securerandom'

class ModerationLog
  attr_reader :id, :review_id, :action, :reason, :moderator_id, :created_at

  VALID_ACTIONS = %w[approve reject flag remove].freeze

  def initialize(attrs = {})
    @id = attrs[:id] || SecureRandom.uuid
    @review_id = attrs[:review_id]
    @action = attrs[:action]
    @reason = attrs[:reason] || ''
    @moderator_id = attrs[:moderator_id]
    @created_at = attrs[:created_at] || Time.now

    validate!
  end

  def to_hash
    {
      id: @id,
      review_id: @review_id,
      action: @action,
      reason: @reason,
      moderator_id: @moderator_id,
      created_at: @created_at.iso8601
    }
  end

  private

  def validate!
    raise ArgumentError, "Review ID is required" if @review_id.nil? || @review_id.empty?
    raise ArgumentError, "Action is required" if @action.nil? || @action.empty?
    unless VALID_ACTIONS.include?(@action)
      raise ArgumentError, "Invalid action: #{@action}. Must be one of: #{VALID_ACTIONS.join(', ')}"
    end
    raise ArgumentError, "Moderator ID is required" if @moderator_id.nil? || @moderator_id.empty?
  end
end

