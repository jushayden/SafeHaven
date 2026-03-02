import { useState, useEffect } from 'react'
import { Phone, ExternalLink, Building2, Loader2, ChevronDown, ChevronUp } from 'lucide-react'
import { getEmergencyContacts } from '../services/api'

function flattenContacts(data) {
  if (!data?.contacts) return []
  const c = data.contacts
  const list = []

  if (Array.isArray(c.general)) {
    c.general.forEach((g) =>
      list.push({ name: g.name || g.description, phone: g.number, url: null })
    )
  }
  if (c.state_agency) {
    list.push({ name: c.state_agency.name, phone: c.state_agency.phone, url: c.state_agency.website })
  }
  if (c.fema_region) {
    list.push({ name: c.fema_region.name, phone: c.fema_region.phone, url: c.fema_region.website })
  }
  if (c.red_cross) {
    list.push({ name: c.red_cross.name, phone: c.red_cross.phone, url: c.red_cross.website })
  }
  if (c.nws) {
    list.push({ name: c.nws.name, phone: c.nws.phone || null, url: c.nws.website })
  }

  return list
}

export default function EmergencyContacts({ state }) {
  const [contacts, setContacts] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [isOpen, setIsOpen] = useState(false)

  useEffect(() => {
    if (!state) return
    setIsLoading(true)
    getEmergencyContacts(state)
      .then((data) => setContacts(flattenContacts(data)))
      .catch(() => setContacts([]))
      .finally(() => setIsLoading(false))
  }, [state])

  if (!state) return null

  return (
    <div className="rounded-xl bg-bg-secondary border border-white/5 overflow-hidden">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full p-4 flex items-center justify-between hover:bg-white/[0.02] transition-colors"
      >
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-blue-500/10">
            <Phone className="w-5 h-5 text-blue-400" />
          </div>
          <div className="text-left">
            <p className="text-sm font-semibold text-text-primary">Emergency Contacts</p>
            <p className="text-xs text-text-secondary">
              {isLoading ? 'Loading...' : `${contacts.length} contacts available`}
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
        <div className="border-t border-white/5 p-4">
          {isLoading ? (
            <div className="flex justify-center py-4">
              <Loader2 className="w-5 h-5 text-text-secondary animate-spin" />
            </div>
          ) : contacts.length > 0 ? (
            <div className="space-y-2">
              {contacts.map((c, i) => (
                <div key={i} className="flex items-start gap-2 p-2 rounded-lg hover:bg-bg-tertiary/30 transition-colors">
                  <Building2 className="w-4 h-4 text-text-secondary mt-0.5 shrink-0" />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium truncate">{c.name}</p>
                    {c.phone && (
                      <a href={`tel:${c.phone}`} className="text-xs text-accent hover:underline">
                        {c.phone}
                      </a>
                    )}
                    {c.url && (
                      <a
                        href={c.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-1 text-xs text-text-secondary hover:text-accent mt-0.5"
                      >
                        <ExternalLink className="w-3 h-3" />
                        Visit website
                      </a>
                    )}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-text-secondary text-center py-2">
              No contacts available.
            </p>
          )}
        </div>
      )}
    </div>
  )
}
