import { useState } from 'react'
import { Route, ChevronDown, ChevronUp, Loader2, Navigation } from 'lucide-react'

function haversineDistance(lat1, lng1, lat2, lng2) {
  const R = 3959
  const dLat = ((lat2 - lat1) * Math.PI) / 180
  const dLng = ((lng2 - lng1) * Math.PI) / 180
  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos((lat1 * Math.PI) / 180) * Math.cos((lat2 * Math.PI) / 180) * Math.sin(dLng / 2) ** 2
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
}

export default function EvacuationRoutes({ center, shelters = [], onRoutesCalculated }) {
  const [isOpen, setIsOpen] = useState(false)
  const [routes, setRoutes] = useState([])
  const [loading, setLoading] = useState(false)
  const [loaded, setLoaded] = useState(false)

  const handleOpen = async () => {
    if (isOpen) {
      setIsOpen(false)
      return
    }
    setIsOpen(true)

    if (!loaded && center && shelters.length > 0 && window.google?.maps) {
      setLoading(true)
      try {
        const directionsService = new window.google.maps.DirectionsService()

        // Pick the closest 5 shelters by straight-line distance
        const sorted = [...shelters]
          .map((s) => ({
            ...s,
            dist: haversineDistance(center.lat, center.lng, s.lat, s.lng),
          }))
          .sort((a, b) => a.dist - b.dist)
          .slice(0, 5)

        const results = await Promise.allSettled(
          sorted.map(
            (s) =>
              new Promise((resolve, reject) => {
                directionsService.route(
                  {
                    origin: new window.google.maps.LatLng(center.lat, center.lng),
                    destination: new window.google.maps.LatLng(s.lat, s.lng),
                    travelMode: window.google.maps.TravelMode.DRIVING,
                  },
                  (result, status) => {
                    if (status === 'OK' && result.routes?.[0]?.legs?.[0]) {
                      const leg = result.routes[0].legs[0]
                      resolve({
                        name: s.name,
                        type: s.type || 'Safe Location',
                        address: s.address || leg.end_address || '',
                        distance: leg.distance?.text || '',
                        duration: leg.duration?.text || '',
                        distanceValue: leg.distance?.value || 0,
                        lat: s.lat,
                        lng: s.lng,
                        directionsResult: result,
                      })
                    } else {
                      reject(status)
                    }
                  }
                )
              })
          )
        )

        const successful = results
          .filter((r) => r.status === 'fulfilled')
          .map((r) => r.value)
          .sort((a, b) => a.distanceValue - b.distanceValue)

        setRoutes(successful)
        onRoutesCalculated?.(successful)
      } catch {
        setRoutes([])
        onRoutesCalculated?.([])
      } finally {
        setLoading(false)
        setLoaded(true)
      }
    }
  }

  if (!center) return null

  return (
    <div className="rounded-xl bg-bg-secondary border border-white/5 overflow-hidden">
      <button
        onClick={handleOpen}
        className="w-full p-4 flex items-center justify-between hover:bg-white/[0.02] transition-colors"
      >
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-green-500/10">
            <Route className="w-5 h-5 text-green-400" />
          </div>
          <div className="text-left">
            <p className="text-sm font-semibold text-text-primary">Evacuation Routes</p>
            <p className="text-xs text-text-secondary">
              {routes.length > 0
                ? `${routes.length} routes calculated`
                : 'Driving directions to nearest safe locations'}
            </p>
          </div>
        </div>
        {isOpen ? (
          <ChevronUp className="w-4 h-4 text-text-secondary" />
        ) : (
          <ChevronDown className="w-4 h-4 text-text-secondary" />
        )}
      </button>

      {isOpen && (
        <div className="border-t border-white/5">
          {loading ? (
            <div className="p-6 flex items-center justify-center gap-2 text-text-secondary text-sm">
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>Calculating routes...</span>
            </div>
          ) : routes.length === 0 && loaded ? (
            <div className="p-6 text-center text-text-secondary text-sm">
              {shelters.length === 0
                ? 'No nearby safe locations found.'
                : 'Unable to calculate routes. The Directions API may not be available.'}
            </div>
          ) : routes.length === 0 && !loaded ? (
            <div className="p-6 flex items-center justify-center gap-2 text-text-secondary text-sm">
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>Calculating routes...</span>
            </div>
          ) : (
            <div className="p-3 space-y-2">
              {routes.map((r, i) => (
                <div
                  key={i}
                  className="p-3 rounded-lg bg-bg-tertiary/30 hover:bg-bg-tertiary/50 transition-colors"
                >
                  <div className="flex items-start justify-between gap-2">
                    <div className="min-w-0 flex-1">
                      <p className="text-sm font-medium text-text-primary truncate">{r.name}</p>
                      <p className="text-[10px] text-text-secondary truncate">{r.type}</p>
                    </div>
                    <div className="text-right shrink-0">
                      <p className="text-sm font-semibold text-accent">{r.duration}</p>
                      <p className="text-[10px] text-text-secondary">{r.distance}</p>
                    </div>
                  </div>
                  <a
                    href={`https://www.google.com/maps/dir/?api=1&origin=${center.lat},${center.lng}&destination=${r.lat},${r.lng}&travelmode=driving`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-1 text-[11px] text-accent hover:underline mt-2"
                  >
                    <Navigation className="w-3 h-3" />
                    Open in Google Maps
                  </a>
                </div>
              ))}
              <p className="text-[10px] text-text-secondary text-center pt-1">
                Actual travel times may vary based on traffic conditions.
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
