import { useState, useEffect } from 'react'
import { AlertTriangle, Bell, ChevronDown, ChevronUp, Clock, ShieldAlert } from 'lucide-react'
import { getNOAAAlerts } from '../services/api'

const SEVERITY_STYLES = {
  Extreme: 'bg-red-500/15 border-red-500/30 text-red-400',
  Severe: 'bg-orange-500/15 border-orange-500/30 text-orange-400',
  Moderate: 'bg-yellow-500/15 border-yellow-500/30 text-yellow-400',
  Minor: 'bg-blue-500/15 border-blue-500/30 text-blue-400',
  Unknown: 'bg-gray-500/15 border-gray-500/30 text-gray-400',
}

export default function NOAAAlerts({ lat, lng }) {
  const [alerts, setAlerts] = useState([])
  const [loading, setLoading] = useState(true)
  const [expandedId, setExpandedId] = useState(null)

  useEffect(() => {
    if (!lat || !lng) return
    setLoading(true)
    getNOAAAlerts(lat, lng)
      .then((data) => setAlerts(data.alerts || []))
      .catch(() => setAlerts([]))
      .finally(() => setLoading(false))
  }, [lat, lng])

  if (loading) {
    return (
      <div className="p-4 rounded-xl bg-bg-secondary border border-white/5">
        <div className="flex items-center gap-2 text-sm text-text-secondary">
          <Bell className="w-4 h-4 animate-pulse" />
          <span>Checking for active weather alerts...</span>
        </div>
      </div>
    )
  }

  if (alerts.length === 0) {
    return (
      <div className="p-4 rounded-xl bg-green-500/10 border border-green-500/20">
        <div className="flex items-center gap-2">
          <ShieldAlert className="w-4 h-4 text-green-400" />
          <span className="text-sm font-medium text-green-400">No Active Alerts</span>
        </div>
        <p className="text-xs text-text-secondary mt-1 ml-6">
          There are no active NOAA weather alerts for this area.
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-2">
      <div className="flex items-center gap-2 text-sm font-medium text-text-primary">
        <AlertTriangle className="w-4 h-4 text-amber-400" />
        <span>Active Alerts ({alerts.length})</span>
      </div>
      {alerts.map((alert, i) => {
        const style = SEVERITY_STYLES[alert.severity] || SEVERITY_STYLES.Unknown
        const isExpanded = expandedId === i
        const expires = alert.expires
          ? new Date(alert.expires).toLocaleString('en-US', {
              month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit',
            })
          : null

        return (
          <div key={i} className={`rounded-lg border ${style}`}>
            <button
              onClick={() => setExpandedId(isExpanded ? null : i)}
              className="w-full p-3 flex items-start gap-2 text-left"
            >
              <AlertTriangle className="w-4 h-4 mt-0.5 shrink-0" />
              <div className="flex-1 min-w-0">
                <p className="text-sm font-semibold leading-tight">{alert.event}</p>
                <div className="flex items-center gap-2 mt-1">
                  <span className="text-[10px] uppercase font-bold opacity-75">{alert.severity}</span>
                  {expires && (
                    <span className="text-[10px] text-text-secondary flex items-center gap-0.5">
                      <Clock className="w-2.5 h-2.5" />
                      Expires {expires}
                    </span>
                  )}
                </div>
              </div>
              {isExpanded ? (
                <ChevronUp className="w-4 h-4 shrink-0 opacity-50" />
              ) : (
                <ChevronDown className="w-4 h-4 shrink-0 opacity-50" />
              )}
            </button>
            {isExpanded && (
              <div className="px-3 pb-3 space-y-2 border-t border-white/10 pt-2">
                {alert.headline && (
                  <p className="text-xs text-text-primary leading-relaxed">{alert.headline}</p>
                )}
                {alert.description && (
                  <p className="text-xs text-text-secondary leading-relaxed whitespace-pre-line">
                    {alert.description.slice(0, 600)}{alert.description.length > 600 ? '...' : ''}
                  </p>
                )}
                {alert.instruction && (
                  <div className="p-2 rounded bg-white/5">
                    <p className="text-[10px] font-semibold text-text-primary mb-0.5 uppercase">What To Do</p>
                    <p className="text-xs text-text-secondary leading-relaxed">{alert.instruction.slice(0, 400)}</p>
                  </div>
                )}
                {alert.areas && (
                  <p className="text-[10px] text-text-secondary">
                    <span className="font-medium">Areas:</span> {alert.areas}
                  </p>
                )}
              </div>
            )}
          </div>
        )
      })}
    </div>
  )
}
