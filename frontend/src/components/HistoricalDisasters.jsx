import { useState } from 'react'
import { History, ChevronDown, ChevronUp, Loader2, Calendar, AlertCircle } from 'lucide-react'
import { getHistoricalDisasters } from '../services/api'

const TYPE_COLORS = {
  Hurricane: 'bg-blue-500/15 text-blue-400',
  Flood: 'bg-cyan-500/15 text-cyan-400',
  'Severe Storm': 'bg-purple-500/15 text-purple-400',
  'Severe Storm(s)': 'bg-purple-500/15 text-purple-400',
  Fire: 'bg-red-500/15 text-red-400',
  Earthquake: 'bg-amber-500/15 text-amber-400',
  Tornado: 'bg-violet-500/15 text-violet-400',
  'Snow': 'bg-slate-400/15 text-slate-300',
  'Severe Ice Storm': 'bg-slate-400/15 text-slate-300',
  'Coastal Storm': 'bg-teal-500/15 text-teal-400',
  'Tropical Storm': 'bg-blue-500/15 text-blue-400',
  'Typhoon': 'bg-blue-500/15 text-blue-400',
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
}

export default function HistoricalDisasters({ state }) {
  const [isOpen, setIsOpen] = useState(false)
  const [disasters, setDisasters] = useState([])
  const [loading, setLoading] = useState(false)
  const [loaded, setLoaded] = useState(false)

  const handleOpen = async () => {
    if (isOpen) {
      setIsOpen(false)
      return
    }
    setIsOpen(true)
    if (!loaded) {
      setLoading(true)
      try {
        const data = await getHistoricalDisasters(state)
        setDisasters(data.disasters || [])
      } catch {
        setDisasters([])
      } finally {
        setLoading(false)
        setLoaded(true)
      }
    }
  }

  return (
    <div className="rounded-xl bg-bg-secondary border border-white/5 overflow-hidden">
      <button
        onClick={handleOpen}
        className="w-full p-4 flex items-center justify-between hover:bg-white/[0.02] transition-colors"
      >
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-accent/10">
            <History className="w-5 h-5 text-accent" />
          </div>
          <div className="text-left">
            <p className="text-sm font-semibold text-text-primary">Historical Disasters</p>
            <p className="text-xs text-text-secondary">
              FEMA-declared disasters in {state}
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
              <span>Loading disaster history...</span>
            </div>
          ) : disasters.length === 0 ? (
            <div className="p-6 text-center text-text-secondary text-sm">
              No FEMA disaster declarations found for {state}.
            </div>
          ) : (
            <div className="max-h-[400px] overflow-y-auto">
              {/* Summary stats */}
              <div className="px-4 py-3 bg-white/[0.02] border-b border-white/5 flex items-center gap-4">
                <div className="text-center">
                  <p className="text-lg font-bold text-text-primary">{disasters.length}</p>
                  <p className="text-[10px] text-text-secondary uppercase">Total Disasters</p>
                </div>
                <div className="h-8 w-px bg-white/10" />
                <div className="flex flex-wrap gap-1.5">
                  {(() => {
                    const counts = {}
                    disasters.forEach((d) => { counts[d.type] = (counts[d.type] || 0) + 1 })
                    return Object.entries(counts)
                      .sort((a, b) => b[1] - a[1])
                      .slice(0, 4)
                      .map(([type, count]) => (
                        <span
                          key={type}
                          className={`text-[10px] px-2 py-0.5 rounded-full font-medium ${TYPE_COLORS[type] || 'bg-gray-500/15 text-gray-400'}`}
                        >
                          {type}: {count}
                        </span>
                      ))
                  })()}
                </div>
              </div>

              {/* Timeline */}
              <div className="p-4 space-y-0">
                {disasters.slice(0, 30).map((d, i) => (
                  <div key={d.disaster_number} className="flex gap-3 group">
                    {/* Timeline line + dot */}
                    <div className="flex flex-col items-center">
                      <div className={`w-2.5 h-2.5 rounded-full shrink-0 mt-1 ${
                        i === 0 ? 'bg-accent' : 'bg-bg-tertiary group-hover:bg-text-secondary'
                      } transition-colors`} />
                      {i < disasters.slice(0, 30).length - 1 && (
                        <div className="w-px flex-1 bg-white/10 my-1" />
                      )}
                    </div>

                    {/* Content */}
                    <div className="pb-4 min-w-0 flex-1">
                      <p className="text-xs font-semibold text-text-primary leading-tight">
                        {d.title}
                      </p>
                      <div className="flex items-center gap-2 mt-1 flex-wrap">
                        <span
                          className={`text-[10px] px-1.5 py-0.5 rounded font-medium ${
                            TYPE_COLORS[d.type] || 'bg-gray-500/15 text-gray-400'
                          }`}
                        >
                          {d.type}
                        </span>
                        <span className="text-[10px] text-text-secondary flex items-center gap-0.5">
                          <Calendar className="w-2.5 h-2.5" />
                          {formatDate(d.declaration_date)}
                        </span>
                        <span className="text-[10px] text-text-secondary">
                          #{d.disaster_number}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
                {disasters.length > 30 && (
                  <p className="text-xs text-text-secondary text-center pt-2">
                    + {disasters.length - 30} more declarations
                  </p>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
