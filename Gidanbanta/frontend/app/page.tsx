import Link from 'next/link'

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-navy">
      {/* Hero Section */}
      <section className="relative overflow-hidden min-h-[600px] md:min-h-[700px]">
        {/* Background Images - Messi and Ronaldo */}
        <div className="absolute inset-0 flex">
          {/* Messi Side */}
          <div className="w-1/2 relative">
            <div 
              className="absolute inset-0 bg-cover bg-center bg-no-repeat"
              style={{
                backgroundImage: "url('https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=800&q=80')",
                filter: "brightness(0.4)"
              }}
            ></div>
            <div className="absolute inset-0 bg-gradient-to-r from-transparent to-navy/80"></div>
          </div>
          
          {/* Ronaldo Side */}
          <div className="w-1/2 relative">
            <div 
              className="absolute inset-0 bg-cover bg-center bg-no-repeat"
              style={{
                backgroundImage: "url('https://images.unsplash.com/photo-1606925797300-0b35e9d1794e?w=800&q=80')",
                filter: "brightness(0.4)"
              }}
            ></div>
            <div className="absolute inset-0 bg-gradient-to-l from-transparent to-navy/80"></div>
          </div>
        </div>

        {/* Overlay gradient */}
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-navy/60 to-navy"></div>
        
        {/* Content */}
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 md:py-32">
          <div className="text-center">
            <h1 className="text-5xl md:text-7xl font-heading font-bold text-white mb-6 drop-shadow-2xl">
              Watch Live. Banter Loud.
            </h1>
            <p className="text-xl md:text-2xl text-white mb-8 max-w-3xl mx-auto drop-shadow-lg">
              Join the ultimate match viewing experience with live chat, camera reactions, and fantasy football.
            </p>
            <p className="text-lg md:text-xl text-cyan font-bold mb-10 drop-shadow-lg">
              Only ₦100 to unlock chat per match
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link 
                href="/signup"
                className="px-8 py-4 bg-primary hover:bg-primary-600 text-white rounded-lg text-lg font-semibold transition-all transform hover:scale-105 shadow-2xl"
              >
                Get Started
              </Link>
              <Link 
                href="#how-it-works"
                className="px-8 py-4 border-2 border-white text-white hover:bg-white/10 rounded-lg text-lg font-semibold transition-all shadow-2xl backdrop-blur-sm"
              >
                How It Works
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section id="how-it-works" className="py-20 bg-navy-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl font-heading font-bold text-center text-text-primary mb-16">
            How It Works
          </h2>
          
          <div className="grid md:grid-3 gap-8">
            <div className="bg-navy-100 p-8 rounded-card">
              <div className="w-16 h-16 bg-primary rounded-full flex items-center justify-center text-2xl font-bold mb-4">
                1
              </div>
              <h3 className="text-2xl font-semibold mb-4">Sign Up & Verify</h3>
              <p className="text-text-muted">
                Create your account, verify your age (18+), and get 3 free messages per match.
              </p>
            </div>

            <div className="bg-navy-100 p-8 rounded-card">
              <div className="w-16 h-16 bg-cyan rounded-full flex items-center justify-center text-2xl font-bold mb-4">
                2
              </div>
              <h3 className="text-2xl font-semibold mb-4">Join Match Rooms</h3>
              <p className="text-text-muted">
                Watch live streams, chat with fans, send camera reactions, and compete in fantasy leagues.
              </p>
            </div>

            <div className="bg-navy-100 p-8 rounded-card">
              <div className="w-16 h-16 bg-success rounded-full flex items-center justify-center text-2xl font-bold mb-4">
                3
              </div>
              <h3 className="text-2xl font-semibold mb-4">Unlock & Win</h3>
              <p className="text-muted">
                Top up with ₦100 to unlock unlimited chat. Win virtual credits through fantasy contests!
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl font-heading font-bold text-center text-text-primary mb-16">
            Simple Pricing
          </h2>
          
          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            <div className="bg-navy-100 p-8 rounded-card border-2 border-transparent hover:border-primary transition-all">
              <h3 className="text-2xl font-semibold mb-4">Free Access</h3>
              <div className="text-4xl font-bold mb-6">₦0</div>
              <ul className="space-y-3 text-text-muted mb-8">
                <li>✓ Watch all live matches</li>
                <li>✓ 3 free messages per match</li>
                <li>✓ View reactions & chat</li>
                <li>✓ Free fantasy leagues</li>
              </ul>
            </div>

            <div className="bg-gradient-to-br from-primary/20 to-cyan/10 p-8 rounded-card border-2 border-primary">
              <div className="bg-primary text-white px-3 py-1 rounded-full text-sm inline-block mb-4">
                Popular
              </div>
              <h3 className="text-2xl font-semibold mb-4">Per-Match Unlock</h3>
              <div className="text-4xl font-bold mb-6">₦100<span className="text-lg text-text-muted">/match</span></div>
              <ul className="space-y-3 text-text-muted mb-8">
                <li>✓ Everything in Free</li>
                <li>✓ Unlimited chat for the match</li>
                <li>✓ Send camera reactions</li>
                <li>✓ Paid fantasy contests</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Payment Partners */}
      <section className="py-20 bg-navy-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-heading font-bold text-text-primary mb-8">
            Supported Payment Partners
          </h2>
          <div className="flex flex-wrap justify-center gap-8 items-center">
            <div className="text-2xl font-bold text-text-muted">Opay</div>
            <div className="text-2xl font-bold text-text-muted">PalmPay</div>
            <div className="text-2xl font-bold text-text-muted">Moniepoint</div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 border-t border-navy-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-xl font-bold mb-4">MatchHang</h3>
              <p className="text-text-muted text-sm">
                The ultimate live match viewing experience.
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Product</h4>
              <ul className="space-y-2 text-text-muted text-sm">
                <li><Link href="/features">Features</Link></li>
                <li><Link href="/pricing">Pricing</Link></li>
                <li><Link href="/fantasy">Fantasy</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-text-muted text-sm">
                <li><Link href="/about">About</Link></li>
                <li><Link href="/terms">Terms</Link></li>
                <li><Link href="/privacy">Privacy</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Support</h4>
              <ul className="space-y-2 text-text-muted text-sm">
                <li><Link href="/help">Help Center</Link></li>
                <li><Link href="/guidelines">Community Guidelines</Link></li>
                <li><Link href="/contact">Contact</Link></li>
              </ul>
            </div>
          </div>
          <div className="mt-12 pt-8 border-t border-navy-100 text-center text-text-muted text-sm">
            <p>&copy; 2025 MatchHang. All rights reserved.</p>
            <p className="mt-2">18+ only. Gamble responsibly. Virtual credits only.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
