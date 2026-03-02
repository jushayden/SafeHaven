import { Component } from 'react'

export default class ErrorBoundary extends Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  componentDidCatch(error, info) {
    console.error('ErrorBoundary caught:', error, info.componentStack)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="p-4 m-4 rounded-lg bg-red-500/10 border border-red-500/30">
          <p className="text-red-400 font-semibold text-sm mb-1">Something crashed</p>
          <pre className="text-xs text-red-300 whitespace-pre-wrap break-words">
            {this.state.error?.message || 'Unknown error'}
          </pre>
          <button
            onClick={() => this.setState({ hasError: false, error: null })}
            className="mt-2 text-xs text-accent hover:underline"
          >
            Try again
          </button>
        </div>
      )
    }
    return this.props.children
  }
}
