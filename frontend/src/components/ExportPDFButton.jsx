import { useState } from 'react'
import { FileDown, Loader2 } from 'lucide-react'
import { exportPDF } from '../services/api'

export default function ExportPDFButton({ riskProfile, aiReport, address }) {
  const [isLoading, setIsLoading] = useState(false)

  const handleExport = async () => {
    if (!riskProfile) return
    setIsLoading(true)
    try {
      const blob = await exportPDF({
        address,
        risk_profile: riskProfile,
        ai_report: aiReport || 'No AI report generated.',
      })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `SafeHaven_Report_${Date.now()}.pdf`
      a.click()
      window.URL.revokeObjectURL(url)
    } catch (err) {
      console.error('PDF export error:', err)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <button
      onClick={handleExport}
      disabled={isLoading || !riskProfile}
      className="flex items-center gap-2 px-3 py-2 rounded-lg bg-bg-tertiary hover:bg-bg-tertiary/80 text-text-secondary hover:text-text-primary text-sm transition-colors disabled:opacity-40 disabled:cursor-not-allowed border border-white/5"
    >
      {isLoading ? (
        <Loader2 className="w-4 h-4 animate-spin" />
      ) : (
        <FileDown className="w-4 h-4" />
      )}
      Export PDF
    </button>
  )
}
