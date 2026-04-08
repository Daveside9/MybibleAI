import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "@/contexts/AuthContext";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

// Temporarily disabled Poppins due to Turbopack font loading issue in Next.js 16.0.6
// const poppins = Poppins({
//   variable: "--font-poppins",
//   weight: ["400", "600", "700"],
//   subsets: ["latin"],
// });

export const metadata: Metadata = {
  title: "MatchHang - Watch Live. Banter Loud.",
  description: "Live match streaming + social viewing rooms with chat, reactions, and fantasy football",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.variable} antialiased`}>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
