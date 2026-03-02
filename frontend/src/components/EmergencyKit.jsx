import { useState } from 'react'
import { Package, ChevronDown, ChevronUp, Check } from 'lucide-react'

const GENERAL_ITEMS = [
  'Water (1 gallon per person per day, 3-day supply)',
  'Non-perishable food (3-day supply)',
  'Battery-powered or hand-crank radio',
  'Flashlight with extra batteries',
  'First aid kit',
  'Whistle (to signal for help)',
  'Dust masks and plastic sheeting',
  'Moist towelettes, garbage bags, and ties',
  'Wrench or pliers (to turn off utilities)',
  'Manual can opener',
  'Local maps',
  'Cell phone with chargers and backup battery',
  'Prescription medications (7-day supply)',
  'Important documents in waterproof container',
  'Cash in small denominations',
]

const HAZARD_ITEMS = {
  hurricane: [
    'Plywood or hurricane shutters for windows',
    'Tarps and waterproof covers',
    'Extra fuel for generator (stored safely)',
    'Rain gear and waterproof boots',
    'Sandbags (if in flood zone)',
  ],
  flood: [
    'Waterproof bags for electronics and documents',
    'Rubber boots and waders',
    'Sump pump or water removal tools',
    'Inflatable raft or flotation devices',
    'Water purification tablets',
  ],
  earthquake: [
    'Heavy-duty work gloves',
    'Sturdy shoes by each bed',
    'Fire extinguisher',
    'Furniture anchoring straps',
    'Crowbar or pry bar',
  ],
  wildfire: [
    'N95 respirator masks',
    'Goggles for eye protection',
    'Long-sleeved cotton clothing',
    'Garden hose and fire-resistant materials',
    'Portable air purifier',
  ],
}

const HAZARD_LABELS = {
  hurricane: 'Hurricane',
  flood: 'Flood',
  earthquake: 'Earthquake',
  wildfire: 'Wildfire',
}

export default function EmergencyKit({ risks }) {
  const [isOpen, setIsOpen] = useState(false)
  const [checked, setChecked] = useState({})

  const activeHazards = risks
    ? Object.keys(HAZARD_ITEMS).filter((h) => risks[h] && risks[h].score > 25)
    : []

  const totalItems = GENERAL_ITEMS.length + activeHazards.reduce((sum, h) => sum + HAZARD_ITEMS[h].length, 0)
  const checkedCount = Object.values(checked).filter(Boolean).length

  const toggle = (key) => setChecked((prev) => ({ ...prev, [key]: !prev[key] }))

  return (
    <div className="rounded-xl bg-bg-secondary border border-white/5 overflow-hidden">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full p-4 flex items-center justify-between hover:bg-white/[0.02] transition-colors"
      >
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-accent/10">
            <Package className="w-5 h-5 text-accent" />
          </div>
          <div className="text-left">
            <p className="text-sm font-semibold text-text-primary">Emergency Kit Checklist</p>
            <p className="text-xs text-text-secondary">
              {checkedCount}/{totalItems} items ready
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          {checkedCount > 0 && (
            <div className="h-1.5 w-16 rounded-full bg-bg-tertiary overflow-hidden">
              <div
                className="h-full rounded-full bg-accent transition-all"
                style={{ width: `${(checkedCount / totalItems) * 100}%` }}
              />
            </div>
          )}
          {isOpen ? (
            <ChevronUp className="w-4 h-4 text-text-secondary" />
          ) : (
            <ChevronDown className="w-4 h-4 text-text-secondary" />
          )}
        </div>
      </button>

      {isOpen && (
        <div className="border-t border-white/5 p-4 space-y-4 max-h-[400px] overflow-y-auto">
          {/* General supplies */}
          <div>
            <p className="text-xs font-semibold text-text-secondary uppercase tracking-wider mb-2">
              Essential Supplies
            </p>
            <div className="space-y-1">
              {GENERAL_ITEMS.map((item) => {
                const key = `general-${item}`
                return (
                  <label key={key} className="flex items-center gap-2 py-1 px-1 cursor-pointer hover:bg-white/5 rounded group">
                    <div
                      className={`w-4 h-4 rounded border flex items-center justify-center shrink-0 transition-colors ${
                        checked[key]
                          ? 'bg-accent border-accent'
                          : 'border-white/20 group-hover:border-white/40'
                      }`}
                      onClick={(e) => { e.preventDefault(); toggle(key) }}
                    >
                      {checked[key] && <Check className="w-3 h-3 text-white" />}
                    </div>
                    <span
                      className={`text-xs leading-relaxed ${
                        checked[key] ? 'text-text-secondary line-through' : 'text-text-primary'
                      }`}
                    >
                      {item}
                    </span>
                  </label>
                )
              })}
            </div>
          </div>

          {/* Hazard-specific sections */}
          {activeHazards.map((hazard) => (
            <div key={hazard}>
              <p className="text-xs font-semibold text-text-secondary uppercase tracking-wider mb-2">
                {HAZARD_LABELS[hazard]} Supplies
              </p>
              <div className="space-y-1">
                {HAZARD_ITEMS[hazard].map((item) => {
                  const key = `${hazard}-${item}`
                  return (
                    <label key={key} className="flex items-center gap-2 py-1 px-1 cursor-pointer hover:bg-white/5 rounded group">
                      <div
                        className={`w-4 h-4 rounded border flex items-center justify-center shrink-0 transition-colors ${
                          checked[key]
                            ? 'bg-accent border-accent'
                            : 'border-white/20 group-hover:border-white/40'
                        }`}
                        onClick={(e) => { e.preventDefault(); toggle(key) }}
                      >
                        {checked[key] && <Check className="w-3 h-3 text-white" />}
                      </div>
                      <span
                        className={`text-xs leading-relaxed ${
                          checked[key] ? 'text-text-secondary line-through' : 'text-text-primary'
                        }`}
                      >
                        {item}
                      </span>
                    </label>
                  )
                })}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
