import { useState, useCallback, useRef, useEffect } from 'react'
import {
  ArrowLeftRight, X, Loader2, MapPin, Search,
  CloudLightning, Waves, Mountain, Flame, ShieldAlert, Trophy,
} from 'lucide-react'
import { geocodeAddress, getRiskProfile } from '../services/api'

function dismissPac() {
  document.querySelectorAll('.pac-container').forEach((el) => {
    el.style.display = 'none'
  })
}

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
  const [hasText, setHasText] = useState(false)
  const [resultB, setResultB] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [showBreakdown] = useState(true)
  const inputRef = useRef(null)
  const autocompleteRef = useRef(null)

  const analyzeAddress = useCallback(async (addr) => {
    dismissPac()
    inputRef.current?.blur()
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

  // Attach Google Maps Autocomplete widget directly to the input (uncontrolled)
  useEffect(() => {
    if (resultB) return

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

  useEffect(() => {
    if (resultB) {
      autocompleteRef.current = null
    }
  }, [resultB])

  const handleSubmit = (e) => {
    e.preventDefault()
    const val = inputRef.current?.value?.trim()
    if (val) analyzeAddress(val)
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
                onClick={() => { setResultB(null); setHasText(false); setError(''); if (inputRef.current) inputRef.current.value = '' }}
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
              onChange={(e) => setHasText(e.target.value.length > 0)}
              placeholder="Enter second address..."
              className="w-full pl-8 pr-9 py-2 bg-bg-tertiary/50 border border-white/10 rounded-lg text-xs text-text-primary placeholder-text-secondary focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent/50 transition-all"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || !hasText}
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
        <div className="px-3 pb-3 pt-2 space-y-2">
          {/* Winner banner */}
          {(() => {
            const sA = SEVERITY_ORDER[rA.overall_risk] || 0
            const sB = SEVERITY_ORDER[rB.overall_risk] || 0
            if (sA === sB) {
              return (
                <div className="py-2 px-3 rounded-lg bg-bg-tertiary/50 border border-white/10 text-center">
                  <p className="text-xs text-text-secondary">Both addresses have the same overall risk.</p>
                </div>
              )
            }
            const safer = sA < sB ? 'A' : 'B'
            const saferAddr = sA < sB ? addressA : resultB.address
            return (
              <div className="py-2 px-3 rounded-lg bg-accent/10 border border-accent/20 flex items-center gap-2">
                <Trophy className="w-4 h-4 text-accent shrink-0" />
                <div>
                  <p className="text-xs font-semibold text-accent">Address {safer} is safer</p>
                  <p className="text-[10px] text-text-secondary truncate">{saferAddr}</p>
                </div>
              </div>
            )
          })()}

          {/* Column headers */}
          <div className="grid grid-cols-[1fr_auto_auto] gap-1 px-1 pt-1">
            <span className="text-[10px] text-text-secondary uppercase tracking-wider">Hazard</span>
            <span className="text-[10px] text-text-secondary uppercase tracking-wider w-12 text-center">A</span>
            <span className="text-[10px] text-text-secondary uppercase tracking-wider w-12 text-center">B</span>
          </div>

          {/* Per-hazard rows */}
          {showBreakdown && RISK_TYPES.map(({ key, label, Icon }) => {
            const a = rA.risks?.[key]
            const b = rB.risks?.[key]
            if (!a && !b) return null
            const scoreA = a?.score ?? 0
            const scoreB = b?.score ?? 0
            const betterA = scoreA < scoreB
            const betterB = scoreB < scoreA
            const tie = scoreA === scoreB

            return (
              <div key={key} className="rounded-lg bg-bg-tertiary/30 p-2">
                <div className="grid grid-cols-[1fr_auto_auto] gap-1 items-center">
                  <div className="flex items-center gap-1.5">
                    <Icon className="w-3.5 h-3.5 text-text-secondary" />
                    <span className="text-[11px] font-medium text-text-primary">{label}</span>
                  </div>
                  <div className={`w-12 text-center rounded-md py-0.5 ${a ? (betterA && !tie ? 'bg-accent/15' : '') : ''}`}>
                    <span className={`text-[11px] font-bold ${a ? SEVERITY_COLORS[a.severity] : 'text-text-secondary'}`}>
                      {a ? a.score : '--'}
                    </span>
                  </div>
                  <div className={`w-12 text-center rounded-md py-0.5 ${b ? (betterB && !tie ? 'bg-accent/15' : '') : ''}`}>
                    <span className={`text-[11px] font-bold ${b ? SEVERITY_COLORS[b.severity] : 'text-text-secondary'}`}>
                      {b ? b.score : '--'}
                    </span>
                  </div>
                </div>
                {/* Dual progress bars */}
                <div className="mt-1.5 space-y-1">
                  <div className="flex items-center gap-1.5">
                    <span className="text-[9px] text-text-secondary w-2">A</span>
                    <div className="flex-1 h-1 bg-bg-tertiary rounded-full overflow-hidden">
                      {a && (
                        <div
                          className={`h-full rounded-full transition-all duration-700 ${BAR_COLORS[a.severity]}`}
                          style={{ width: `${a.score}%` }}
                        />
                      )}
                    </div>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <span className="text-[9px] text-text-secondary w-2">B</span>
                    <div className="flex-1 h-1 bg-bg-tertiary rounded-full overflow-hidden">
                      {b && (
                        <div
                          className={`h-full rounded-full transition-all duration-700 ${BAR_COLORS[b.severity]}`}
                          style={{ width: `${b.score}%` }}
                        />
                      )}
                    </div>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
