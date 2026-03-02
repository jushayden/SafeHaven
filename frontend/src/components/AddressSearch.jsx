import { useState, useRef, useEffect, useCallback } from 'react'
import { Search, MapPin, Loader2, X } from 'lucide-react'

// Force-hide all Google autocomplete dropdowns
function dismissPac() {
  document.querySelectorAll('.pac-container').forEach((el) => {
    el.style.display = 'none'
  })
}

export default function AddressSearch({ onSearch, onClear, isLoading, hasResults }) {
  const [hasText, setHasText] = useState(false)
  const inputRef = useRef(null)
  const autocompleteRef = useRef(null)

  const triggerSearch = useCallback((address) => {
    if (address) {
      dismissPac()
      inputRef.current?.blur()
      onSearch(address)
    }
  }, [onSearch])

  // Attach Google Maps Autocomplete widget (uncontrolled input)
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
          setHasText(true)
          triggerSearch(place.formatted_address)
        }
      })

      autocompleteRef.current = ac
    }

    initAutocomplete()
    const t1 = setTimeout(initAutocomplete, 2000)
    const t2 = setTimeout(initAutocomplete, 5000)
    return () => { clearTimeout(t1); clearTimeout(t2) }
  }, [triggerSearch])

  // Handle Enter key directly — Google Autocomplete swallows Enter
  // when the dropdown is open, preventing form submit
  useEffect(() => {
    const input = inputRef.current
    if (!input) return

    const handleKeyDown = (e) => {
      if (e.key === 'Enter') {
        // If a pac-item is highlighted, let Google handle it (place_changed will fire)
        const highlighted = document.querySelector('.pac-item-selected')
        if (highlighted) return

        // Otherwise, submit with whatever text is in the input
        e.preventDefault()
        const val = input.value?.trim()
        if (val) triggerSearch(val)
      }
    }

    input.addEventListener('keydown', handleKeyDown)
    return () => input.removeEventListener('keydown', handleKeyDown)
  }, [triggerSearch])

  const handleClear = () => {
    if (inputRef.current) inputRef.current.value = ''
    setHasText(false)
    autocompleteRef.current = null
    dismissPac()
    onClear?.()
    inputRef.current?.focus()
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    const val = inputRef.current?.value?.trim()
    if (val) triggerSearch(val)
  }

  return (
    <div className="relative w-full">
      <form onSubmit={handleSubmit} className="relative">
        <div className="relative">
          <MapPin className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-text-secondary z-10" />
          <input
            ref={inputRef}
            type="text"
            onChange={(e) => setHasText(e.target.value.length > 0)}
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
              disabled={isLoading || !hasText}
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
