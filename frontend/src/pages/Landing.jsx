import { useNavigate } from 'react-router-dom'
import { Shield, CloudLightning, Waves, Mountain, Flame, MapPin, Sparkles, ArrowRight, ChevronRight, Database, Zap } from 'lucide-react'

const HAZARDS = [
  { icon: CloudLightning, label: 'Hurricanes', color: 'text-blue-400', bg: 'bg-blue-500/10 border-blue-500/20' },
  { icon: Waves, label: 'Floods', color: 'text-cyan-400', bg: 'bg-cyan-500/10 border-cyan-500/20' },
  { icon: Mountain, label: 'Earthquakes', color: 'text-amber-400', bg: 'bg-amber-500/10 border-amber-500/20' },
  { icon: Flame, label: 'Wildfires', color: 'text-red-400', bg: 'bg-red-500/10 border-red-500/20' },
]

const FEATURES = [
  {
    icon: MapPin,
    title: 'Multi-Hazard Risk Profile',
    desc: 'Get risk scores for hurricanes, floods, earthquakes, and wildfires based on FEMA, USGS, and NOAA data.',
  },
  {
    icon: Sparkles,
    title: 'AI Safety Report',
    desc: 'Gemini AI generates a personalized preparedness plan with actionable steps tailored to your location.',
  },
  {
    icon: Shield,
    title: 'Emergency Resources',
    desc: 'Find nearby shelters, hospitals, and fire stations. Access state-level emergency contacts instantly.',
  },
]

const STEPS = [
  { num: '01', title: 'Enter Your Address', desc: 'Type any U.S. address to begin your risk assessment.', icon: MapPin },
  { num: '02', title: 'Analyze Risk Data', desc: 'We pull from FEMA, USGS, and NOAA to build your profile.', icon: Database },
  { num: '03', title: 'Get Your Report', desc: 'Receive an AI-generated safety plan tailored to your area.', icon: Zap },
]

export default function Landing() {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-bg-primary">
      {/* Nav */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-bg-primary/80 backdrop-blur-md border-b border-white/5">
        <div className="max-w-6xl mx-auto px-6 h-14 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 rounded-lg overflow-hidden shrink-0">
              <img src="/icons/logo-bg.png" alt="SafeHaven" className="w-[170%] h-[170%] object-cover -ml-[35%] -mt-[35%]" />
            </div>
            <span className="text-base font-bold text-text-primary tracking-tight">
              Safe<span className="text-accent">Haven</span>
            </span>
          </div>
          <button
            onClick={() => navigate('/dashboard')}
            className="text-sm text-text-secondary hover:text-text-primary transition-colors flex items-center gap-1"
          >
            Open Dashboard
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </nav>

      {/* Hero */}
      <section className="relative overflow-hidden pt-14">
        {/* Background effects */}
        <div className="absolute inset-0">
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[600px] bg-accent/[0.03] rounded-full blur-3xl" />
          <div className="absolute top-40 left-1/4 w-[300px] h-[300px] bg-blue-500/[0.02] rounded-full blur-3xl" />
          <div className="absolute top-60 right-1/4 w-[300px] h-[300px] bg-red-500/[0.02] rounded-full blur-3xl" />
        </div>

        <div className="relative max-w-4xl mx-auto px-6 pt-24 pb-20 text-center">
          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-extrabold text-text-primary leading-[1.1] mb-6 tracking-tight">
            Know Your Risk.
            <br />
            <span className="bg-gradient-to-r from-accent to-teal-400 bg-clip-text text-transparent">
              Protect Your Home.
            </span>
          </h1>

          <p className="text-lg sm:text-xl text-text-secondary max-w-2xl mx-auto mb-10 leading-relaxed">
            Comprehensive disaster risk profiles for any U.S. address — powered by
            federal hazard data and AI-driven safety planning.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <button
              onClick={() => navigate('/dashboard')}
              className="inline-flex items-center gap-2.5 px-8 py-4 rounded-xl bg-accent hover:bg-accent-hover text-white font-semibold text-base transition-all shadow-lg shadow-accent/25 hover:shadow-accent/40 hover:scale-[1.02] active:scale-[0.98]"
            >
              Check Your Address
              <ArrowRight className="w-5 h-5" />
            </button>
            <span className="text-sm text-text-secondary">Free &middot; No signup required</span>
          </div>

          {/* Hazard cards */}
          <div className="flex flex-wrap justify-center gap-3 mt-14">
            {HAZARDS.map(({ icon: Icon, label, color, bg }) => (
              <div key={label} className={`flex items-center gap-2.5 px-4 py-2.5 rounded-lg border ${bg}`}>
                <Icon className={`w-4 h-4 ${color}`} />
                <span className={`text-sm font-medium ${color}`}>{label}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="max-w-5xl mx-auto px-6 py-20">
        <div className="text-center mb-12">
          <p className="text-xs font-semibold text-accent uppercase tracking-widest mb-2">How It Works</p>
          <h2 className="text-2xl sm:text-3xl font-bold text-text-primary">Three steps to safety</h2>
        </div>
        <div className="grid sm:grid-cols-3 gap-6">
          {STEPS.map(({ num, title, desc, icon: Icon }) => (
            <div key={num} className="relative p-6 rounded-xl bg-bg-secondary/60 border border-white/5 hover:border-white/10 transition-colors group">
              <div className="flex items-center gap-3 mb-3">
                <span className="text-xs font-bold text-accent/50">{num}</span>
                <div className="p-1.5 rounded-lg bg-accent/10 text-accent">
                  <Icon className="w-4 h-4" />
                </div>
              </div>
              <h3 className="text-sm font-semibold text-text-primary mb-1">{title}</h3>
              <p className="text-xs text-text-secondary leading-relaxed">{desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Features */}
      <section className="max-w-5xl mx-auto px-6 pb-20">
        <div className="text-center mb-12">
          <p className="text-xs font-semibold text-accent uppercase tracking-widest mb-2">Features</p>
          <h2 className="text-2xl sm:text-3xl font-bold text-text-primary">Everything you need to prepare</h2>
        </div>
        <div className="grid sm:grid-cols-3 gap-5">
          {FEATURES.map(({ icon: Icon, title, desc }) => (
            <div key={title} className="p-6 rounded-xl bg-bg-secondary border border-white/5 hover:border-accent/20 transition-all hover:shadow-lg hover:shadow-accent/5 group">
              <div className="p-2.5 rounded-lg bg-accent/10 text-accent w-fit mb-4 group-hover:bg-accent/15 transition-colors">
                <Icon className="w-5 h-5" />
              </div>
              <h3 className="text-sm font-semibold text-text-primary mb-2">{title}</h3>
              <p className="text-xs text-text-secondary leading-relaxed">{desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Data sources + SDG badge */}
      <section className="max-w-5xl mx-auto px-6 pb-20">
        <div className="grid sm:grid-cols-2 gap-4">
          <div className="p-5 rounded-xl bg-bg-secondary/50 border border-white/5 flex items-center gap-4">
            <Database className="w-5 h-5 text-text-secondary shrink-0" />
            <div>
              <p className="text-xs font-medium text-text-primary mb-1">Federal Data Sources</p>
              <p className="text-[11px] text-text-secondary">
                FEMA &middot; USGS &middot; NOAA &middot; Google Maps &middot; Gemini AI
              </p>
            </div>
          </div>
          <a
            href="https://sdgs.un.org/goals/goal11"
            target="_blank"
            rel="noopener noreferrer"
            className="p-5 rounded-xl bg-accent/5 border border-accent/15 hover:border-accent/30 transition-colors flex items-center gap-4 no-underline group"
          >
            <div className="p-2 rounded-lg bg-accent/10">
              <Shield className="w-5 h-5 text-accent" />
            </div>
            <div>
              <p className="text-xs font-medium text-accent mb-0.5">UN SDG 11</p>
              <p className="text-[11px] text-text-secondary">
                Sustainable Cities & Communities
              </p>
            </div>
            <ChevronRight className="w-4 h-4 text-accent/50 ml-auto group-hover:translate-x-0.5 transition-transform" />
          </a>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/5 py-6">
        <div className="max-w-5xl mx-auto px-6 flex flex-col sm:flex-row items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 rounded-sm overflow-hidden shrink-0 opacity-60">
              <img src="/icons/logo-bg.png" alt="" className="w-[170%] h-[170%] object-cover -ml-[35%] -mt-[35%]" />
            </div>
            <span className="text-xs text-text-secondary">
              SafeHaven — MEGA Hackathon 2026
            </span>
          </div>
          <span className="text-xs text-text-secondary">
            Designed & Developed by Hayden Jose
          </span>
        </div>
      </footer>
    </div>
  )
}
