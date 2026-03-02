import { useState, useRef, useEffect } from 'react'
import { Search, MapPin, Loader2, X } from 'lucide-react'

export default function AddressSearch({ onSearch, onClear, isLoading, hasResults }) {
  const [query, setQuery] = useState('')
  const inputRef = useRef(null)
  const autocompleteRef = useRef(null)

  // Attach Google Maps Autocomplete widget to the input
  useEffect(() => {
    const initAutocomplete = () => {
      if (!inputRef.current || !window.google?.maps?.places?.Autocomplete) return
      if (autocompleteRef.current) return

      const ac = new window.google.maps.places.Autocomplete(inputRef.current, {
        componentRestrictions: { country: 'us' },
        types: ['address'],
        fields: ['formatted_address'],
      })

      ac.addListener('place_changed', () => {
        const place = ac.getPlace()
        if (place?.formatted_address) {
          setQuery(place.formatted_address)
          onSearch(place.formatted_address)
        }
      })

      autocompleteRef.current = ac
    }

    initAutocomplete()
    const t1 = setTimeout(initAutocomplete, 2000)
    const t2 = setTimeout(initAutocomplete, 5000)
    return () => { clearTimeout(t1); clearTimeout(t2) }
  }, [onSearch])

  const handleClear = () => {
    setQuery('')
    // Detach and re-create autocomplete on next render
    autocompleteRef.current = null
    onClear?.()
    inputRef.current?.focus()
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (query.trim()) {
      onSearch(query.trim())
    }
  }

  return (
    <div className="relative w-full">
      <form onSubmit={handleSubmit} className="relative">
        <div className="relative">
          <MapPin className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-text-secondary z-10" />
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter any U.S. address..."
            className={`w-full pl-10 ${hasResults ? 'pr-20' : 'pr-12'} py-3 bg-bg-tertiary/50 border border-white/10 rounded-lg text-text-primary placeholder-text-secondary focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent/50 transition-all`}
            disabled={isLoading}
          />
          <div className="absolute right-2 top-1/2 -translate-y-1/2 flex items-center gap-1 z-10">
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
    </div>
  )
}
