'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { api } from '@/lib/api';
import PageNavigation from '@/components/PageNavigation';

interface Wallet {
  balance: number;
  deposited_amount: number;
  winnings_amount: number;
  updated_at: string;
}

interface Transaction {
  id: number;
  type: string;
  amount: number;
  status: string;
  description: string;
  created_at: string;
  completed_at: string | null;
}

export default function WalletPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const [wallet, setWallet] = useState<Wallet | null>(null);
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);
  const [showTopUpModal, setShowTopUpModal] = useState(false);
  const [topUpAmount, setTopUpAmount] = useState('');

  useEffect(() => {
    if (!authLoading && !user) {
      router.push('/login');
    } else if (user) {
      loadWalletData();
    }
  }, [user, authLoading]);

  const loadWalletData = async () => {
    setLoading(true);

    // Load wallet
    const walletResponse = await api.getWallet();
    if (walletResponse.data) {
      setWallet(walletResponse.data as Wallet);
    }

    // Load transactions
    const transactionsResponse = await api.getTransactions();
    if (transactionsResponse.data) {
      setTransactions(transactionsResponse.data as Transaction[]);
    }

    setLoading(false);
  };

  const handleTopUp = () => {
    // TODO: Integrate payment provider
    alert('Payment integration coming soon! This will integrate with Opay/PalmPay/Moniepoint.');
    setShowTopUpModal(false);
  };

  if (authLoading || loading) {
    return (
      <div className="min-h-screen bg-navy flex items-center justify-center">
        <div className="text-text-primary text-xl">Loading wallet...</div>
      </div>
    );
  }

  if (!user || !wallet) {
    return null;
  }

  const getTransactionIcon = (type: string) => {
    switch (type) {
      case 'deposit': return '💰';
      case 'withdrawal': return '🏦';
      case 'chat_unlock': return '💬';
      case 'fantasy_entry': return '⚽';
      case 'fantasy_win': return '🏆';
      case 'refund': return '↩️';
      default: return '📝';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'text-success';
      case 'pending': return 'text-cyan';
      case 'failed': return 'text-danger';
      default: return 'text-text-muted';
    }
  };

  return (
    <div className="min-h-screen bg-navy relative overflow-hidden">
      {/* Animated Football Background - Fully Visible */}
      <div className="fixed inset-0 z-0">
        <div 
          className="absolute inset-0 bg-cover bg-center"
          style={{
            backgroundImage: "url('https://images.unsplash.com/photo-1579952363873-27f3bade9f55?q=80&w=1920&auto=format&fit=crop')",
          }}
        ></div>
        <div className="absolute inset-0 bg-gradient-to-b from-black/40 via-black/30 to-black/50"></div>
      </div>
      
      <div className="relative z-10">
      </div>
      
      {/* Header */}
      <header className="bg-gradient-to-br from-gray-900/95 via-gray-800/95 to-black/95 shadow-2xl relative z-10 border-b border-gray-700 backdrop-blur-sm" 
              style={{
                boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.1), 0 10px 30px rgba(0,0,0,0.5)',
              }}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <h1 className="text-3xl font-heading font-bold bg-gradient-to-r from-yellow-400 via-orange-400 to-yellow-500 bg-clip-text text-transparent drop-shadow-lg">
            💰 My Wallet
          </h1>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <PageNavigation />
        {/* Balance Cards */}
        <div className="grid md:grid-cols-3 gap-6 mb-8 relative z-10">
          {/* Total Balance */}
          <div className="bg-gradient-to-br from-yellow-500/30 to-orange-600/30 rounded-card p-6 border-2 border-yellow-400 backdrop-blur-md shadow-2xl transform hover:scale-105 transition-all"
               style={{
                 boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.2), 0 10px 30px rgba(251, 191, 36, 0.3)',
               }}>
            <div className="text-sm text-yellow-200 font-semibold mb-2">💵 Total Balance</div>
            <div className="text-5xl font-bold text-white mb-4 drop-shadow-lg">
              ₦{wallet.balance.toFixed(2)}
            </div>
            <button
              onClick={() => setShowTopUpModal(true)}
              className="w-full px-4 py-3 bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white font-bold rounded-lg transition-all transform hover:scale-105 shadow-lg"
            >
              ➕ Top Up Now
            </button>
          </div>

          {/* Deposited */}
          <div className="bg-gradient-to-br from-blue-600/30 to-cyan-600/30 rounded-card p-6 border-2 border-blue-400 backdrop-blur-md shadow-2xl transform hover:scale-105 transition-all"
               style={{
                 boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.2), 0 10px 30px rgba(59, 130, 246, 0.3)',
               }}>
            <div className="text-sm text-blue-200 font-semibold mb-2">💳 Deposited</div>
            <div className="text-4xl font-bold text-white mb-2 drop-shadow-lg">
              ₦{wallet.deposited_amount.toFixed(2)}
            </div>
            <div className="text-xs text-blue-100 font-medium">
              🔒 Cannot be withdrawn
            </div>
          </div>

          {/* Winnings */}
          <div className="bg-gradient-to-br from-green-600/30 to-emerald-600/30 rounded-card p-6 border-2 border-green-400 backdrop-blur-md shadow-2xl transform hover:scale-105 transition-all"
               style={{
                 boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.2), 0 10px 30px rgba(34, 197, 94, 0.3)',
               }}>
            <div className="text-sm text-green-200 font-semibold mb-2">🏆 Winnings</div>
            <div className="text-4xl font-bold text-white mb-2 drop-shadow-lg">
              ₦{wallet.winnings_amount.toFixed(2)}
            </div>
            <button
              disabled={wallet.winnings_amount <= 0}
              className="text-sm text-white font-bold hover:text-green-200 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            >
              💸 Withdraw
            </button>
          </div>
        </div>

        {/* KYC Warning */}
        {user.kyc_status !== 'verified' && (
          <div className="bg-gradient-to-r from-orange-500/30 to-red-500/30 border-2 border-orange-400 text-white px-6 py-4 rounded-card mb-8 backdrop-blur-md shadow-2xl relative z-10"
               style={{
                 boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.2), 0 10px 30px rgba(249, 115, 22, 0.3)',
               }}>
            <h3 className="font-bold mb-1 text-lg text-yellow-300">⚠️ KYC Verification Required</h3>
            <p className="text-sm mb-3 text-orange-100">
              Complete KYC verification to top up your wallet and withdraw winnings.
            </p>
            <button className="px-6 py-2 bg-gradient-to-r from-yellow-500 to-orange-500 hover:from-yellow-600 hover:to-orange-600 text-white rounded-lg text-sm font-bold shadow-lg transform hover:scale-105 transition-all">
              ✅ Start Verification
            </button>
          </div>
        )}

        {/* Transaction History */}
        <div className="bg-gradient-to-br from-gray-900/95 to-gray-800/95 rounded-card p-6 backdrop-blur-md shadow-2xl border border-gray-700 relative z-10"
             style={{
               boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.1), 0 10px 30px rgba(0,0,0,0.5)',
             }}>
          <h2 className="text-2xl font-heading font-bold bg-gradient-to-r from-blue-400 via-cyan-400 to-blue-500 bg-clip-text text-transparent mb-6 drop-shadow-lg">
            📊 Transaction History
          </h2>

          {transactions.length === 0 ? (
            <div className="text-center py-12">
              <div className="text-6xl mb-4">📝</div>
              <p className="text-gray-300 text-lg font-medium">No transactions yet</p>
              <p className="text-gray-400 text-sm mt-2">Your transaction history will appear here</p>
            </div>
          ) : (
            <div className="space-y-3">
              {transactions.map((transaction) => (
                <div
                  key={transaction.id}
                  className="bg-gradient-to-r from-gray-800/80 to-gray-900/80 rounded-lg p-4 flex items-center justify-between hover:from-gray-700/80 hover:to-gray-800/80 transition-all border border-gray-700 backdrop-blur-sm shadow-lg transform hover:scale-[1.02]"
                >
                  <div className="flex items-center gap-4">
                    <div className="text-4xl">
                      {getTransactionIcon(transaction.type)}
                    </div>
                    <div>
                      <div className="font-bold text-white text-lg">
                        {transaction.description || transaction.type.replace('_', ' ')}
                      </div>
                      <div className="text-sm text-gray-300 font-medium">
                        {new Date(transaction.created_at).toLocaleString()}
                      </div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className={`text-xl font-bold drop-shadow-lg ${
                      ['deposit', 'fantasy_win', 'refund'].includes(transaction.type)
                        ? 'text-green-400'
                        : 'text-red-400'
                    }`}>
                      {['deposit', 'fantasy_win', 'refund'].includes(transaction.type) ? '+' : '-'}
                      ₦{transaction.amount.toFixed(2)}
                    </div>
                    <div className={`text-xs font-semibold ${getStatusColor(transaction.status)}`}>
                      {transaction.status.toUpperCase()}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Payment Methods */}
        <div className="mt-8 bg-gradient-to-br from-gray-900/95 to-gray-800/95 rounded-card p-6 backdrop-blur-md shadow-2xl border border-gray-700 relative z-10"
             style={{
               boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.1), 0 10px 30px rgba(0,0,0,0.5)',
             }}>
          <h2 className="text-2xl font-heading font-bold bg-gradient-to-r from-purple-400 via-pink-400 to-purple-500 bg-clip-text text-transparent mb-6 drop-shadow-lg">
            💳 Supported Payment Methods
          </h2>
          <div className="grid md:grid-cols-3 gap-4">
            <div className="bg-gradient-to-br from-green-600/30 to-emerald-600/30 rounded-lg p-6 text-center border-2 border-green-400 backdrop-blur-sm shadow-lg transform hover:scale-105 transition-all"
                 style={{
                   boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.2), 0 8px 20px rgba(34, 197, 94, 0.3)',
                 }}>
              <div className="text-3xl font-bold text-white mb-2 drop-shadow-lg">Opay</div>
              <div className="text-sm text-green-200 font-semibold">⚡ Instant top-up</div>
            </div>
            <div className="bg-gradient-to-br from-blue-600/30 to-cyan-600/30 rounded-lg p-6 text-center border-2 border-blue-400 backdrop-blur-sm shadow-lg transform hover:scale-105 transition-all"
                 style={{
                   boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.2), 0 8px 20px rgba(59, 130, 246, 0.3)',
                 }}>
              <div className="text-3xl font-bold text-white mb-2 drop-shadow-lg">PalmPay</div>
              <div className="text-sm text-blue-200 font-semibold">⚡ Instant top-up</div>
            </div>
            <div className="bg-gradient-to-br from-orange-600/30 to-red-600/30 rounded-lg p-6 text-center border-2 border-orange-400 backdrop-blur-sm shadow-lg transform hover:scale-105 transition-all"
                 style={{
                   boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.2), 0 8px 20px rgba(249, 115, 22, 0.3)',
                 }}>
              <div className="text-3xl font-bold text-white mb-2 drop-shadow-lg">Moniepoint</div>
              <div className="text-sm text-orange-200 font-semibold">⚡ Instant top-up</div>
            </div>
          </div>
        </div>
      </main>

      {/* Top Up Modal */}
      {showTopUpModal && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-gradient-to-br from-gray-900 to-gray-800 rounded-card p-8 max-w-md w-full border-2 border-yellow-400 shadow-2xl"
               style={{
                 boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.1), 0 20px 60px rgba(251, 191, 36, 0.4)',
               }}>
            <h2 className="text-3xl font-heading font-bold bg-gradient-to-r from-yellow-400 to-orange-500 bg-clip-text text-transparent mb-6 drop-shadow-lg">
              💰 Top Up Wallet
            </h2>
            
            <div className="mb-6">
              <label className="block text-sm font-bold text-yellow-300 mb-2">
                Amount (₦)
              </label>
              <input
                type="number"
                min="100"
                step="100"
                value={topUpAmount}
                onChange={(e) => setTopUpAmount(e.target.value)}
                placeholder="Enter amount"
                className="w-full px-4 py-3 bg-gray-800 border-2 border-gray-600 rounded-lg text-white font-semibold text-lg focus:outline-none focus:border-yellow-400 transition-all"
              />
              <div className="text-xs text-gray-300 font-medium mt-2">
                💵 Minimum: ₦100
              </div>
            </div>

            <div className="mb-6">
              <label className="block text-sm font-bold text-yellow-300 mb-2">
                Payment Method
              </label>
              <select className="w-full px-4 py-3 bg-gray-800 border-2 border-gray-600 rounded-lg text-white font-semibold focus:outline-none focus:border-yellow-400 transition-all">
                <option>Opay</option>
                <option>PalmPay</option>
                <option>Moniepoint</option>
              </select>
            </div>

            <div className="flex gap-3">
              <button
                onClick={() => setShowTopUpModal(false)}
                className="flex-1 px-4 py-3 bg-gray-700 hover:bg-gray-600 text-white font-bold rounded-lg transition-all transform hover:scale-105"
              >
                ❌ Cancel
              </button>
              <button
                onClick={handleTopUp}
                disabled={!topUpAmount || parseInt(topUpAmount) < 100}
                className="flex-1 px-4 py-3 bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white font-bold rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-105 shadow-lg"
              >
                ✅ Continue
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
