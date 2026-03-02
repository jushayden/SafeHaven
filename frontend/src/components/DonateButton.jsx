import { useState } from 'react'
import { Heart, Loader2 } from 'lucide-react'
import { createCheckoutSession } from '../services/api'

const AMOUNTS = [5, 10, 25, 50]

export default function DonateButton({ compact = false }) {
  const [isLoading, setIsLoading] = useState(false)
  const [selectedAmount, setSelectedAmount] = useState(10)
  const [showPicker, setShowPicker] = useState(false)

  const handleDonate = async () => {
    setIsLoading(true)
    try {
      const data = await createCheckoutSession(selectedAmount)
      if (data.url) {
        window.location.href = data.url
      }
    } catch (err) {
      console.error('Donation error:', err)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="relative">
      <button
        onClick={() => setShowPicker(!showPicker)}
        className={`flex items-center gap-2 rounded-lg bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-600 hover:to-teal-600 text-white font-medium transition-all shadow-lg shadow-emerald-500/20 hover:shadow-emerald-500/30 ${
          compact ? 'px-3 py-1.5 text-xs' : 'px-4 py-2.5 text-sm'
        }`}
      >
        <Heart className={compact ? 'w-3.5 h-3.5' : 'w-4 h-4'} />
        {compact ? 'Donate' : 'Donate to Disaster Relief'}
      </button>

      {showPicker && (
        <>
          <div className="fixed inset-0 z-40" onClick={() => setShowPicker(false)} />
          <div className="absolute top-full right-0 mt-2 w-64 bg-bg-secondary border border-white/10 rounded-xl shadow-2xl p-4 z-50">
            <p className="text-xs font-medium text-text-secondary mb-3">Select amount:</p>
            <div className="grid grid-cols-4 gap-2 mb-3">
              {AMOUNTS.map((amt) => (
                <button
                  key={amt}
                  onClick={() => setSelectedAmount(amt)}
                  className={`py-2 rounded-lg text-sm font-semibold transition-all ${
                    selectedAmount === amt
                      ? 'bg-accent text-white shadow-md shadow-accent/25'
                      : 'bg-bg-tertiary/60 text-text-secondary hover:text-text-primary hover:bg-bg-tertiary'
                  }`}
                >
                  ${amt}
                </button>
              ))}
            </div>
            <button
              onClick={handleDonate}
              disabled={isLoading}
              className="w-full py-2.5 rounded-lg bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-600 hover:to-teal-600 text-white text-sm font-semibold transition-all disabled:opacity-50 flex items-center justify-center gap-2 shadow-lg shadow-emerald-500/20"
            >
              {isLoading ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <>Donate ${selectedAmount}</>
              )}
            </button>
            <p className="text-[10px] text-text-secondary text-center mt-2">
              Proceeds go to Red Cross & Direct Relief
            </p>
          </div>
        </>
      )}
    </div>
  )
}
