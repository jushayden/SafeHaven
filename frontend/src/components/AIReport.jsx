import { useState, useEffect } from 'react'
import { Sparkles, ChevronDown, ChevronUp, Loader2, Brain, Shield, ClipboardList } from 'lucide-react'
import Markdown from 'react-markdown'

const LOADING_STEPS = [
  { icon: Brain, text: 'Analyzing hazard data...' },
  { icon: Shield, text: 'Evaluating risk factors...' },
  { icon: ClipboardList, text: 'Generating safety recommendations...' },
  { icon: Sparkles, text: 'Finalizing your personalized report...' },
]

function LoadingAnimation() {
  const [step, setStep] = useState(0)

  useEffect(() => {
    const timer = setInterval(() => {
      setStep((s) => (s + 1) % LOADING_STEPS.length)
    }, 2000)
    return () => clearInterval(timer)
  }, [])

  const current = LOADING_STEPS[step]
  const Icon = current.icon

  return (
    <div className="flex flex-col items-center gap-4 py-10">
      <div className="relative">
        <div className="w-14 h-14 rounded-full bg-accent/10 flex items-center justify-center animate-pulse-glow">
          <Icon className="w-7 h-7 text-accent" />
        </div>
        <div className="absolute inset-0 rounded-full border-2 border-accent/20 animate-spin" style={{ borderTopColor: '#10b981', animationDuration: '2s' }} />
      </div>
      <div className="text-center">
        <p className="text-sm text-text-primary font-medium">{current.text}</p>
        <div className="flex gap-1 justify-center mt-2">
          {LOADING_STEPS.map((_, i) => (
            <div
              key={i}
              className={`w-1.5 h-1.5 rounded-full transition-colors duration-300 ${
                i === step ? 'bg-accent' : 'bg-bg-tertiary'
              }`}
            />
          ))}
        </div>
      </div>
    </div>
  )
}

export default function AIReport({ report, isLoading }) {
  const [isExpanded, setIsExpanded] = useState(true)
  const [displayedText, setDisplayedText] = useState('')
  const [isTyping, setIsTyping] = useState(false)

  useEffect(() => {
    if (!report) {
      setDisplayedText('')
      return
    }

    setIsTyping(true)
    setDisplayedText('')

    // Stream in chunks of words for smoother effect with markdown
    const words = report.split(/(\s+)/)
    let wordIndex = 0
    const interval = setInterval(() => {
      const chunkSize = 3
      if (wordIndex < words.length) {
        wordIndex = Math.min(wordIndex + chunkSize, words.length)
        setDisplayedText(words.slice(0, wordIndex).join(''))
      } else {
        setIsTyping(false)
        clearInterval(interval)
      }
    }, 30)

    return () => clearInterval(interval)
  }, [report])

  return (
    <div className="animate-fade-in-up bg-bg-secondary border border-white/5 rounded-xl overflow-hidden" style={{ animationDelay: '400ms' }}>
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full px-4 py-3 flex items-center justify-between hover:bg-bg-tertiary/30 transition-colors"
      >
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-accent/15 text-accent">
            <Sparkles className="w-4 h-4" />
          </div>
          <span className="font-semibold text-sm">AI Safety Report</span>
          {isLoading && (
            <span className="flex items-center gap-1 text-xs text-accent">
              <Loader2 className="w-3 h-3 animate-spin" />
              Analyzing...
            </span>
          )}
          {isTyping && !isLoading && (
            <span className="text-xs text-accent">Generating...</span>
          )}
        </div>
        {isExpanded ? (
          <ChevronUp className="w-4 h-4 text-text-secondary" />
        ) : (
          <ChevronDown className="w-4 h-4 text-text-secondary" />
        )}
      </button>

      {isExpanded && (
        <div className="px-4 pb-4">
          {isLoading ? (
            <LoadingAnimation />
          ) : displayedText ? (
            <div className="ai-report-content">
              <Markdown
                components={{
                  h1: ({ children }) => <h2 className="text-base font-bold text-text-primary mt-4 mb-2 first:mt-0">{children}</h2>,
                  h2: ({ children }) => <h3 className="text-sm font-bold text-text-primary mt-4 mb-2 first:mt-0">{children}</h3>,
                  h3: ({ children }) => <h4 className="text-sm font-semibold text-text-primary mt-3 mb-1">{children}</h4>,
                  p: ({ children }) => <p className="text-sm text-text-secondary leading-relaxed mb-2">{children}</p>,
                  ul: ({ children }) => <ul className="text-sm text-text-secondary space-y-1 mb-3 ml-4 list-disc">{children}</ul>,
                  ol: ({ children }) => <ol className="text-sm text-text-secondary space-y-1 mb-3 ml-4 list-decimal">{children}</ol>,
                  li: ({ children }) => <li className="leading-relaxed">{children}</li>,
                  strong: ({ children }) => <strong className="text-text-primary font-semibold">{children}</strong>,
                  em: ({ children }) => <em className="text-text-secondary italic">{children}</em>,
                  hr: () => <hr className="border-white/10 my-3" />,
                  a: ({ href, children }) => (
                    <a href={href} target="_blank" rel="noopener noreferrer" className="text-accent hover:underline">
                      {children}
                    </a>
                  ),
                }}
              >
                {displayedText}
              </Markdown>
              {isTyping && <span className="inline-block w-1.5 h-4 bg-accent animate-pulse ml-0.5 align-middle" />}
            </div>
          ) : (
            <p className="text-sm text-text-secondary py-4 text-center">
              Search an address to generate an AI safety report.
            </p>
          )}
        </div>
      )}
    </div>
  )
}
