import { Heart, ArrowLeft } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function DonationSuccess() {
  return (
    <div className="pt-14 min-h-screen flex items-center justify-center">
      <div className="text-center max-w-md px-4">
        <div className="w-16 h-16 rounded-full bg-green-500/15 border border-green-500/30 flex items-center justify-center mx-auto mb-4">
          <Heart className="w-8 h-8 text-green-400" />
        </div>
        <h1 className="text-2xl font-bold mb-2">Thank You!</h1>
        <p className="text-text-secondary mb-6">
          Your donation will help disaster relief organizations like the Red Cross and Direct Relief
          support communities in need.
        </p>
        <Link
          to="/"
          className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-accent hover:bg-accent-hover text-white transition-colors no-underline"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Dashboard
        </Link>
      </div>
    </div>
  )
}
