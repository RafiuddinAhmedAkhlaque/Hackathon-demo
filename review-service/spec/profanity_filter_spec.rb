require_relative 'spec_helper'

RSpec.describe ProfanityFilter do
  let(:filter) { ProfanityFilter.new }

  describe '#check!' do
    it 'allows clean text' do
      expect { filter.check!('This is a great product') }.not_to raise_error
    end

    it 'raises for text with banned words' do
      expect { filter.check!('This is spam content') }.to raise_error(/prohibited/)
    end

    it 'handles nil text' do
      expect { filter.check!(nil) }.not_to raise_error
    end

    it 'handles empty text' do
      expect { filter.check!('') }.not_to raise_error
    end
  end

  describe '#clean' do
    it 'replaces banned words with asterisks' do
      result = filter.clean('This is spam content')
      expect(result).to include('****')
      expect(result).not_to include('spam')
    end

    it 'returns clean text unchanged' do
      text = 'This is great'
      expect(filter.clean(text)).to eq(text)
    end
  end

  describe '#contains_profanity?' do
    it 'returns true for text with banned words' do
      expect(filter.contains_profanity?('This is fake review')).to be true
    end

    it 'returns false for clean text' do
      expect(filter.contains_profanity?('Great product')).to be false
    end

    it 'returns false for nil' do
      expect(filter.contains_profanity?(nil)).to be false
    end
  end
end

