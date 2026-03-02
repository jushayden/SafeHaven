import { CloudLightning, Waves, Mountain, Flame } from 'lucide-react'

const ICONS = {
  hurricane: CloudLightning,
  flood: Waves,
  earthquake: Mountain,
  wildfire: Flame,
}

const SEVERITY_COLORS = {
  Low: 'bg-risk-low/15 text-risk-low border-risk-low/30',
  Moderate: 'bg-risk-moderate/15 text-risk-moderate border-risk-moderate/30',
  High: 'bg-risk-high/15 text-risk-high border-risk-high/30',
  Extreme: 'bg-risk-extreme/15 text-risk-extreme border-risk-extreme/30',
}

const BAR_COLORS = {
  Low: 'bg-risk-low',
  Moderate: 'bg-risk-moderate',
  High: 'bg-risk-high',
  Extreme: 'bg-risk-extreme',
}

const LABELS = {
  hurricane: 'Hurricane',
  flood: 'Flood',
  earthquake: 'Earthquake',
  wildfire: 'Wildfire',
}

export default function RiskCard({ type, data, delay = 0 }) {
  const Icon = ICONS[type]
  const { score, severity, description } = data

  return (
    <div
      className="animate-fade-in-up bg-bg-secondary border border-white/5 rounded-xl p-4 hover:border-white/10 transition-all"
      style={{ animationDelay: `${delay}ms` }}
    >
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <div className={`p-2 rounded-lg ${SEVERITY_COLORS[severity]}`}>
            <Icon className="w-4 h-4" />
          </div>
          <span className="font-semibold text-sm">{LABELS[type]}</span>
        </div>
        <span className={`text-xs font-bold px-2 py-0.5 rounded-full border ${SEVERITY_COLORS[severity]}`}>
          {severity}
        </span>
      </div>

      <div className="mb-2">
        <div className="flex justify-between text-xs text-text-secondary mb-1">
          <span>Risk Score</span>
          <span className="font-mono">{score}/100</span>
        </div>
        <div className="w-full h-2 bg-bg-tertiary rounded-full overflow-hidden">
          <div
            className={`h-full rounded-full transition-all duration-1000 ease-out ${BAR_COLORS[severity]}`}
            style={{ width: `${score}%` }}
          />
        </div>
      </div>

      <p className="text-xs text-text-secondary leading-relaxed">{description}</p>
    </div>
  )
}
