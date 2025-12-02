"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { useRouter } from "next/navigation"

interface SignupFormProps {
  onToggle: () => void
}

export function SignupForm({ onToggle }: SignupFormProps) {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const router = useRouter()

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!formData.name || !formData.email || !formData.password) {
      setError("Please fill in all fields")
      return
    }
    
    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match")
      return
    }
    
    setLoading(true)
    setError("")
    
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/signup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: formData.name,
          email: formData.email,
          password: formData.password
        }),
      })
      
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Signup failed')
      }
      
      // Auto-login after successful signup
      const loginFormData = new FormData()
      loginFormData.append('username', formData.email)
      loginFormData.append('password', formData.password)
      
      const loginResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/login`, {
        method: 'POST',
        body: loginFormData,
      })
      
      if (loginResponse.ok) {
        const loginData = await loginResponse.json()
        localStorage.setItem('token', loginData.access_token)
        
        // Store user info
        localStorage.setItem('user', JSON.stringify({
          email: formData.email,
          name: formData.name
        }))
        
        router.push('/dashboard')
      } else {
        onToggle() // Switch to login form
      }
    } catch (err: any) {
      setError(err.message || 'Signup failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-bold text-white">Join Bible GPT</h1>
        <p className="text-white/70">Create account to start your journey</p>
      </div>

      {/* Form */}
      <form onSubmit={handleSubmit} className="space-y-4">
        {error && (
          <div className="bg-red-500/20 border border-red-500/50 rounded-lg p-3 text-red-200 text-sm">
            {error}
          </div>
        )}
        
        <div className="space-y-2">
          <label htmlFor="name" className="text-sm font-medium text-white/90">Full Name</label>
          <Input
            id="name"
            type="text"
            name="name"
            placeholder="John Doe"
            value={formData.name}
            onChange={handleChange}
            className="bg-white/10 border-white/20 text-white placeholder:text-white/50"
            required
          />
        </div>

        <div className="space-y-2">
          <label htmlFor="email" className="text-sm font-medium text-white/90">Email</label>
          <Input
            id="email"
            type="email"
            name="email"
            placeholder="you@example.com"
            value={formData.email}
            onChange={handleChange}
            className="bg-white/10 border-white/20 text-white placeholder:text-white/50"
            required
          />
        </div>

        <div className="space-y-2">
          <label htmlFor="password" className="text-sm font-medium text-white/90">Password</label>
          <Input
            id="password"
            type="password"
            name="password"
            placeholder="••••••••"
            value={formData.password}
            onChange={handleChange}
            className="bg-white/10 border-white/20 text-white placeholder:text-white/50"
            required
          />
        </div>

        <div className="space-y-2">
          <label htmlFor="confirmPassword" className="text-sm font-medium text-white/90">Confirm Password</label>
          <Input
            id="confirmPassword"
            type="password"
            name="confirmPassword"
            placeholder="••••••••"
            value={formData.confirmPassword}
            onChange={handleChange}
            className="bg-white/10 border-white/20 text-white placeholder:text-white/50"
            required
          />
        </div>

        <Button
          type="submit"
          disabled={loading}
          className="w-full bg-indigo-500 hover:bg-indigo-600 text-white font-semibold py-2 rounded-lg transition-all duration-200"
        >
          {loading ? "Creating Account..." : "Sign Up"}
        </Button>
      </form>

      {/* Divider */}
      <div className="relative">
        <div className="absolute inset-0 flex items-center">
          <div className="w-full border-t border-white/20"></div>
        </div>
        <div className="relative flex justify-center text-sm">
          <span className="px-2 bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white/70">
            Already have an account?
          </span>
        </div>
      </div>

      {/* Login link */}
      <button
        onClick={onToggle}
        className="w-full py-2 px-4 rounded-lg border border-white/20 text-white hover:bg-white/5 transition-all duration-200"
      >
        Sign In Instead
      </button>
    </div>
  )
}
