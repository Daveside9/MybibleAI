import type React from "react"
export function AuthContainer({ children }: { children: React.ReactNode }) {
  return (
    <div className="backdrop-blur-md bg-white/10 border border-white/20 rounded-2xl p-8 shadow-2xl">{children}</div>
  )
}
