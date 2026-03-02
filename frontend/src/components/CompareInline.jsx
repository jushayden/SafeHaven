import { useState, useCallback, useRef, useEffect } from 'react'
import {
  ArrowLeftRight, X, Loader2, MapPin, Search,
  CloudLightning, Waves, Mountain, Flame, ShieldAlert, ChevronDown, ChevronUp,
} from 'lucide-react'
import { geocodeAddress, getRiskProfile } from '../services/api'

const RISK_TYPES = [
  { key: 'hurricane', label: 'Hurricane', Icon: CloudLightning },
  { key: 'flood', label: 'Flood', Icon: Waves },
  { key: 'earthquake', label: 'Earthquake', Icon: Mountain },
  { key: 'wildfire', label: 'Wildfire', Icon: Flame },
]

const SEVERITY_ORDER = { Low: 1, Moderate: 2, High: 3, Extreme: 4 }
const SEVERITY_COLORS = {
  Low: 'text-risk-low',
  Moderate: 'text-risk-moderate',
  High: 'text-risk-high',
  Extreme: 'text-risk-extreme',
}
const BAR_COLORS = {
  Low: 'bg-risk-low',
  Moderate: 'bg-risk-moderate',
  High: 'bg-risk-high',
  Extreme: 'bg-risk-extreme',
}
const OVERALL_BG = {
  Low: 'bg-risk-low/10 border-risk-low/30',
  Moderate: 'bg-risk-moderate/10 border-risk-moderate/30',
  High: 'bg-risk-high/10 border-risk-high/30',
  Extreme: 'bg-risk-extreme/10 border-risk-extreme/30',
}

export default function CompareInline({ addressA, riskProfileA, onClose }) {
  const [query, setQuery] = useState('')
  const [resultB, setResultB] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [showBreakdown, setShowBreakdown] = useState(true)
  const inputRef = useRef(null)
  const autocompleteRef = useRef(null)

  const analyzeAddress = useCallback(async (addr) => {
    setLoading(true)
    setError('')
    try {
      const geo = await geocodeAddress(addr)
      const risk = await getRiskProfile(geo.lat, geo.lng)
      setResultB({
        address: geo.formatted_address || addr,
        riskProfile: risk,
      })
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to analyze address.')
    } finally {
      setLoading(false)
    }
  }, [])

  // Attach Google Maps Autocomplete widget directly to the input
  useEffect(() => {
    if (resultB) return // Don't init when showing results

    const initAutocomplete = () => {
      if (!inputRef.current || !window.google?.maps?.places?.Autocomplete) return
      if (autocompleteRef.current) return // Already initialized

      const ac = new window.google.maps.places.Autocomplete(inputRef.current, {
        componentRestrictions: { country: 'us' },
        types: ['address'],
        fields: ['formatted_address'],
      })

      ac.addListener('place_changed', () => {
        const place = ac.getPlace()
        if (place?.formatted_address) {
          setQuery(place.formatted_address)
          analyzeAddress(place.formatted_address)
        }
      })

      autocompleteRef.current = ac
    }

    initAutocomplete()
    const t1 = setTimeout(initAutocomplete, 1000)
    const t2 = setTimeout(initAutocomplete, 3000)
    return () => {
      clearTimeout(t1)
      clearTimeout(t2)
    }
  }, [resultB, analyzeAddress])

  // Clean up autocomplete widget when result is cleared
  useEffect(() => {
    if (resultB) {
      autocompleteRef.current = null
    }
  }, [resultB])

  const handleSubmit = (e) => {
    e.preventDefault()
    if (query.trim()) analyzeAddress(query.trim())
  }

  const rA = riskProfileA
  const rB = resultB?.riskProfile

  return (
    <div className="rounded-xl bg-bg-secondary border border-accent/20 overflow-hidden animate-fade-in-up">
      {/* Header */}
      <div className="p-3 flex items-center justify-between border-b border-white/5">
        <div className="flex items-center gap-2">
          <ArrowLeftRight className="w-4 h-4 text-accent" />
          <span className="text-sm font-semibold text-text-primary">Compare Addresses</span>
        </div>
        <button
          onClick={onClose}
          className="p-1 rounded hover:bg-white/10 transition-colors"
        >
          <X className="w-3.5 h-3.5 text-text-secondary" />
        </button>
      </div>

      {/* Address A summary */}
      <div className="px-3 pt-3">
        <p className="text-[10px] text-text-secondary uppercase tracking-wider mb-1">Address A</p>
        <div className={`p-2.5 rounded-lg border ${OVERALL_BG[rA.overall_risk]}`}>
          <p className="text-xs text-text-secondary truncate">{addressA}</p>
          <div className="flex items-center gap-1.5 mt-1">
            <ShieldAlert className={`w-4 h-4 ${SEVERITY_COLORS[rA.overall_risk]}`} />
            <span className={`text-sm font-bold ${SEVERITY_COLORS[rA.overall_risk]}`}>
              {rA.overall_risk}
            </span>
          </div>
        </div>
      </div>

      {/* Address B search */}
      <div className="px-3 pt-3">
        <p className="text-[10px] text-text-secondary uppercase tracking-wider mb-1">Address B</p>
        {resultB ? (
          <div className={`p-2.5 rounded-lg border ${OVERALL_BG[rB.overall_risk]}`}>
            <div className="flex items-center justify-between">
              <p className="text-xs text-text-secondary truncate flex-1">{resultB.address}</p>
              <button
                onClick={() => { setResultB(null); setQuery(''); setError('') }}
                className="p-0.5 rounded hover:bg-white/10 ml-1"
              >
                <X className="w-3 h-3 text-text-secondary" />
              </button>
            </div>
            <div className="flex items-center gap-1.5 mt-1">
              <ShieldAlert className={`w-4 h-4 ${SEVERITY_COLORS[rB.overall_risk]}`} />
              <span className={`text-sm font-bold ${SEVERITY_COLORS[rB.overall_risk]}`}>
                {rB.overall_risk}
              </span>
            </div>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="relative">
            <MapPin className="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-text-secondary z-10" />
            <input
              ref={inputRef}
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Enter second address..."
              className="w-full pl-8 pr-9 py-2 bg-bg-tertiary/50 border border-white/10 rounded-lg text-xs text-text-primary placeholder-text-secondary focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent/50 transition-all"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || !query.trim()}
              className="absolute right-1.5 top-1/2 -translate-y-1/2 p-1 rounded bg-accent hover:bg-accent-hover disabled:opacity-40 transition-colors z-10"
            >
              {loading ? (
                <Loader2 className="w-3 h-3 text-white animate-spin" />
              ) : (
                <Search className="w-3 h-3 text-white" />
              )}
            </button>
          </form>
        )}
        {error && <p className="text-xs text-red-400 mt-1.5">{error}</p>}
      </div>

      {/* Comparison results */}
      {rB && (
        <div className="px-3 pb-3 pt-2">
          {(() => {
            const sA = SEVERITY_ORDER[rA.overall_risk] || 0
            const sB = SEVERITY_ORDER[rB.overall_risk] || 0
            if (sA === sB) {
              return (
                <p className="text-xs text-text-secondary text-center py-1.5">
                  Both addresses have the same overall risk level.
                </p>
              )
            }
            const saferLabel = sA < sB ? 'Address A' : 'Address B'
            return (
              <div className="py-1.5 px-2.5 rounded-lg bg-green-500/10 border border-green-500/20 mb-2">
                <p className="text-xs text-green-400 text-center">
                  <span className="font-semibold">{saferLabel}</span> has a lower overall risk.
                </p>
              </div>
            )
          })()}

          <button
            onClick={() => setShowBreakdown(!showBreakdown)}
            className="w-full flex items-center justify-between text-xs text-text-secondary hover:text-text-primary py-1 transition-colors"
          >
            <span className="font-medium">Risk Breakdown</span>
            {showBreakdown ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
          </button>

          {showBreakdown && (
            <div className="space-y-2 mt-1">
              {RISK_TYPES.map(({ key, label, Icon }) => {
                const a = rA.risks?.[key]
                const b = rB.risks?.[key]
                if (!a && !b) return null

                return (
                  <div key={key} className="p-2 rounded-lg bg-bg-tertiary/30">
                    <div className="flex items-center gap-1.5 mb-2">
                      <Icon className="w-3 h-3 text-text-secondary" />
                      <span className="text-[11px] font-semibold text-text-primary">{label}</span>
                    </div>
                    <div className="grid grid-cols-2 gap-2">
                      {[{ risk: a, label: 'A' }, { risk: b, label: 'B' }].map(({ risk, label: l }) => (
                        <div key={l}>
                          <div className="flex items-center justify-between mb-0.5">
                            <span className="text-[10px] text-text-secondary">{l}</span>
                            {risk ? (
                              <span className={`text-[10px] font-bold ${SEVERITY_COLORS[risk.severity]}`}>
                                {risk.score}
                              </span>
                            ) : (
                              <span className="text-[10px] text-text-secondary">N/A</span>
                            )}
                          </div>
                          {risk && (
                            <div className="w-full h-1 bg-bg-tertiary rounded-full overflow-hidden">
                              <div
                                className={`h-full rounded-full ${BAR_COLORS[risk.severity]}`}
                                style={{ width: `${risk.score}%` }}
                              />
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )
              })}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
