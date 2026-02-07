class ReviewValidator
  MIN_TITLE_LENGTH = 3
  MAX_TITLE_LENGTH = 200
  MIN_BODY_LENGTH = 10
  MAX_BODY_LENGTH = 5000
  VALID_RATINGS = (1..5).to_a

  def validate_create!(attrs)
    errors = []

    errors << "Product ID is required" if blank?(attrs[:product_id])
    errors << "User ID is required" if blank?(attrs[:user_id])
    errors << "Rating is required" if attrs[:rating].nil?

    if attrs[:rating] && !VALID_RATINGS.include?(attrs[:rating])
      errors << "Rating must be between 1 and 5"
    end

    if attrs[:title]
      if attrs[:title].length < MIN_TITLE_LENGTH
        errors << "Title must be at least #{MIN_TITLE_LENGTH} characters"
      end
      if attrs[:title].length > MAX_TITLE_LENGTH
        errors << "Title must be at most #{MAX_TITLE_LENGTH} characters"
      end
    end

    if attrs[:body]
      if attrs[:body].length < MIN_BODY_LENGTH
        errors << "Body must be at least #{MIN_BODY_LENGTH} characters"
      end
      if attrs[:body].length > MAX_BODY_LENGTH
        errors << "Body must be at most #{MAX_BODY_LENGTH} characters"
      end
    end

    raise errors.join("; ") unless errors.empty?
  end

  private

  def blank?(value)
    value.nil? || (value.is_a?(String) && value.strip.empty?)
  end
end

