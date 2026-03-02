import { useState, useCallback, useRef } from 'react'
import { Shield, ArrowLeftRight, MapPin, BarChart3, Bot, FileDown } from 'lucide-react'
import AddressSearch from '../components/AddressSearch'
import RiskCard from '../components/RiskCard'
import OverallRisk from '../components/OverallRisk'
import NOAAAlerts from '../components/NOAAAlerts'
import AIReport from '../components/AIReport'
import EmergencyKit from '../components/EmergencyKit'
import HistoricalDisasters from '../components/HistoricalDisasters'
import EmergencyContacts from '../components/EmergencyContacts'
import EvacuationRoutes from '../components/EvacuationRoutes'
import CompareInline from '../components/CompareInline'
import MapView from '../components/MapView'
import ShareButton from '../components/ShareButton'
import ExportPDFButton from '../components/ExportPDFButton'
import ErrorBoundary from '../components/ErrorBoundary'
import { geocodeAddress, getRiskProfile, getShelters, getAIReport } from '../services/api'

export default function Dashboard() {
  const [isLoading, setIsLoading] = useState(false)
  const [isReportLoading, setIsReportLoading] = useState(false)
  const [mapCenter, setMapCenter] = useState(null)
  const [riskProfile, setRiskProfile] = useState(null)
  const [searchShelters, setSearchShelters] = useState([])
  const [viewportShelters, setViewportShelters] = useState([])
  const [aiReport, setAiReport] = useState('')
  const [address, setAddress] = useState('')
  const [state, setState] = useState('')
  const [error, setError] = useState('')
  const [compareOpen, setCompareOpen] = useState(false)
  const [evacRoutes, setEvacRoutes] = useState([])
  const viewportTimerRef = useRef(null)
  const lastViewportKeyRef = useRef('')

  // Merge address-search places + viewport-loaded places, deduplicating by name+lat
  const shelters = (() => {
    const seen = new Set()
    const merged = []
    for (const s of searchShelters) {
      const key = `${s.name}|${s.lat}|${s.lng}`
      if (!seen.has(key)) { seen.add(key); merged.push(s) }
    }
    for (const s of viewportShelters) {
      const key = `${s.name}|${s.lat}|${s.lng}`
      if (!seen.has(key)) { seen.add(key); merged.push(s) }
    }
    return merged
  })()

  const handleClear = useCallback(() => {
    setMapCenter(null)
    setRiskProfile(null)
    setSearchShelters([])
    setViewportShelters([])
    setAiReport('')
    setAddress('')
    setState('')
    setError('')
    setEvacRoutes([])
  }, [])

  const handleSearch = useCallback(async (query) => {
    setIsLoading(true)
    setError('')
    setRiskProfile(null)
    setAiReport('')
    setSearchShelters([])

    try {
      // Step 1: Geocode
      const geo = await geocodeAddress(query)
      console.log('[SafeHaven] Geocode result:', geo)
      setMapCenter({ lat: geo.lat, lng: geo.lng })
      setAddress(geo.formatted_address || query)

      // Step 2: Risk profile + shelters in parallel
      const [risk, shelterData] = await Promise.all([
        getRiskProfile(geo.lat, geo.lng),
        getShelters(geo.lat, geo.lng).catch(() => ({ places: [] })),
      ])

      console.log('[SafeHaven] Risk profile:', risk)
      console.log('[SafeHaven] Shelters:', shelterData)

      setRiskProfile(risk)
      setState(risk.state || '')
      setSearchShelters(shelterData.places || [])
      setIsLoading(false)

      // Step 3: AI report (after main data loads so UI is responsive)
      setIsReportLoading(true)
      try {
        const report = await getAIReport({
          address: geo.formatted_address || query,
          state: risk.state,
          risks: risk.risks,
          overall_risk: risk.overall_risk,
          location_factors: risk.location_factors,
        })
        console.log('[SafeHaven] AI report received')
        setAiReport(report.report || '')
      } catch (e) {
        console.error('[SafeHaven] AI report error:', e)
        setAiReport('Unable to generate AI report at this time. Please try again later.')
      } finally {
        setIsReportLoading(false)
      }
    } catch (err) {
      console.error('[SafeHaven] Search error:', err)
      setError(err.response?.data?.detail || 'Failed to analyze this address. Please try again.')
      setIsLoading(false)
    }
  }, [])

  // Load places when user pans/zooms the map to zoom >= 12
  const handleViewportChange = useCallback(({ lat, lng }) => {
    // Round to ~500m grid to avoid re-fetching for tiny pans
    const key = `${lat.toFixed(2)}|${lng.toFixed(2)}`
    if (key === lastViewportKeyRef.current) return
    lastViewportKeyRef.current = key

    clearTimeout(viewportTimerRef.current)
    viewportTimerRef.current = setTimeout(async () => {
      try {
        const data = await getShelters(lat, lng)
        setViewportShelters(data.places || [])
      } catch {
        // Silently fail — viewport loading is best-effort
      }
    }, 600)
  }, [])

  return (
    <div className="pt-14 min-h-screen">
      <div className="flex flex-col md:flex-row h-[calc(100vh-3.5rem)]">
        {/* Left Sidebar */}
        <div className="w-full md:w-[420px] lg:w-[460px] shrink-0 overflow-y-auto border-r border-white/5 p-4 space-y-4">
          <AddressSearch onSearch={handleSearch} onClear={handleClear} isLoading={isLoading} hasResults={!!riskProfile} />

          {riskProfile && !isLoading && !compareOpen && (
            <button
              onClick={() => setCompareOpen(true)}
              className="flex items-center gap-1.5 text-xs text-text-secondary hover:text-accent transition-colors"
            >
              <ArrowLeftRight className="w-3.5 h-3.5" />
              Compare with another address
            </button>
          )}

          {compareOpen && riskProfile && (
            <CompareInline
              addressA={address}
              riskProfileA={riskProfile}
              onClose={() => setCompareOpen(false)}
            />
          )}

          {error && (
            <div className="p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm">
              {error}
            </div>
          )}

          {!riskProfile && !isLoading && !error && (
            <div className="py-8">
              <div className="flex flex-col items-center text-center mb-6">
                <Shield className="w-12 h-12 text-accent/40 mb-3" />
                <h2 className="text-lg font-semibold text-text-primary mb-1">
                  Know Your Risk
                </h2>
                <p className="text-sm text-text-secondary max-w-xs">
                  Get a comprehensive disaster risk assessment for any U.S. address.
                </p>
              </div>

              <div className="space-y-3">
                <p className="text-[10px] text-text-secondary uppercase tracking-wider font-medium px-1">How it works</p>
                {[
                  { icon: MapPin, step: '1', title: 'Enter an address', desc: 'Type any U.S. address in the search bar above' },
                  { icon: BarChart3, step: '2', title: 'View risk scores', desc: 'See hurricane, flood, earthquake & wildfire risk levels' },
                  { icon: Bot, step: '3', title: 'Read AI insights', desc: 'Get a personalized safety report powered by Gemini AI' },
                  { icon: FileDown, step: '4', title: 'Export & compare', desc: 'Download a PDF report or compare two addresses' },
                ].map(({ icon: Icon, step, title, desc }) => (
                  <div key={step} className="flex items-start gap-3 p-3 rounded-lg bg-bg-secondary/50 border border-white/5">
                    <div className="w-8 h-8 rounded-lg bg-accent/10 flex items-center justify-center shrink-0">
                      <Icon className="w-4 h-4 text-accent" />
                    </div>
                    <div>
                      <p className="text-sm font-medium text-text-primary">{title}</p>
                      <p className="text-xs text-text-secondary mt-0.5">{desc}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {isLoading && (
            <div className="space-y-4">
              {[1, 2, 3, 4].map((i) => (
                <div key={i} className="h-28 bg-bg-secondary rounded-xl animate-pulse" />
              ))}
            </div>
          )}

          {riskProfile && !isLoading && (
            <ErrorBoundary>
              <OverallRisk severity={riskProfile.overall_risk} address={address} locationFactors={riskProfile.location_factors} />

              {/* NOAA Active Alerts */}
              {mapCenter && (
                <div className="mt-4">
                  <NOAAAlerts lat={mapCenter.lat} lng={mapCenter.lng} />
                </div>
              )}

              <div className="grid grid-cols-2 gap-3 mt-4">
                {['hurricane', 'flood', 'earthquake', 'wildfire'].map((type, i) => (
                  riskProfile.risks?.[type] && (
                    <RiskCard
                      key={type}
                      type={type}
                      data={riskProfile.risks[type]}
                      delay={i * 100}
                    />
                  )
                ))}
              </div>

              <div className="mt-4">
                <AIReport report={aiReport} isLoading={isReportLoading} />
              </div>

              {/* Emergency Kit Checklist — collapsible */}
              <div className="mt-4">
                <EmergencyKit risks={riskProfile.risks} />
              </div>

              <div className="mt-4">
                <EmergencyContacts state={state} />
              </div>

              {/* Evacuation Routes — collapsible, calculates on click */}
              {mapCenter && (
                <div className="mt-4">
                  <EvacuationRoutes center={mapCenter} shelters={shelters} onRoutesCalculated={setEvacRoutes} />
                </div>
              )}

              {/* Historical Disasters — collapsible, loads on click */}
              {state && (
                <div className="mt-4">
                  <HistoricalDisasters state={state} />
                </div>
              )}

              <div className="flex items-center gap-2 pt-2">
                <ShareButton riskProfile={riskProfile} address={address} aiReport={aiReport} />
                <ExportPDFButton
                  riskProfile={riskProfile}
                  aiReport={aiReport}
                  address={address}
                />
              </div>
            </ErrorBoundary>
          )}
        </div>

        {/* Right Map Panel */}
        <div className="flex-1 relative min-h-[400px] md:min-h-0">
          <ErrorBoundary>
            <MapView
              center={mapCenter}
              shelters={shelters}
              evacRoutes={evacRoutes}
              onViewportChange={handleViewportChange}
            />
          </ErrorBoundary>
        </div>
      </div>
    </div>
  )
}
