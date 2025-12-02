"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";

export default function AdminPage() {
  const router = useRouter();

  interface AdminStats {
    total_users: number;
    active_users: number;
    total_chats: number;
  }
  
  interface User {
    id: number;
    name: string;
    email: string;
  }
  
  const [stats, setStats] = useState<AdminStats>({} as AdminStats);
  const [users, setUsers] = useState<User[]>([]);
  const [token, setToken] = useState<string | null>(null);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loggedIn, setLoggedIn] = useState(false);
  const [error, setError] = useState("");

  // State for creating a new user
  const [newUserName, setNewUserName] = useState("");
  const [newUserEmail, setNewUserEmail] = useState("");
  const [newUserPassword, setNewUserPassword] = useState("");
  const [isCreatingUser, setIsCreatingUser] = useState(false);
  const [createUserError, setCreateUserError] = useState("");
  const [userToDelete, setUserToDelete] = useState<User | null>(null);

  // Helper for authenticated fetch requests
  const fetchAuthenticated = (url: string, options: RequestInit = {}) => {
    const storedToken = localStorage.getItem("admin_token");
    if (!storedToken) {
      // This will trigger logout and redirect
      throw new Error("Authentication token not found.");
    }

    const headers = new Headers(options.headers || {});
    headers.append('Authorization', `Bearer ${storedToken}`);

    return fetch(`${process.env.NEXT_PUBLIC_API_URL}${url}`, {
      ...options,
      headers,
    });
  };

  // Log in admin
  const loginAdmin = async () => {
    try {
      const formData = new FormData();
      formData.append('username', email);
      formData.append('password', password);
      
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/login`, {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        throw new Error("Login failed");
      }

      const data = await res.json();
      const accessToken = data.access_token;

      localStorage.setItem("admin_token", accessToken);
      setToken(accessToken);
      setLoggedIn(true);
      setError("");
    } catch (err: any) {
      console.error(err);
      setError("Login failed. Check credentials.");
    }
  };

  // Fetch admin data
  const fetchAdminData = async () => {
    try {
      const [statsRes, usersRes] = await Promise.all([
        fetchAuthenticated(`/api/stats`),
        fetchAuthenticated(`/api/users`)
      ]);

      if (statsRes.status === 401 || usersRes.status === 401) {
        logoutAdmin();
        return;
      }

      if (!statsRes.ok || !usersRes.ok) {
        throw new Error("Failed to fetch admin data");
      }

      const statsData = await statsRes.json();
      const usersData = await usersRes.json();

      setStats(statsData);
      setUsers(usersData.users);
    } catch (err: any) {
      console.error(err);
      // If the error is due to a missing token, logout.
      if (err.message.includes("Authentication token not found")) {
        logoutAdmin();
      } else {
        setError("Failed to fetch admin data.");
      }
    }
  };

  // Delete a user
  const handleDeleteUser = async () => {
    if (!userToDelete) return;

    try {
      const response = await fetchAuthenticated(`/api/admin/users/${userToDelete.id}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        throw new Error("Failed to delete user.");
      }

      // Refresh data after deletion
      await fetchAdminData();
      setCreateUserError(""); // Clear any previous errors
    } catch (err: any) {
      setCreateUserError(err.message);
    } finally {
      setUserToDelete(null); // Close the dialog
    }
  };

  // Create a new user
  const handleCreateUser = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newUserName || !newUserEmail || !newUserPassword) {
      setCreateUserError("Please fill in all fields.");
      return;
    }

    setIsCreatingUser(true);
    setCreateUserError("");

    try {
      const response = await fetchAuthenticated(`/api/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: newUserName,
          email: newUserEmail,
          password: newUserPassword,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        const errorMessage = Object.values(errorData).flat().join(' ') || "Failed to create user.";
        throw new Error(errorMessage);
      }

      // Clear form and refresh user list
      setNewUserName("");
      setNewUserEmail("");
      setNewUserPassword("");
      await fetchAdminData(); // Refresh stats and user list

    } catch (err: any) {
      setCreateUserError(err.message);
    } finally {
      setIsCreatingUser(false);
    }
  };

  // Logout function
  const logoutAdmin = () => {
    localStorage.removeItem("admin_token");
    setToken(null);
    setLoggedIn(false);
    router.push("/"); // redirect to home/login page
  };

  // Load token from localStorage on mount
  useEffect(() => {
    const storedToken = localStorage.getItem("admin_token");
    if (storedToken) {
      setToken(storedToken);
      setLoggedIn(true);
    }
  }, []);

  // Fetch data when token/loggedIn state changes
  useEffect(() => {
    if (loggedIn) {
      fetchAdminData();
    }
  }, [loggedIn]);

  if (!loggedIn) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
        <h1 className="text-3xl font-bold mb-6">Admin Login</h1>
        {error && <p className="text-red-500 mb-4">{error}</p>}
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          className="border p-2 rounded mb-2"
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          className="border p-2 rounded mb-4"
        />
        <button
          onClick={loginAdmin}
          className="bg-pink-500 text-white px-4 py-2 rounded hover:bg-pink-600"
        >
          Log In
        </button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      {/* Header with logout */}
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Admin Dashboard</h1>
        <button
          onClick={logoutAdmin}
          className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
        >
          Logout
        </button>
      </div>

      {/* Stats Section */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white rounded-xl p-4 shadow-md">
          <h2 className="text-lg font-semibold">Total Users</h2>
          <p className="text-3xl font-bold">{stats?.total_users || 0}</p>
        </div>
        <div className="bg-white rounded-xl p-4 shadow-md">
          <h2 className="text-lg font-semibold">Active Users</h2>
          <p className="text-3xl font-bold">{stats?.active_users || 0}</p>
        </div>
        <div className="bg-white rounded-xl p-4 shadow-md">
          <h2 className="text-lg font-semibold">Total Chats</h2>
          <p className="text-3xl font-bold">{stats?.total_chats || 0}</p>
        </div>
      </div>

      {/* User List */}
      <div className="bg-white rounded-xl shadow-md p-6">
        <h2 className="text-2xl font-semibold mb-4">Users</h2>
        <ul className="divide-y divide-gray-300">
          {users.map((user) => (
            <li key={user.id} className="py-3 flex justify-between items-center">
              <div>
                {user.name} — <span className="text-gray-500">{user.email}</span>
              </div>
              <AlertDialog>
                <AlertDialogTrigger asChild>
                  <button 
                    onClick={() => setUserToDelete(user)}
                    className="bg-red-500 text-white px-3 py-1 rounded text-sm hover:bg-red-600"
                  >
                    Delete
                  </button>
                </AlertDialogTrigger>
              </AlertDialog>
            </li>
          ))}
        </ul>
      </div>

      {/* Create User Form */}
      <div className="bg-white rounded-xl shadow-md p-6 mt-8">
        <h2 className="text-2xl font-semibold mb-4">Create New User</h2>
        <form onSubmit={handleCreateUser} className="space-y-4">
          {createUserError && <p className="text-red-500 text-sm">{createUserError}</p>}
          <input
            type="text"
            value={newUserName}
            onChange={(e) => setNewUserName(e.target.value)}
            placeholder="Full Name"
            className="w-full border p-2 rounded"
            required
          />
          <input
            type="email"
            value={newUserEmail}
            onChange={(e) => setNewUserEmail(e.target.value)}
            placeholder="Email Address"
            className="w-full border p-2 rounded"
            required
          />
          <input
            type="password"
            value={newUserPassword}
            onChange={(e) => setNewUserPassword(e.target.value)}
            placeholder="Password"
            className="w-full border p-2 rounded"
            required
          />
          <button
            type="submit"
            disabled={isCreatingUser}
            className="w-full bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 disabled:bg-gray-400"
          >
            {isCreatingUser ? "Creating..." : "Create User"}
          </button>
        </form>
      </div>

      {/* Deletion Confirmation Dialog */}
      {userToDelete && (
        <AlertDialog open={!!userToDelete} onOpenChange={() => setUserToDelete(null)}>
          <AlertDialogContent>
            <AlertDialogHeader>
              <AlertDialogTitle>Are you sure?</AlertDialogTitle>
              <AlertDialogDescription>
                This action cannot be undone. This will permanently delete the user account for <span className="font-semibold">{userToDelete.email}</span>.
              </AlertDialogDescription>
            </AlertDialogHeader>
            <AlertDialogFooter>
              <AlertDialogCancel>Cancel</AlertDialogCancel>
              <AlertDialogAction
                onClick={handleDeleteUser}
                className="bg-red-600 hover:bg-red-700"
              >
                Yes, delete user
              </AlertDialogAction>
            </AlertDialogFooter>
          </AlertDialogContent>
        </AlertDialog>
      )}
    </div>
  );
}