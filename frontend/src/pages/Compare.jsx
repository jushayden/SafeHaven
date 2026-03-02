import { useState, useCallback } from 'react'
import { Shield, ArrowLeftRight, Loader2, MapPin, Search, CloudLightning, Waves, Mountain, Flame, ShieldAlert, ArrowLeft } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
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

function AddressInput({ label, value, onChange, onSubmit, isLoading }) {
  const handleSubmit = (e) => {
    e.preventDefault()
    if (value.trim()) onSubmit()
  }

  return (
    <form onSubmit={handleSubmit} className="relative">
      <label className="text-xs text-text-secondary mb-1.5 block">{label}</label>
      <div className="relative">
        <MapPin className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-secondary" />
        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder="Enter a U.S. address..."
          className="w-full pl-9 pr-10 py-2.5 bg-bg-tertiary/50 border border-white/10 rounded-lg text-sm text-text-primary placeholder-text-secondary focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent/50 transition-all"
          disabled={isLoading}
        />
        <button
          type="submit"
          disabled={isLoading || !value.trim()}
          className="absolute right-2 top-1/2 -translate-y-1/2 p-1 rounded-md bg-accent hover:bg-accent-hover disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
        >
          {isLoading ? (
            <Loader2 className="w-3.5 h-3.5 text-white animate-spin" />
          ) : (
            <Search className="w-3.5 h-3.5 text-white" />
          )}
        </button>
      </div>
    </form>
  )
}

export default function Compare() {
  const navigate = useNavigate()
  const [addrA, setAddrA] = useState('')
  const [addrB, setAddrB] = useState('')
  const [resultA, setResultA] = useState(null)
  const [resultB, setResultB] = useState(null)
  const [loadingA, setLoadingA] = useState(false)
  const [loadingB, setLoadingB] = useState(false)
  const [errorA, setErrorA] = useState('')
  const [errorB, setErrorB] = useState('')

  const analyzeAddress = useCallback(async (query, setResult, setLoading, setError) => {
    setLoading(true)
    setError('')
    try {
      const geo = await geocodeAddress(query)
      const risk = await getRiskProfile(geo.lat, geo.lng)
      setResult({
        address: geo.formatted_address || query,
        riskProfile: risk,
      })
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to analyze this address.')
      setResult(null)
    } finally {
      setLoading(false)
    }
  }, [])

  const bothLoaded = resultA && resultB

  return (
    <div className="pt-14 min-h-screen">
      <div className="max-w-5xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex items-center gap-3 mb-6">
          <button
            onClick={() => navigate('/dashboard')}
            className="p-2 rounded-lg hover:bg-white/5 transition-colors"
          >
            <ArrowLeft className="w-5 h-5 text-text-secondary" />
          </button>
          <div className="flex items-center gap-2">
            <ArrowLeftRight className="w-5 h-5 text-accent" />
            <h1 className="text-xl font-bold text-text-primary">Compare Addresses</h1>
          </div>
        </div>

        {/* Address inputs */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
          <div className="p-4 rounded-xl bg-bg-secondary border border-white/5">
            <AddressInput
              label="Address A"
              value={addrA}
              onChange={setAddrA}
              onSubmit={() => analyzeAddress(addrA, setResultA, setLoadingA, setErrorA)}
              isLoading={loadingA}
            />
            {errorA && <p className="text-xs text-red-400 mt-2">{errorA}</p>}
          </div>
          <div className="p-4 rounded-xl bg-bg-secondary border border-white/5">
            <AddressInput
              label="Address B"
              value={addrB}
              onChange={setAddrB}
              onSubmit={() => analyzeAddress(addrB, setResultB, setLoadingB, setErrorB)}
              isLoading={loadingB}
            />
            {errorB && <p className="text-xs text-red-400 mt-2">{errorB}</p>}
          </div>
        </div>

        {/* Loading skeleton */}
        {(loadingA || loadingB) && (
          <div className="flex items-center justify-center gap-2 py-8 text-text-secondary text-sm">
            <Loader2 className="w-4 h-4 animate-spin" />
            <span>Analyzing...</span>
          </div>
        )}

        {/* Results comparison */}
        {bothLoaded && (
          <div className="space-y-6 animate-fade-in-up">
            {/* Overall risk comparison */}
            <div className="grid grid-cols-2 gap-4">
              {[resultA, resultB].map((r, i) => (
                <div
                  key={i}
                  className={`p-4 rounded-xl border ${OVERALL_BG[r.riskProfile.overall_risk]}`}
                >
                  <p className="text-xs text-text-secondary truncate mb-1">{r.address}</p>
                  <div className="flex items-center gap-2">
                    <ShieldAlert className={`w-6 h-6 ${SEVERITY_COLORS[r.riskProfile.overall_risk]}`} />
                    <span className={`text-lg font-bold ${SEVERITY_COLORS[r.riskProfile.overall_risk]}`}>
                      {r.riskProfile.overall_risk}
                    </span>
                  </div>
                </div>
              ))}
            </div>

            {/* Winner callout */}
            {(() => {
              const sA = SEVERITY_ORDER[resultA.riskProfile.overall_risk] || 0
              const sB = SEVERITY_ORDER[resultB.riskProfile.overall_risk] || 0
              if (sA === sB) {
                return (
                  <div className="text-center py-2">
                    <p className="text-sm text-text-secondary">Both addresses have the same overall risk level.</p>
                  </div>
                )
              }
              const safer = sA < sB ? resultA : resultB
              return (
                <div className="text-center py-2 px-4 rounded-lg bg-green-500/10 border border-green-500/20">
                  <p className="text-sm text-green-400">
                    <span className="font-semibold">{safer.address}</span> has a lower overall risk.
                  </p>
                </div>
              )
            })()}

            {/* Per-hazard comparison */}
            <div className="space-y-3">
              <h2 className="text-sm font-semibold text-text-primary">Risk Breakdown</h2>
              {RISK_TYPES.map(({ key, label, Icon }) => {
                const a = resultA.riskProfile.risks?.[key]
                const b = resultB.riskProfile.risks?.[key]
                if (!a && !b) return null

                return (
                  <div key={key} className="p-4 rounded-xl bg-bg-secondary border border-white/5">
                    <div className="flex items-center gap-2 mb-3">
                      <Icon className="w-4 h-4 text-text-secondary" />
                      <span className="text-sm font-semibold text-text-primary">{label}</span>
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      {[a, b].map((risk, i) => (
                        <div key={i}>
                          <p className="text-[10px] text-text-secondary truncate mb-1">
                            {i === 0 ? resultA.address : resultB.address}
                          </p>
                          {risk ? (
                            <>
                              <div className="flex items-center justify-between mb-1">
                                <span className={`text-xs font-bold ${SEVERITY_COLORS[risk.severity]}`}>
                                  {risk.severity}
                                </span>
                                <span className="text-xs font-mono text-text-secondary">{risk.score}/100</span>
                              </div>
                              <div className="w-full h-1.5 bg-bg-tertiary rounded-full overflow-hidden">
                                <div
                                  className={`h-full rounded-full transition-all duration-1000 ${BAR_COLORS[risk.severity]}`}
                                  style={{ width: `${risk.score}%` }}
                                />
                              </div>
                            </>
                          ) : (
                            <p className="text-xs text-text-secondary">N/A</p>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        )}

        {/* Empty state */}
        {!bothLoaded && !loadingA && !loadingB && (
          <div className="text-center py-16">
            <ArrowLeftRight className="w-12 h-12 text-bg-tertiary mx-auto mb-4" />
            <p className="text-sm text-text-secondary max-w-sm mx-auto">
              Enter two U.S. addresses above and search each one to compare their disaster risk profiles side by side.
            </p>
          </div>
        )}
      </div>
    </div>
  )
}
