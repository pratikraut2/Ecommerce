import { useState, useRef } from 'react';
import { Search, X } from 'lucide-react';

export default function SearchBar({ onSearch, placeholder = "Search products..." }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [isFocused, setIsFocused] = useState(false);
  const inputRef = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (searchTerm.trim()) {
      onSearch(searchTerm.trim());
      console.log('Search triggered:', searchTerm); // todo: remove mock functionality
    }
  };

  const handleChange = (e) => {
    setSearchTerm(e.target.value);
  };

  const handleClear = () => {
    setSearchTerm('');
    inputRef.current?.focus();
  };

  const handleFocus = () => {
    setIsFocused(true);
  };

  const handleBlur = () => {
    setIsFocused(false);
  };

  return (
    <form onSubmit={handleSubmit} className="relative w-full max-w-md">
      <div className={`relative group transition-all duration-200 ${
        isFocused ? 'scale-[1.02]' : ''
      }`}>
        {/* Search Icon */}
        <Search className={`absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 transition-colors duration-200 ${
          isFocused ? 'text-blue-600' : 'text-gray-400'
        }`} />
        
        {/* Input Field */}
        <input
          ref={inputRef}
          type="search"
          placeholder={placeholder}
          value={searchTerm}
          onChange={handleChange}
          onFocus={handleFocus}
          onBlur={handleBlur}
          className={`w-full pl-10 pr-12 py-2.5 border rounded-lg bg-white/50 backdrop-blur-sm text-gray-900 placeholder:text-gray-400 transition-all duration-200 focus:outline-none ${
            isFocused 
              ? 'border-blue-500/50 bg-white/80 shadow-lg shadow-blue-500/10 ring-2 ring-blue-500/20' 
              : 'border-gray-300 hover:border-gray-400 hover:bg-white/70'
          }`}
          data-testid="input-search"
        />

        {/* Clear Button */}
        {searchTerm && (
          <button
            type="button"
            onClick={handleClear}
            className="absolute right-1 top-1/2 transform -translate-y-1/2 h-8 w-8 p-1 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-md transition-all duration-200"
            data-testid="button-clear-search"
          >
            <X className="h-3 w-3" />
          </button>
        )}

        {/* Enhanced Focus Ring */}
        <div className={`absolute inset-0 rounded-lg bg-gradient-to-r from-blue-500/10 to-purple-500/10 opacity-0 pointer-events-none transition-opacity duration-200 ${
          isFocused ? 'opacity-100' : ''
        }`}></div>
      </div>

      {/* Search Suggestions (placeholder for future enhancement) */}
      {isFocused && searchTerm && (
        <div className="absolute top-full left-0 right-0 mt-2 bg-white/95 backdrop-blur-sm border border-gray-300 rounded-lg shadow-lg z-50">
          <div className="p-3 text-sm text-gray-600">
            Press Enter to search for "{searchTerm}"
          </div>
        </div>
      )}
    </form>
  );
}