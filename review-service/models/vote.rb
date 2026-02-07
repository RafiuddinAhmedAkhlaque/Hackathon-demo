require 'securerandom'

class Vote
  attr_reader :id, :review_id, :user_id, :vote_type, :created_at

  VALID_TYPES = %w[helpful not_helpful].freeze

  def initialize(attrs = {})
    @id = attrs[:id] || SecureRandom.uuid
    @review_id = attrs[:review_id]
    @user_id = attrs[:user_id]
    @vote_type = attrs[:vote_type]
    @created_at = attrs[:created_at] || Time.now

    validate!
  end

  def helpful?
    @vote_type == 'helpful'
  end

  def to_hash
    {
      id: @id,
      review_id: @review_id,
      user_id: @user_id,
      vote_type: @vote_type,
      created_at: @created_at.iso8601
    }
  end

  private

  def validate!
    raise ArgumentError, "Review ID is required" if @review_id.nil? || @review_id.empty?
    raise ArgumentError, "User ID is required" if @user_id.nil? || @user_id.empty?
    unless VALID_TYPES.include?(@vote_type)
      raise ArgumentError, "Invalid vote type: #{@vote_type}"
    end
  end
end

