import { useState, useRef, useEffect, useCallback } from 'react'
import { Layers } from 'lucide-react'

const MAP_STYLES = [
  { elementType: 'geometry', stylers: [{ color: '#0c1222' }] },
  { elementType: 'labels.text.stroke', stylers: [{ color: '#0c1222' }] },
  { elementType: 'labels.text.fill', stylers: [{ color: '#6b7280' }] },
  { featureType: 'administrative', elementType: 'geometry.stroke', stylers: [{ color: '#243046' }] },
  { featureType: 'road', elementType: 'geometry', stylers: [{ color: '#1a2a3e' }] },
  { featureType: 'road', elementType: 'geometry.stroke', stylers: [{ color: '#162032' }] },
  { featureType: 'water', elementType: 'geometry', stylers: [{ color: '#081018' }] },
  { featureType: 'poi', elementType: 'geometry', stylers: [{ color: '#162032' }] },
  { featureType: 'poi.park', elementType: 'geometry', stylers: [{ color: '#0d2818' }] },
  { featureType: 'transit', elementType: 'geometry', stylers: [{ color: '#162032' }] },
]

const defaultCenter = { lat: 28.5383, lng: -81.3792 }

// Map backend place_type values to our categories
function classifyPlace(place) {
  const pt = place.place_type || ''
  if (pt === 'hospital') return 'hospital'
  if (pt === 'fire_station') return 'fire_station'
  if (pt === 'police') return 'police'
  // church, local_government_office → shelter category
  return 'shelter'
}

const MARKER_COLORS = {
  shelter: '#22c55e',
  hospital: '#3b82f6',
  fire_station: '#ef4444',
  police: '#a855f7',
}

const MARKER_LABELS = {
  shelter: 'Shelter',
  hospital: 'Hospital',
  fire_station: 'Fire Station',
  police: 'Police Station',
}

const LAYER_CONFIG = [
  { key: 'shelters', label: 'Shelters', color: 'bg-green-500', category: 'shelter' },
  { key: 'hospitals', label: 'Hospitals', color: 'bg-blue-500', category: 'hospital' },
  { key: 'fireStations', label: 'Fire Stations', color: 'bg-red-500', category: 'fire_station' },
  { key: 'police', label: 'Police Stations', color: 'bg-purple-500', category: 'police' },
]

// Load Google Maps script once
let loadPromise = null
function loadGoogleMaps() {
  if (loadPromise) return loadPromise
  if (window.google?.maps) return Promise.resolve()

  loadPromise = new Promise((resolve, reject) => {
    const key = import.meta.env.VITE_GOOGLE_MAPS_API_KEY
    if (!key) {
      reject(new Error('No API key'))
      return
    }
    const script = document.createElement('script')
    script.src = `https://maps.googleapis.com/maps/api/js?key=${key}&libraries=places`
    script.async = true
    script.defer = true
    script.onload = resolve
    script.onerror = reject
    document.head.appendChild(script)
  })
  return loadPromise
}

const MIN_ZOOM_FOR_PLACES = 12

export default function MapView({ center, shelters = [], evacRoutes = [], onViewportChange }) {
  const mapRef = useRef(null)
  const mapContainerRef = useRef(null)
  const markersRef = useRef([])
  const infoWindowRef = useRef(null)
  const centerMarkerRef = useRef(null)
  const routeRenderersRef = useRef([])
  const [isLoaded, setIsLoaded] = useState(!!window.google?.maps)
  const [loadError, setLoadError] = useState(false)
  const [showLayers, setShowLayers] = useState({
    shelters: true,
    hospitals: true,
    fireStations: true,
    police: true,
  })

  // Load the script
  useEffect(() => {
    loadGoogleMaps()
      .then(() => setIsLoaded(true))
      .catch(() => setLoadError(true))
  }, [])

  // Initialize the map
  useEffect(() => {
    if (!isLoaded || !mapContainerRef.current || mapRef.current) return

    mapRef.current = new window.google.maps.Map(mapContainerRef.current, {
      center: center || defaultCenter,
      zoom: center ? 13 : 5,
      minZoom: 4,
      maxZoom: 18,
      styles: MAP_STYLES,
      disableDefaultUI: true,
      zoomControl: true,
      zoomControlOptions: {
        position: window.google.maps.ControlPosition.RIGHT_CENTER,
      },
      fullscreenControl: true,
      fullscreenControlOptions: {
        position: window.google.maps.ControlPosition.RIGHT_BOTTOM,
      },
      restriction: {
        latLngBounds: { north: 85, south: -85, west: -180, east: 180 },
        strictBounds: true,
      },
    })

    infoWindowRef.current = new window.google.maps.InfoWindow()

    // Fire viewport change when user pans/zooms
    mapRef.current.addListener('idle', () => {
      const map = mapRef.current
      if (!map) return
      const zoom = map.getZoom()
      const c = map.getCenter()
      if (zoom >= MIN_ZOOM_FOR_PLACES && c) {
        onViewportChange?.({ lat: c.lat(), lng: c.lng(), zoom })
      }
    })
  }, [isLoaded])

  // Update center
  useEffect(() => {
    if (!mapRef.current) return

    // If center is cleared, remove marker and reset zoom
    if (!center) {
      if (centerMarkerRef.current) {
        centerMarkerRef.current.marker.setMap(null)
        centerMarkerRef.current.pulse.setMap(null)
        centerMarkerRef.current = null
      }
      mapRef.current.panTo(defaultCenter)
      mapRef.current.setZoom(5)
      return
    }

    mapRef.current.panTo(center)
    mapRef.current.setZoom(13)

    // Update or create center marker (drop-pin shape)
    const pinPath = 'M 0,-24 C -8,-24 -14,-18 -14,-10 C -14,-2 0,12 0,12 C 0,12 14,-2 14,-10 C 14,-18 8,-24 0,-24 Z'
    if (centerMarkerRef.current) {
      centerMarkerRef.current.marker.setPosition(center)
      centerMarkerRef.current.pulse.setCenter(center)
    } else {
      // Pulse ring overlay
      const pulse = new window.google.maps.Circle({
        map: mapRef.current,
        center,
        radius: 150,
        fillColor: '#10b981',
        fillOpacity: 0.15,
        strokeColor: '#10b981',
        strokeOpacity: 0.4,
        strokeWeight: 2,
        zIndex: 998,
      })
      // Animate pulse
      let growing = true
      setInterval(() => {
        const r = pulse.getRadius()
        if (growing) {
          pulse.setRadius(r + 10)
          if (r >= 300) growing = false
        } else {
          pulse.setRadius(r - 10)
          if (r <= 150) growing = true
        }
      }, 50)

      const marker = new window.google.maps.Marker({
        position: center,
        map: mapRef.current,
        icon: {
          path: pinPath,
          scale: 1.5,
          fillColor: '#10b981',
          fillOpacity: 1,
          strokeColor: '#ffffff',
          strokeWeight: 2,
          anchor: new window.google.maps.Point(0, 12),
        },
        zIndex: 999,
      })

      centerMarkerRef.current = { marker, pulse }
    }
  }, [center])

  // Update shelter/hospital/fire markers
  useEffect(() => {
    if (!mapRef.current) return

    // Clear old markers
    markersRef.current.forEach((m) => m.setMap(null))
    markersRef.current = []

    const classified = shelters.map((s) => ({ ...s, _category: classifyPlace(s) }))

    const filtered = classified.filter((s) => {
      if (s._category === 'shelter' && !showLayers.shelters) return false
      if (s._category === 'hospital' && !showLayers.hospitals) return false
      if (s._category === 'fire_station' && !showLayers.fireStations) return false
      if (s._category === 'police' && !showLayers.police) return false
      return true
    })

    filtered.forEach((s) => {
      const marker = new window.google.maps.Marker({
        position: { lat: s.lat, lng: s.lng },
        map: mapRef.current,
        icon: {
          path: window.google.maps.SymbolPath.CIRCLE,
          scale: 7,
          fillColor: MARKER_COLORS[s._category] || '#6b7280',
          fillOpacity: 0.9,
          strokeColor: '#ffffff',
          strokeWeight: 1.5,
        },
      })

      marker.addListener('click', () => {
        infoWindowRef.current.setContent(
          `<div style="padding:4px;color:#1a1a2e;">` +
            `<p style="font-weight:600;font-size:13px;margin:0">${s.name}</p>` +
            `<p style="font-size:11px;color:#666;margin:2px 0 0">${s.type || MARKER_LABELS[s._category] || ''}</p>` +
            (s.address ? `<p style="font-size:11px;color:#888;margin:2px 0 0">${s.address}</p>` : '') +
          `</div>`
        )
        infoWindowRef.current.open(mapRef.current, marker)
      })

      markersRef.current.push(marker)
    })
  }, [shelters, showLayers])

  // Render evacuation route polylines
  useEffect(() => {
    // Clear old renderers
    routeRenderersRef.current.forEach((r) => r.setMap(null))
    routeRenderersRef.current = []

    if (!mapRef.current || evacRoutes.length === 0) return

    evacRoutes.forEach((route, i) => {
      if (!route.directionsResult) return
      const renderer = new window.google.maps.DirectionsRenderer({
        map: mapRef.current,
        directions: route.directionsResult,
        suppressMarkers: true,
        polylineOptions: {
          strokeColor: '#10b981',
          strokeOpacity: i === 0 ? 0.9 : 0.5,
          strokeWeight: i === 0 ? 5 : 3,
        },
      })
      routeRenderersRef.current.push(renderer)
    })
  }, [evacRoutes])

  if (loadError) {
    return (
      <div className="w-full h-full bg-bg-secondary rounded-xl flex items-center justify-center">
        <p className="text-text-secondary text-sm">Failed to load Google Maps.</p>
      </div>
    )
  }

  if (!isLoaded) {
    return (
      <div className="w-full h-full bg-bg-secondary rounded-xl flex items-center justify-center">
        <div className="text-text-secondary text-sm">Loading map...</div>
      </div>
    )
  }

  return (
    <div className="relative w-full h-full rounded-xl overflow-hidden">
      <div ref={mapContainerRef} className="w-full h-full" />

      {/* Layer toggles — top-left to avoid zoom controls on the right */}
      <div className="absolute top-3 left-3 bg-bg-primary/90 backdrop-blur-sm border border-white/10 rounded-lg p-2 space-y-1">
        <div className="flex items-center gap-1.5 text-xs text-text-secondary px-1 mb-1">
          <Layers className="w-3 h-3" />
          <span>Layers</span>
        </div>
        {LAYER_CONFIG.map(({ key, label, color }) => (
          <label key={key} className="flex items-center gap-2 px-1 py-0.5 cursor-pointer hover:bg-white/5 rounded">
            <div className="relative">
              <input
                type="checkbox"
                checked={showLayers[key]}
                onChange={() => setShowLayers((prev) => ({ ...prev, [key]: !prev[key] }))}
                className="sr-only"
              />
              <div className={`w-3 h-3 rounded-sm border ${showLayers[key] ? `${color} border-transparent` : 'border-white/20'}`} />
            </div>
            <span className="text-xs text-text-primary">{label}</span>
          </label>
        ))}
      </div>

      {/* Legend — bottom-right to avoid Google attribution on the bottom-left */}
      {(center || shelters.length > 0) && (
        <div className="absolute bottom-3 right-14 bg-bg-primary/90 backdrop-blur-sm border border-white/10 rounded-lg p-2">
          <div className="flex flex-wrap items-center gap-3">
            <div className="flex items-center gap-1">
              <div className="w-2.5 h-2.5 rounded-full bg-accent" />
              <span className="text-[10px] text-text-secondary">Your Location</span>
            </div>
            {LAYER_CONFIG.filter(({ key }) => showLayers[key]).map(({ key, label, color }) => (
              <div key={key} className="flex items-center gap-1">
                <div className={`w-2.5 h-2.5 rounded-full ${color}`} />
                <span className="text-[10px] text-text-secondary">{label.replace(/s$/, '')}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
