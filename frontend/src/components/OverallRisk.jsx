import { ShieldAlert, AlertTriangle } from 'lucide-react'

const SEVERITY_STYLES = {
  Low: 'from-risk-low/20 to-transparent border-risk-low/30 text-risk-low',
  Moderate: 'from-risk-moderate/20 to-transparent border-risk-moderate/30 text-risk-moderate',
  High: 'from-risk-high/20 to-transparent border-risk-high/30 text-risk-high',
  Extreme: 'from-risk-extreme/20 to-transparent border-risk-extreme/30 text-risk-extreme',
}

export default function OverallRisk({ severity, address }) {
  if (!severity) return null

  return (
    <div
      className={`animate-fade-in-up p-4 rounded-xl border bg-gradient-to-r ${SEVERITY_STYLES[severity]}`}
    >
      <div className="flex items-center gap-3">
        <ShieldAlert className="w-8 h-8" />
        <div>
          <p className="text-xs text-text-secondary uppercase tracking-wider">Overall Risk Level</p>
          <p className="text-2xl font-bold">{severity}</p>
          {address && (
            <p className="text-xs text-text-secondary mt-0.5 truncate max-w-xs">{address}</p>
          )}
        </div>
      </div>
      <div className="flex items-start gap-2 mt-3 p-2.5 rounded-lg bg-amber-500/10 border border-amber-500/20">
        <AlertTriangle className="w-4 h-4 text-amber-400 mt-0.5 shrink-0" />
        <p className="text-xs text-amber-200/80 leading-relaxed">
          <span className="font-semibold text-amber-300">Disclaimer:</span> Risk scores are regional estimates based on state and county-level data from FEMA, USGS, and NOAA. They do not account for property-specific factors such as elevation, construction type, or local drainage infrastructure.
        </p>
      </div>
    </div>
  )
}
