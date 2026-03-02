import { Link } from 'react-router-dom'
import DonateButton from './DonateButton'

export default function Header() {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-bg-primary/80 backdrop-blur-md border-b border-white/5">
      <div className="max-w-screen-2xl mx-auto px-4 h-14 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 no-underline">
          <div className="w-10 h-10 rounded-lg overflow-hidden shrink-0 flex items-center justify-center">
            <img src="/icons/logo-bg.png" alt="SafeHaven" className="w-[140%] h-[140%] object-cover" />
          </div>
          <span className="text-lg font-bold text-text-primary tracking-tight">
            Safe<span className="text-accent">Haven</span>
          </span>
        </Link>
        <DonateButton compact />
      </div>
    </header>
  )
}
