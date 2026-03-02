import { ShieldAlert, AlertTriangle, Mountain, Navigation, Users, Building2, TreePine } from 'lucide-react'

const SEVERITY_STYLES = {
  Low: 'from-risk-low/20 to-transparent border-risk-low/30 text-risk-low',
  Moderate: 'from-risk-moderate/20 to-transparent border-risk-moderate/30 text-risk-moderate',
  High: 'from-risk-high/20 to-transparent border-risk-high/30 text-risk-high',
  Extreme: 'from-risk-extreme/20 to-transparent border-risk-extreme/30 text-risk-extreme',
}

export default function OverallRisk({ severity, address, locationFactors }) {
  if (!severity) return null

  const elev = locationFactors?.elevation
  const coast = locationFactors?.coast_proximity
  const density = locationFactors?.population_density
  const building = locationFactors?.building_age
  const whp = locationFactors?.wildfire_vegetation

  const hasFactors = elev?.elevation_ft != null || coast?.coast_distance_miles != null || density?.density_per_sq_mile != null || building?.median_era != null || (whp?.whp_class != null && whp?.whp_class !== 'Unknown')

  return (
    <div
      className={`animate-fade-in-up p-4 rounded-xl border bg-gradient-to-r ${SEVERITY_STYLES[severity]}`}
    >
      <div className="flex items-center gap-3">
        <ShieldAlert className="w-8 h-8" />
        <div>
          <p className="text-xs text-text-secondary uppercase tracking-wider">Overall Risk Level</p>
          <p className="text-2xl font-bold">{severity}</p>
          {address && (
            <p className="text-xs text-text-secondary mt-0.5 truncate max-w-xs">{address}</p>
          )}
        </div>
      </div>

      {/* Location factors */}
      {hasFactors && (
        <div className="mt-3 grid grid-cols-3 gap-2">
          {elev?.elevation_ft != null && (
            <div className="p-2 rounded-lg bg-white/5 border border-white/5 text-center">
              <Mountain className="w-3.5 h-3.5 text-text-secondary mx-auto mb-1" />
              <p className="text-sm font-bold text-text-primary">{Math.round(elev.elevation_ft)} ft</p>
              <p className="text-[10px] text-text-secondary">Elevation</p>
            </div>
          )}
          {coast?.coast_distance_miles != null && (
            <div className="p-2 rounded-lg bg-white/5 border border-white/5 text-center">
              <Navigation className="w-3.5 h-3.5 text-text-secondary mx-auto mb-1" />
              <p className="text-sm font-bold text-text-primary">{Math.round(coast.coast_distance_miles)} mi</p>
              <p className="text-[10px] text-text-secondary">To Coast</p>
            </div>
          )}
          {density?.density_per_sq_mile != null && (
            <div className="p-2 rounded-lg bg-white/5 border border-white/5 text-center">
              <Users className="w-3.5 h-3.5 text-text-secondary mx-auto mb-1" />
              <p className="text-sm font-bold text-text-primary">{density.density_per_sq_mile >= 1000 ? `${(density.density_per_sq_mile / 1000).toFixed(1)}k` : Math.round(density.density_per_sq_mile)}</p>
              <p className="text-[10px] text-text-secondary">Pop/mi²</p>
            </div>
          )}
          {building?.median_era != null && (
            <div className="p-2 rounded-lg bg-white/5 border border-white/5 text-center">
              <Building2 className="w-3.5 h-3.5 text-text-secondary mx-auto mb-1" />
              <p className="text-sm font-bold text-text-primary">{building.median_era}</p>
              <p className="text-[10px] text-text-secondary">Bldg Era</p>
            </div>
          )}
          {whp?.whp_class != null && whp.whp_class !== 'Unknown' && (
            <div className="p-2 rounded-lg bg-white/5 border border-white/5 text-center">
              <TreePine className="w-3.5 h-3.5 text-text-secondary mx-auto mb-1" />
              <p className="text-sm font-bold text-text-primary">{whp.whp_class}</p>
              <p className="text-[10px] text-text-secondary">Fire Veg</p>
            </div>
          )}
        </div>
      )}

      <div className="flex items-start gap-2 mt-3 p-2.5 rounded-lg bg-amber-500/10 border border-amber-500/20">
        <AlertTriangle className="w-4 h-4 text-amber-400 mt-0.5 shrink-0" />
        <p className="text-xs text-amber-200/80 leading-relaxed">
          <span className="font-semibold text-amber-300">Disclaimer:</span> Risk scores are estimates combining FEMA, USGS, NOAA, Census, and USFS data with location-specific factors (elevation, coast proximity, population density, building age, wildfire vegetation). They do not account for individual building construction, local drainage, or micro-terrain features.
        </p>
      </div>
    </div>
  )
}
