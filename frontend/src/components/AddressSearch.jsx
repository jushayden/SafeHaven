import { useState, useRef, useEffect, useCallback } from 'react'
import { Search, MapPin, Loader2, X } from 'lucide-react'

export default function AddressSearch({ onSearch, onClear, isLoading, hasResults }) {
  const [query, setQuery] = useState('')
  const [suggestions, setSuggestions] = useState([])
  const [showSuggestions, setShowSuggestions] = useState(false)
  const autocompleteService = useRef(null)
  const inputRef = useRef(null)
  const wrapperRef = useRef(null)

  useEffect(() => {
    const tryInit = () => {
      if (window.google?.maps?.places) {
        autocompleteService.current = new window.google.maps.places.AutocompleteService()
      }
    }
    tryInit()
    // Retry after a delay in case the Maps script loads after this component mounts
    const timer = setTimeout(tryInit, 2000)
    const timer2 = setTimeout(tryInit, 5000)
    return () => { clearTimeout(timer); clearTimeout(timer2) }
  }, [])

  useEffect(() => {
    function handleClickOutside(e) {
      if (wrapperRef.current && !wrapperRef.current.contains(e.target)) {
        setShowSuggestions(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const fetchSuggestions = useCallback((input) => {
    if (!autocompleteService.current || input.length < 3) {
      setSuggestions([])
      return
    }
    autocompleteService.current.getPlacePredictions(
      {
        input,
        componentRestrictions: { country: 'us' },
        types: ['address'],
      },
      (predictions, status) => {
        if (status === window.google.maps.places.PlacesServiceStatus.OK && predictions) {
          setSuggestions(predictions)
          setShowSuggestions(true)
        } else {
          setSuggestions([])
        }
      }
    )
  }, [])

  const handleInputChange = (e) => {
    const value = e.target.value
    setQuery(value)
    fetchSuggestions(value)
  }

  const handleSelect = (description) => {
    setQuery(description)
    setShowSuggestions(false)
    onSearch(description)
  }

  const handleClear = () => {
    setQuery('')
    setSuggestions([])
    setShowSuggestions(false)
    onClear?.()
    inputRef.current?.focus()
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (query.trim()) {
      setShowSuggestions(false)
      onSearch(query.trim())
    }
  }

  return (
    <div ref={wrapperRef} className="relative w-full">
      <form onSubmit={handleSubmit} className="relative">
        <div className="relative">
          <MapPin className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-text-secondary" />
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={handleInputChange}
            placeholder="Enter any U.S. address..."
            className={`w-full pl-10 ${hasResults ? 'pr-20' : 'pr-12'} py-3 bg-bg-tertiary/50 border border-white/10 rounded-lg text-text-primary placeholder-text-secondary focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent/50 transition-all`}
            disabled={isLoading}
          />
          <div className="absolute right-2 top-1/2 -translate-y-1/2 flex items-center gap-1">
            {hasResults && !isLoading && (
              <button
                type="button"
                onClick={handleClear}
                className="p-1.5 rounded-md hover:bg-white/10 transition-colors"
                title="Clear search"
              >
                <X className="w-4 h-4 text-text-secondary" />
              </button>
            )}
            <button
              type="submit"
              disabled={isLoading || !query.trim()}
              className="p-1.5 rounded-md bg-accent hover:bg-accent-hover disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
            >
              {isLoading ? (
                <Loader2 className="w-4 h-4 text-white animate-spin" />
              ) : (
                <Search className="w-4 h-4 text-white" />
              )}
            </button>
          </div>
        </div>
      </form>

      {showSuggestions && suggestions.length > 0 && (
        <div className="absolute top-full left-0 right-0 mt-1 bg-bg-secondary border border-white/10 rounded-lg shadow-2xl overflow-hidden z-50">
          {suggestions.map((s) => (
            <button
              key={s.place_id}
              onClick={() => handleSelect(s.description)}
              className="w-full px-4 py-3 text-left text-sm text-text-primary hover:bg-bg-tertiary/50 transition-colors flex items-center gap-2 border-b border-white/5 last:border-0"
            >
              <MapPin className="w-4 h-4 text-text-secondary shrink-0" />
              <span>{s.description}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
