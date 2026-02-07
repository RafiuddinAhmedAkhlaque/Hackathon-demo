class ProfanityFilter
  # Simplified list for demonstration
  BANNED_WORDS = %w[
    spam scam fake
  ].freeze

  def check!(text)
    return if text.nil? || text.empty?

    words = text.downcase.split(/\s+/)
    found = words.select { |w| BANNED_WORDS.include?(w) }

    unless found.empty?
      raise "Content contains prohibited words: #{found.join(', ')}"
    end
  end

  def clean(text)
    return text if text.nil? || text.empty?

    result = text
    BANNED_WORDS.each do |word|
      result = result.gsub(/\b#{Regexp.escape(word)}\b/i, '*' * word.length)
    end
    result
  end

  def contains_profanity?(text)
    return false if text.nil? || text.empty?
    words = text.downcase.split(/\s+/)
    words.any? { |w| BANNED_WORDS.include?(w) }
  end
end

